"""
an example about how to load data and generate a schedule
"""
from loadData import DataLoading
from Graph import CourseGraph
from Schedule import Schedule

if __name__ == '__main__':
    G = CourseGraph({})
    DataLoading.load_courses(G, prereq_filename="test/testcourses.txt",
                             show_upper=True)
    R_detail, R = DataLoading.load_requirements(
        requirements=["firstReq", "secondReq"],
        filename="test/test_spec.txt")
    G.load_requirements(R_detail)
    L = Schedule(DataLoading.load_width_func_table("test/test_widthFunc.txt"))
    G.labeling()
    print(G)