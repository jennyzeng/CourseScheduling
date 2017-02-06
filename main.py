from Course import Course, CoursesGraph
from scheduling import *
from loadData import DataLoading

creditsPerQuarter = 16
def widthFunc(level, course):
	return sum([graph[c].units if graph[c] else geGraph[c].units for c in level]
	           ) + course.units > creditsPerQuarter

SpecsCourse,SpecsNum = DataLoading.loadSpec()
graph = CoursesGraph()
DataLoading.loadCourses(graph, "info/test/courses4.txt")
graph.updateSatisfies()
print("Taking %d credits per quarter: " % (creditsPerQuarter))
L = courseScheduling(graph, widthFunc, SpecsCourse, SpecsNum)
geGraph = CoursesGraph()
DataLoading.loadCourses(geGraph, "info/test/ge.txt")
addGEs(L, geGraph, widthFunc)
for i, L in enumerate(L):
	print("year %d quarter %d:" % (i // 3 + 1, i % 3 + 1), L)

"""
Taking 16 credits per quarter:
year 1 quarter 1: ['I&CSCI90', 'WRITING39A', 'I&CSCI31', 'MATH2A']
year 1 quarter 2: ['I&CSCI6B', 'WRITING39B', 'I&CSCI32', 'MATH2B']
year 1 quarter 3: ['IN4MATX43', 'I&CSCI6D', 'I&CSCI51']
year 2 quarter 1: ['WRITING39C', 'I&CSCI33', 'MATH3A', 'STATS67']
year 2 quarter 2: ['I&CSCI53+53L', 'I&CSCI45C', 'COMPSCI178', 'GEVI']
year 2 quarter 3: ['I&CSCI46', 'GEVa', 'GEVIII', 'GEII-3']
year 3 quarter 1: ['COMPSCI169', 'COMPSCI161', 'COMPSCI171', 'GEIV-1']
year 3 quarter 2: ['COMPSCI162', 'COMPSCI116', 'COMPSCI167', 'COMPSCI175']
year 3 quarter 3: ['COMPSCI164', 'COMPSCI165', 'COMPSCI163', 'GEII-1']
year 4 quarter 1: ['GEIV-2', 'GEII-2', 'GEVII', 'GEVb']
year 4 quarter 2: ['GEIV-3']
"""
