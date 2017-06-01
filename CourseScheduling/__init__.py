from CourseScheduling.Course import Course
from CourseScheduling.Graph import CourseGraph
from CourseScheduling.CourseScheduling import CourseScheduling
from CourseScheduling.Schedule import Schedule


## two helper functions

def is_upper_standing(applied_units, upper_units):
    """
    :param applied_units: How many units the user has applied
    :param upper_units: If applied_units >= upper_units, the user is upper division standing
    :return: True if the user is upper division standing
    """
    return applied_units > upper_units


def update_requirements(R_detail, R, taken):
    """
    Update the requirements table according to the courses the user has already taken
    :param R_detail: a detail requirements table, showing which course cid satisfy which requirement at each set
    :param R: a brief requirements table, showing for each requirements, how many courses is required for each subset
    :param taken: a set of courses that the user've taken. They will be removed from requirements table
    :return: updated  R_detail, R. (but original R_detail and R are changed!!!)
    """
    for rid, rlist in R_detail.items():
        for index, rset in enumerate(rlist):
            for cid in set(rset):
                if cid in taken:
                    R[rid][index] = max(R[rid][index] - 1, 0)
                    R_detail[rid][index].remove(cid)
    return R_detail, R
