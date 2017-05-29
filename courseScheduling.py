from Graph import CourseGraph
from Course import Course
from Schedule import Schedule
from priodict import priorityDictionary as priodict

class CourseScheduling:
    def __init__(self, total_quarter_codes=6):
        self.total_quarter_codes = total_quarter_codes


    def get_schedule(self, G:CourseGraph, L: Schedule, u:int, R):
        """
        :param G: course graph G
        :param L: empty schedule
        :param u: upper bound layer index
        :param R: requirements table
        :return: schedule
        """
        PQ = self._init_priodict(G)

        while PQ:
            current = PQ.smallest()
            del PQ[current]
            if G[current].courseValue == 0: # do not assign this course
                continue


    def _course_satisfy_any_requirements(self, v:Course):
        pass





    def _init_priodict(self, G:CourseGraph):
        PQ = priodict()
        for cid, course in G.items():
            if not course.prereq_list(): # course has no prereq
                PQ[cid] = course.label
        return PQ



    def assign_course(self, v: Course, L: Schedule, u: int):
        """
        :param v: course
        :param L: schedule
        :param u: upperBound index
        :return: the index of the layer where v will be assigned
        """
        step = len(L) - 1
        if self.valid(L, step, v) or v.has_dependent(step):
            L.add_layer()
            i = step + 1
            while not self.valid(L, i, v) and (not v.isUpperOnly or i >= u):
                # add new empty layer L_i above current highest layer
                L.add_layer()
                i += 1

        lastStep = len(L) - 1
        assigned = False
        while not assigned and (not v.isUpperOnly or step >= u):
            if v.has_dependent(step):
                return lastStep
            elif self.valid(L, step, v):
                lastStep = step
            step -= 1

        return lastStep

    def valid(self, L: Schedule, i: int, v: Course):
        """
        For a course v, we define a layer L_i with
        M_i+v.units < W(L_i) and (i mod 6) in v.quarterCodes
        to be a valid layer of v.

        :param L: current schedule
        :param i: index for layer L_i
        :param v:  course
        :return:   true if valid
        """
        return L.layer_is_full(i, v.units) and \
               (i % self.total_quarter_codes) in v.quarterCodes
