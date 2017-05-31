import sys
from collections import deque


class CourseGraph:
    def __init__(self, G: dict()):
        """
        :param G: a dict object representing the graph for courses
        """
        self.G = G

    def __str__(self):
        return ";\n ".join("{}:\n{}".format(k, v) for k, v in self.G.items())

    def __contains__(self, item):
        return item in self.G

    def __delete__(self, instance):
        del self.G[instance]

    def __getitem__(self, item):
        return self.G[item]

    def __setitem__(self, key, value):
        self.G[key] = value

    def items(self):
        return self.G.items()

    def update_successors(self):
        """
        update successors info for courses after adding courses into the graph
        """
        for k, v in self.G.items():
            for index, OR in enumerate(v.prereq):
                for cid in OR:
                    if cid in self.G:
                        self.G[cid].successors.add((k, index))

    def load_requirements(self, Rs: dict):
        """
        load a dict of requirements into the courses
        :param Rs: a set of requirements
        :return:
        """
        for requirement, AND in Rs.items():
            for index, OR in enumerate(AND):
                for cid in OR:
                    if cid in self.G:
                        self.G[cid].requirements.add((requirement, index))

    # def clear_free_courses(self):
    #     """
    #     clear courses that are not required (not satisfy any requirements)
    #     may not required because we check before scheduling the course
    #     """
    #     for cid, course in self.G.items():
    #         if course.courseValue == 0:
    #             del self.G[cid]

    def _topological_order(self):
        """
        :return: a topological ordering for the items in graph
        direction is u -> u.prereq (from sink)
        """
        from collections import Counter
        from copy import deepcopy

        C = deque()  # collection of nodes with no incoming edges
        D = Counter()  # counter for counting the number of incoming edges
        for k, v in self.G.items():
            for w in v.prereq_list():
                if w in self.G:
                    D[w] += 1
        for k, v in self.G.items():  # find nodes at sink
            if D[k] == 0:
                C.append(k)
        output = []
        starts = deepcopy(C)
        while C:
            cid = C.popleft()
            output.append(cid)
            for w in self.G[cid].prereq_list():
                if w in self.G and w not in output:
                    D[w] -= 1
                    if D[w] == 0:
                        C.append(w)
        if len(output) != len(self.G):
            raise Exception("exist cycle, cannot get a topological order")
        return output, starts

    def labeling(self):
        for cid, course in self.G.items():
            if course.courseValue == 0:
                del self.G[cid]
            elif course.successors:
                course.label = sys.maxsize
            else:
                course.label = course.courseValue
        topological_order, starts = self._topological_order()
        for v in topological_order:
            for u in self.G[v].prereq_list():
                self.G[u].label = min((self.G[v].label + self.G[u].courseValue),
                                      self.G[u].label)
        return starts
