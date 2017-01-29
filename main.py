from Course import Course, CoursesGraph
from scheduling import courseScheduling
from loadData import DataLoading

def widthFunc(level):
	return sum([graph[c].units for c in level])>16

graph = CoursesGraph()
DataLoading.loadPrereq(graph, "info/test/courses2.txt")
graph.updateSatisfies()
print(graph)
for i, L in enumerate(courseScheduling(graph, widthFunc)):
	print(i, ": ", L)

"""
0 :  ['I&CSCI90', 'I&CSCI31', 'MATH1A', 'IN4MATX43', 'I&CSCI6B']
1 :  ['I&CSCI32', 'MATH1B', 'I&CSCI51', 'I&CSCI6D']
2 :  ['I&CSCI33', 'MATH2A', 'I&CSCI53+53L']
3 :  ['I&CSCI45C', 'MATH2B']
4 :  ['I&CSCI46', 'STATS67', 'MATH3A']
5 :  ['COMPSCI162', 'COMPSCI164', 'COMPSCI161', 'COMPSCI171', 'COMPSCI169', 'COMPSCI178']
6 :  ['COMPSCI163', 'COMPSCI167', 'COMPSCI165', 'COMPSCI175']
"""