from Graph import CourseGraph
from Course import Course
from Schedule import Schedule
from priodict import priorityDictionary as priodict
from copy import deepcopy

__author__ = "Jenny Zeng"
__email__ = "jennyzengzzh@gmail.com"


class CourseScheduling:
    def __init__(self, start_q=0, total_quarter_codes=6):
        self.total_quarter_codes = total_quarter_codes
        self.start_q = start_q

    def get_best_schedule(self, G: CourseGraph, L: Schedule, R: dict, from_u: int, to_u: int):
        """
        :param G: CourseGraph
        :param L: Schedule
        :param R: brief requirements table
        :param from_u:  left upper bound range, inclusive
        :param to_u: right upper bound range, inclusive
        :return:
                best: the schedule with the min makespan among all schedules generated
                best_u: the upper bound for the best schedule
                best_r: How the schedule satisfy the requirements. if number >= 1,
                        it means there is still some requirements it does not satisfy.
        """
        best = None
        best_u = None
        best_r = None
        for u in range(from_u, to_u + 1):
            G_temp = deepcopy(G)
            L_temp = deepcopy(L)
            R_temp = deepcopy(R)
            schedule = self.get_single_schedule(G_temp, L_temp, R_temp, u)
            if schedule and (not best or len(schedule) > len(best)):
                best = schedule
                best_u = u
                best_r = R_temp
        return best, best_u, best_r

    def get_single_schedule(self, G: CourseGraph, L: Schedule, R, u: int):
        """
        :param G: a labeled course graph G
        :param L: empty schedule
        :param u: upper bound layer index
        :param R: requirements table
        :return: schedule if schedule is valid, else none
        """
        PQ = self._init_priodict(G)
        while PQ:
            current = PQ.smallest()
            del PQ[current]
            cur_course = G[current]
            if self._course_satisfy_any_requirements(cur_course, R):  # assign this course
                assigned_index = self.find_course_assign_index(cur_course, L, u)
                L.add_course(assigned_index, current, cur_course.units)
                self._expand_queue(G, current, PQ, assigned_index)
                self.tag_requirement(R, cur_course)
        if not self._violates_upper(G, R, L, u):
            # L.clear_empty()
            return L
        else:
            return None

    def _violates_upper(self, G: CourseGraph, R, L: Schedule, u: int):
        """
        :param G: CourseGraph
        :param L: Schedule
        :param u: upper bound index
        :return: if the schedule violates the upper bound. If violates, return True
        """
        # first check R is all 0
        # if any([any(i) for i in R.values()]):
        #     return True
        if u > len(L): return True
        # check if a upper only class is in lower division
        for clist in L.L[:u]:
            for cid in clist:
                if G[cid].isUpperOnly:
                    return True
        return False

    def tag_requirement(self, R, v: Course):
        """
        after we assign the course v to the schedule, we check what requirements it satisfies
        :param R: requirements table
        :param v: Course
        """
        for requirement, index in v.requirements:
            R[requirement][index] = max(0, R[requirement][index] - 1)

    def _expand_queue(self, G, cid, PQ: priodict, assigned_index: int):
        """
        after we assign course v to the schedule, we expand the priority queue with new ready coruses
        at the same time, we also tag prereq in course cid's successors in the corresponding OR set.
        :param G: CourseGraph
        :param cid: course id, the key in G
        :param PQ: Priority queue
        :param assigned_index: where cid is assigned in L.
        """
        for child, OR_index in G[cid].successors:
            if child not in G:
                continue
            child_course = G[child]
            if not child_course.prereqBool[OR_index]:
                child_course.tag_prereq(OR_index, cid)
                child_course.dependentIndex = max(assigned_index, G[child].dependentIndex)

            if child_course.prereq_is_satisfied():
                PQ[child] = child_course.label

    def _course_satisfy_any_requirements(self, v: Course, R):
        """
        :param v: course
        :param R: Requirements table
        :return: True if v satisfy any requirements in R.
        """
        for name, index in v.requirements:
            if R[name][index] > 0:
                return True

        return False

    def _init_priodict(self, G: CourseGraph):
        """
        initialize the priodict with current ready courses
        :param G:
        :return:
        """
        PQ = priodict()
        for cid, course in G.items():
            if not course.unsatisfied_prereq():  # course has no prereq
                PQ[cid] = course.label
        return PQ

    def find_course_assign_index(self, v: Course, L: Schedule, u: int):
        """
        single course assignment
        :param v: course
        :param L: schedule
        :param u: upperBound index
        :return: the index of the layer where v will be assigned
        """
        step = len(L) - 1
        i = step
        if (not self._valid(L, step, v)) or v.has_dependent(step):
            i += 1
            while not self._valid(L, i, v) and (not v.isUpperOnly or i >= u):
                # add new empty layer L_i above current highest layer
                # L.add_layer()
                i += 1

        lastStep = i
        step -= 1
        while (v.isUpperOnly and step >= u) or (not v.isUpperOnly and step >= 0):
            if v.has_dependent(step):
                break
            elif self._valid(L, step, v):
                lastStep = step
            step -= 1

        return lastStep

    def _valid(self, L: Schedule, i: int, v: Course):
        """
        For a course v, we define a layer L_i with
        M_i+v.units < W(L_i) and (i mod 6) in v.quarterCodes
        to be a valid layer of v.

        :param L: current schedule
        :param i: index for layer L_i
        :param v:  course
        :return:   true if valid
        """
        return (not L.layer_is_full(i, v.units)) and ((i + self.start_q) % self.total_quarter_codes) in v.quarterCodes
