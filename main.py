from Course import Course, CoursesGraph
from scheduling import *
from loadData import DataLoading

creditsPerQuarter = 16


# def widthFunc(level, course):
# 	return sum([graph[c].units if graph[c] else geGraph[c].units for c in level]
# 	           ) + course.units > creditsPerQuarter


# data loading
## for Computer Science graph
SpecsCourse, SpecsTable = DataLoading().loadSpec(major="Computer Science",
                                                 specs=["Lower-division", "Upper-division", "Intelligent Systems"],
                                                 filename="info/specializations.txt")
graph = CoursesGraph()
DataLoading().loadCourses(graph, "info/test/fullcourses.txt")
graph.updateSatisfies()
graph.loadSpecs(SpecsCourse)

## ge graph
geGraph = CoursesGraph()
DataLoading().loadCourses(geGraph, "info/test/ge.txt")
generalCourse, generalSpecsTable = DataLoading().loadSpec(major="General",
                                                          specs=["GEII", "GEIV", "GEV", "GEVI", "Writing"],
                                                          filename="info/test/general.txt")
geGraph.loadSpecs(generalCourse)
# print(graph)

SpecsTable.update(generalSpecsTable)

# scheduling
L = CourseScheduling([graph, geGraph], SpecsTable).multiGraphScheduling()

print("Taking %d credits per quarter: " % (creditsPerQuarter))
for i, L in enumerate(L):
	print("year %d quarter %d:" % (i // 3 + 1, i % 3 + 1), L)

"""
Taking 16 credits per quarter:
year 1 quarter 1: ['I&CSCI6B', 'I&CSCI31', 'MATH2A', 'I&CSCI90']
year 1 quarter 2: ['I&CSCI6D', 'COMPSCI125', 'I&CSCI51']
year 1 quarter 3: ['I&CSCI32', 'MATH2B', 'GEVII-1', 'GEVb']
year 2 quarter 1: ['IN4MATX43', 'I&CSCI33', 'STATS67', 'MATH3A']
year 2 quarter 2: ['I&CSCI45C', 'COMPSCI178', 'GEVIII-1', 'GEII-2']
year 2 quarter 3: ['I&CSCI46', 'GEIV-2', 'GEIV-3', 'GEII-1']
year 3 quarter 1: ['COMPSCI169', 'COMPSCI171', 'COMPSCI161', 'GEII-3']
year 3 quarter 2: ['COMPSCI175', 'GEIV-1', 'GEVa', 'GEVI-1']
"""
