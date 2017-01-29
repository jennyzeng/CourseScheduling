from Course import Course, CoursesGraph
from scheduling import courseScheduling
from loadData import DataLoading

creditsPerQuarter = 16
def widthFunc(level, course):
	return sum([graph[c].units for c in level]) + course.units > creditsPerQuarter


graph = CoursesGraph()
DataLoading.loadPrereq(graph, "info/test/courses2.txt")
graph.updateSatisfies()
# print(graph)
print("Taking %d credits per quarter: " % (creditsPerQuarter))
for i, L in enumerate(courseScheduling(graph, widthFunc)):
	print("year %d quarter %d:" % (i // 3 + 1, i % 3 + 1), L)

"""
Taking 16 credits per quarter:
year 1 quarter 1: ['I&CSCI6B', 'I&CSCI31', 'MATH1A', 'I&CSCI90']
year 1 quarter 2: ['I&CSCI6D', 'I&CSCI51', 'I&CSCI32']
year 1 quarter 3: ['IN4MATX43', 'I&CSCI53+53L', 'I&CSCI33']
year 2 quarter 1: ['MATH1B', 'I&CSCI45C']
year 2 quarter 2: ['MATH2A', 'I&CSCI46']
year 2 quarter 3: ['MATH2B', 'COMPSCI164']
year 3 quarter 1: ['MATH3A', 'STATS67', 'COMPSCI161']
year 3 quarter 2: ['COMPSCI162', 'COMPSCI116', 'COMPSCI178', 'COMPSCI171']
year 3 quarter 3: ['COMPSCI163', 'COMPSCI165', 'COMPSCI175']
year 4 quarter 1: ['COMPSCI169']
year 4 quarter 2: ['COMPSCI167']

"""
