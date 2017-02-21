from Course import Course, CoursesGraph
from scheduling import *
from loadData import DataLoading


def loadData(major, specs, specsFilename, courseFilename, useTaken, takenFilename):
	specsCourse, specsTable = DataLoading().loadSpec(
									major=major, specs=specs, filename=specsFilename)
	graph = CoursesGraph()
	DataLoading().loadCourses(graph, courseFilename)
	graph.updateSatisfies()
	graph.loadSpecs(specsCourse)
	defaultUnits = 0
	if useTaken:
		defaultUnits = DataLoading().loadTaken(graph, specsTable, takenFilename)

	return graph, specsTable, defaultUnits


def printResult(L, bestBound, startQ, creditsPerQuarter):
	print("start quarter: ", startQ)
	print("Taking %d credits per quarter: " % (creditsPerQuarter))
	for i, level in enumerate(L):
		i = i + startQ
		print("year %d quarter %d:" % (i // 3 + 1, i % 3 + 1), level)

	print("best upper bound: year %d quarter %d" % (bestBound // 3 + 1, bestBound % 3 + 1))


if __name__ == '__main__':
	creditsPerQuarter = 17
	startQ = 2
	# data loading
	## for Computer Science graph
	graph, specsTable, defaultUnits = loadData(
		major="Computer Science",
		specs=["GEI", "GEII", "GEIII", "GEIV", "GEV", "GEVI",
		       "Lower-division",
		       "Upper-division",
		       "Algorithms",
		       "Intelligent Systems"],
		specsFilename="info/test/specializations.txt",
		courseFilename="info/test/fullcourses.txt",
		useTaken=True,
		takenFilename="info/test/taken.txt"
	)
	# scheduling
	L, bestBound = CourseScheduling(graph, specsTable, creditsPerQuarter, startQ, defaultUnits).findBestSchedule(5)

	printResult(L, bestBound, startQ, creditsPerQuarter)


"""
Taking 16 credits per quarter:
year 1 quarter 1: ['WRITING39A', 'MATH2A', 'I&CSCI90', 'I&CSCI31']
year 1 quarter 2: ['I&CSCI6B', 'WRITING39B', 'MATH2B', 'IN4MATX131']
year 1 quarter 3: ['I&CSCI32', 'I&CSCI51', 'I&CSCI6D']
year 2 quarter 1: ['WRITING39C', 'STATS67', 'MATH3A', 'I&CSCI33']
year 2 quarter 2: ['I&CSCI53+53L', 'COMPSCI178', 'I&CSCI45C']
year 2 quarter 3: ['IN4MATX43', 'COMPSCI132', 'COMPSCI177', 'COMPSCI122A']
year 3 quarter 1: ['COMPSCI184A', 'COMPSCI169', 'COMPSCI151', 'I&CSCI46']
year 3 quarter 2: ['I&CSCI139W', 'COMPSCI125', 'IN4MATX113', 'COMPSCI133']
year 3 quarter 3: ['COMPSCI154', 'GEIV-3', 'GEVIII-1', 'GEII-2']
year 4 quarter 1: ['IN4MATX121', 'COMPSCI161', 'COMPSCI171', 'GEIV-2']
year 4 quarter 2: ['COMPSCI175', 'GEII-1', 'GEVI-1', 'GEVII-1']
year 4 quarter 3: ['GEIV-1']
7
"""
