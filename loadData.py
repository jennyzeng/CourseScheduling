from Course import Course
from Graph import CourseGraph
import re


class DataLoading:
    @staticmethod
    def load_width_func_table(filename):
        wdict = {}
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip().split(":")
                if line[0] == "else":
                    wdict["else"] = int(line[1])
                else:
                    wdict[int(line[0])] = int(line[1])
        return wdict

    @staticmethod
    def load_courses(prereq_filename, show_upper=True):
        """
        load courses in the file to the graph
        :param G: graph
        :param prereq_filename: filename
        :param show_upper: if true, config upper, otherwise all courses is not upper only.
        """
        G = dict()
        with open(prereq_filename, 'r') as f:
            for line in f:
                info = line.strip().split(";")

                G["".join(info[0:2])] = Course(name=info[2], units=int(info[4]),
                                               quarter_codes=eval(info[5]), prereq=eval(info[3]),
                                               is_upper_only=eval(info[6])if show_upper else False)
        return G

    @staticmethod
    def load_requirements(requirements, filename):
        """
        :param requirements: the list of requirements you want to get from the file
        :param filename: the name of the file storing the requirements information
        :return:
                hashTable: store Course nums set for each spec
                            is only used for updating the graph
                R:  a table of requirements.
                    stores the corresponding require num for that course nums set.
                    each requirement is a AND of ORs.
                    unlike the prerequisite, requirements require students to take a specific
                    number of courses in ORs, not only one.
                    suppose the requirement name is k, and the index of OR is i, then
                    R[k][i] = n, where n is the number of courses required for OR set i.
        """
        hashTable = {}
        R = {}
        with open(filename) as f:
            content = f.read().split(";")
            for requirement in content:
                requirement = requirement.strip().split('\n')
                if requirement[0] not in requirements:
                    continue
                hashTable[requirement[0]] = []
                R[requirement[0]] = []
                i = 1

                while i < len(requirement):
                    if re.match("^(all)$|^([1-9][0-9]*)$", requirement[i]):
                        hashTable[requirement[0]].append(set())
                        R[requirement[0]].append(requirement[i])
                        i += 1  # skip {

                    elif requirement[i] == "}":
                        # change keys at end
                        if R[requirement[0]][-1] == "all":
                            R[requirement[0]][-1] = len(hashTable[requirement[0]][-1])
                        elif R[requirement[0]][-1] == "recommend":  # TODO: need modify later
                            R[requirement[0]][-1] = len(hashTable[requirement[0]][-1]) // 2
                        else:
                            R[requirement[0]][-1] = eval(R[requirement[0]][-1])
                        i += 1
                    elif "{" in requirement[i]:
                        i += 1
                    else:
                        hashTable[requirement[0]][-1].add(requirement[i].replace(" ", ""))
                        i += 1

        return hashTable, R

    @staticmethod
    def load_taken(filename):
        """
        taken.txt file is in the following format:
        first line: start quarter code
        second line: total units applied
        then, each line on and after third line shows a cid that you've taken.txt
        :return: start quater code, units, a set of cid
        """
        with open(filename) as f:
            cids = set()
            startQ = int(f.readline())
            totalUnits = int(f.readline())
            for cid in f.readlines():
                cid = cid.strip()
                cids.add(cid)
        return startQ, totalUnits, cids

    @staticmethod
    def load_avoid(filename):
        avoids = set()
        with open(filename) as f:
            for cid in f.readlines():
                cid = cid.strip()
                avoids.add(cid)
        return avoids


if __name__ == "__main__":
    # graph = CoursesGraph()
    # DataLoading.loadCourses(graph)
    # graph.updateSatisfies()
    # print(graph)
    # print(DataLoading.load_requirements(
    #                              requirements=["Lower-division", "Upper-division", "Intelligent Systems"],
    #                              filename="info/test/specializations.txt"))

    print(DataLoading.load_requirements(requirements=["firstReq", "secondReq"],
                                        filename="test/test_spec.txt"))
