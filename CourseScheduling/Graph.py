"""
The course graph for scheduling. It uses a basic adjacency structure for graph
"""
from collections import deque

__author__ = "Jenny Zeng"
__email__ = "jennyzengzzh@gmail.com"

class CourseGraph:
    def __init__(self, G: dict, r_detail: dict,R:dict, avoid=None, taken=None):
        """
        :param G: a dict object representing the graph for courses
        :param r_detail: a **detail** requirement table. It is required.
                format: {r_name: [set1, set2,...]}
        :param R: a requirements table counting the number of courses required for
                each requirements
        :param avoid: a set of cids
        :param taken: a set of cids
        """
        self.G = G
        self.update_successors()
        if avoid:
            self.add_avoid(avoid)
        if taken:
            self.update_taken(taken)

        self.update_requirements(r_detail, R)

        # labeling is done here because we know the requirements
        self.labeling()

    def __str__(self):
        return ";\n ".join("{}:\n{}".format(k, v) for k, v in self.G.items())

    def __contains__(self, item):
        return item in self.G

    def __getitem__(self, item):
        return self.G[item]

    def __setitem__(self, key, value):
        self.G[key] = value

    def add_avoid(self, cids: set):
        """
        :param cids: a list of cid, showing the courses you want to avoid
        :return:
        """
        for cid in cids:
            if cid in self.G:
                del self.G[cid]

    def items(self):
        """
        :return: (cid, course) in self.G graph
        """
        return self.G.items()

    def __delitem__(self, key):
        del self.G[key]

    def labeling(self):
        """
        label courses according to their longest distance to the sink
        ( to the courses without any successors)
        """
        for cid, course in list(self.G.items()):
            if course.courseValue == 0:
                del self.G[cid]
            else:
                course.label = course.courseValue

        topological_order, starts = self._topological_order()
        for v in topological_order:
            for u in self.G[v].prereq_list():
                if u in self.G:
                    self.G[u].label = min((self.G[v].label + self.G[u].courseValue),
                                          self.G[u].label)
        return starts

    def update_taken(self, cids):
        """
        update the taken information. remove courses in cids from the graph, and
        tag the prereq of those courses' successors.
        :param cids: a list of courses one've taken
        """
        for cid in cids:
            if cid in self.G:
                for child, index in self.G[cid].successors:
                    if child in self.G:
                        self.G[child].tag_prereq(index, cid)
                del self.G[cid]

    def update_successors(self):
        """
        update successors info for courses after adding courses into the graph
        """
        for k, v in self.G.items():
            for index, OR in enumerate(v.prereq):
                for cid in OR:
                    if cid in self.G:
                        self.G[cid].successors.add((k, index))

    def update_requirements(self, R_detail:dict, R: dict):
        """
        add a dict of requirements into the courses. will not remove the requirements already exist in the graph
        note: after update requirements, one should update the labels to enable the change

        :param Rs: a set of requirements
        """
        for requirement, AND in R_detail.items():
            for index, OR in enumerate(AND):
                if R[requirement][index]:
                    for cid in OR:
                        if cid in self.G:
                            self.G[cid].requirements.add((requirement, index))


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
