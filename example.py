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
            for cid in set(rset):
                if cid in taken:
                    R[rid][index] = max(R[rid][index] - 1, 0)
                    R_detail[rid][index].remove(cid)
    return R_detail, R


if __name__ == '__main__':
    # load taken info
    startQ, applied_units, taken = DataLoading.load_taken(filename="info/test/taken2.txt")
    # config upper standing units
    upper_units = 90
    # load avoid info
    avoid = DataLoading.load_avoid(filename="info/test/avoid.txt")
    # load graph, config if user is upper standing
    G = DataLoading.load_courses(prereq_filename="info/test/fullcourses_new.txt",
                                 show_upper=is_upper_standing(0, upper_units))
    # load requirement sheet
    R_detail, R = DataLoading.load_requirements(
        requirements=["University", "GEI", "GEII", "GEIII", "GEIV",
                      "GEV", "GEVI", "GEVII", "GEVIII", "CS-Lower-division", "CS-Upper-division",
                      "Algorithms", "Intelligent Systems"],
        filename="info/test/specializations.txt")

    # update requirement table based on the taken information
    update_requirements(R_detail, R, taken)

    # load max width for each quarter
    max_widths = DataLoading.load_width_func_table("info/test/widthFunc.txt")

    # construct CourseGraph. graph is labeled after init
    graph = CourseGraph(G, r_detail=R_detail, R=R, avoid=avoid, taken=taken)

    # construct Schedule with width func requirements
    L = Schedule(widths=max_widths)
    # construct the scheduling class
    cs = CourseScheduling(start_q=startQ)
    # get the best schedule when the upper bound range from 0 to 10, inclusive.
    L, best_u, best_r = cs.get_best_schedule(graph, L, R, 0, 10)
    print(L)
    print(best_u)
    print(R_detail)
    print(best_r)
