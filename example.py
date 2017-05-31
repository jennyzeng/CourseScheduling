"""
an example about how to load data and generate a schedule
"""
from loadData import DataLoading
from Graph import CourseGraph
from Schedule import Schedule
from CourseScheduling import CourseScheduling


def is_upper_standing(applied_units, upper_units):
    return applied_units > upper_units


def update_requirements(R_detail, R, taken):
    for rid, rlist in R_detail.items():
        for index, rset in enumerate(rlist):
            for cid in rset:
                if cid in taken:
                    R[rid][index] = max(R[rid][index] - 1, 0)

    return R_detail, R


if __name__ == '__main__':
    # load taken info
    startQ, applied_units, taken = DataLoading.load_taken(filename="test/taken.txt")
    # config upper standing units
    upper_units = 5
    # load avoid info
    avoid = DataLoading.load_avoid(filename="test/avoid.txt")
    # load graph, config if user is upper standing
    G = DataLoading.load_courses(prereq_filename="test/testcourses.txt",
                                 show_upper=is_upper_standing(applied_units, upper_units))
    # load requirement sheet
    R_detail, R = DataLoading.load_requirements(
        requirements=["firstReq", "secondReq"],
        filename="test/test_spec.txt")

    # update requirement table based on the taken information
    update_requirements(R_detail, R, taken)

    # load max width for each quarter
    max_widths = DataLoading.load_width_func_table("test/test_widthFunc.txt")

    # construct CourseGraph. graph is labeled after init
    graph = CourseGraph(G, r_detail=R_detail, avoid=avoid)

    # construct Schedule with width func requirements
    L = Schedule(widths=max_widths)

    cs = CourseScheduling()
    L, best_u, best_r = cs.get_best_schedule(graph, L, R, 0, 3)
    print(L)
    print(best_u)
    print(best_r)
    # print(graph)
