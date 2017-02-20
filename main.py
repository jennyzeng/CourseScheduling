from Course import Course, CoursesGraph
from scheduling import *
from loadData import DataLoading

creditsPerQuarter = 16

# data loading
## for Computer Science graph
SpecsCourse, SpecsTable = DataLoading().loadSpec(major="Computer Science",
                                                 specs=["Lower-division", "Upper-division","Writing","Intelligent Systems"],
                                                 filename="info/specializations.txt")
graph = CoursesGraph()
DataLoading().loadCourses(graph, "info/test/fullcourses.txt")
# DataLoading().loadCourses(graph, "info/test/noprereq.txt")
graph.updateSatisfies()
graph.loadSpecs(SpecsCourse)

## ge graph
geGraph = CoursesGraph()
DataLoading().loadCourses(geGraph, "info/test/ge.txt")
generalCourse, generalSpecsTable = DataLoading().loadSpec(major="General",
                                                          specs=["GEII", "GEIV", "GEV", "GEVI"],
                                                          filename="info/test/general.txt")
# graph.mergeGraph(geGraph)
geGraph.loadSpecs(generalCourse)
# print(graph)
# graph.mergeGraph(geGraph)
SpecsTable.update(generalSpecsTable)



# scheduling
L, SpecsTable = CourseScheduling([graph,geGraph], SpecsTable, 16).multiGraphScheduling()

print("Taking %d credits per quarter: " % (creditsPerQuarter))
for i, L in enumerate(L):
	print("year %d quarter %d:" % (i // 3 + 1, i % 3 + 1), L)

print(SpecsTable)
print(SpecsCourse)
"""
Taking 16 credits per quarter:
year 1 quarter 1: ['I&CSCI6B', 'I&CSCI31', 'I&CSCI90', 'WRITING39A']
year 1 quarter 2: ['MATH2A', 'I&CSCI6D', 'IN4MATX131', 'I&CSCI32']
year 1 quarter 3: ['I&CSCI51', 'WRITING39B', 'MATH2B']
year 2 quarter 1: ['IN4MATX43', 'I&CSCI33', 'WRITING39C', 'MATH3A']
year 2 quarter 2: ['STATS67', 'I&CSCI45C', 'IN4MATX113', 'COMPSCI122A']
year 2 quarter 3: ['COMPSCI132', 'I&CSCI139W', 'I&CSCI46', 'GEIV-2']
year 3 quarter 1: ['COMPSCI151', 'COMPSCI184A', 'COMPSCI169', 'COMPSCI112']
year 3 quarter 2: ['COMPSCI178', 'COMPSCI125', 'I&CSCI161', 'COMPSCI133']
year 3 quarter 3: ['COMPSCI154', 'GEVIII-1', 'GEVI-1', 'GEII-1']
year 4 quarter 1: ['COMPSCI161', 'COMPSCI171', 'GEIV-1', 'GEII-2']
year 4 quarter 2: ['COMPSCI175', 'GEIV-3', 'GEVII-1']
"""
