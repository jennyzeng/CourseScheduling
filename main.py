from Course import Course, CoursesGraph
from scheduling import *
from loadData import DataLoading


def loadData(major, specs, specsFilename, courseFilename, useTaken, takenFilename, useAvoid, avoidFilename):
	specsCourse, specsTable = DataLoading().loadSpec(
									major=major, specs=specs, filename=specsFilename)
	graph = CoursesGraph()
	DataLoading().loadCourses(graph, courseFilename)
	graph.loadSpecs(specsCourse)
	graph.updateSatisfies()

	defaultUnits = 0
	startQ = 0
	if useTaken:
		startQ, defaultUnits= DataLoading().loadTaken(graph, specsTable, takenFilename)
	if useAvoid:
		DataLoading().loadAvoid(graph, avoidFilename)

	return graph, specsTable, defaultUnits, startQ



def printResult(L, bestBound, startQ, creditsPerQuarter):
	print("start quarter: ", startQ)
	print("Taking %d credits per quarter: " % (creditsPerQuarter))
	for i, level in enumerate(L):
		i = i + startQ
		print("year %d quarter %d:" % (i // 3 + 1, i % 3 + 1), level)

	print("best upper bound: year %d quarter %d" % (bestBound // 3 + 1, bestBound % 3 + 1))


if __name__ == '__main__':
	creditsPerQuarter = 20
	# data loading
	## for Computer Science graph
	graph, specsTable, defaultUnits, startQ = loadData(
		major="Computer Science",
		specs=["University",
			 "GEI", "GEII", "GEIII", "GEIV", "GEV", "GEVI","GEVII","GEVIII",
		       "Lower-division",
		       "Upper-division",
		       "Algorithms",
		       "Intelligent Systems"
		       # "Visual Computing"
		       #"Information"
		       ],
		specsFilename="info/test/specializations.txt",
		courseFilename="info/test/fullcourses.txt",
		useTaken=False,
		takenFilename="info/test/taken.txt",
		useAvoid=False,
		avoidFilename="info/test/avoid.txt"
	)
	# scheduling
	L, bestBound = CourseScheduling(graph, specsTable, creditsPerQuarter, startQ, defaultUnits).findBestSchedule(5)
	printResult(L, bestBound, startQ, creditsPerQuarter)


"""
start quarter:  0
Taking 17 credits per quarter:
year 1 quarter 1: ['I&CSCI31', 'I&CSCI6B', 'MATH2A', 'WRITINGLOW1', 'I&CSCI90']
year 1 quarter 2: ['I&CSCI32', 'MATH2B', 'I&CSCI51']
year 1 quarter 3: ['I&CSCI33', 'I&CSCI6D', 'STATS67', 'MATH3A']
year 2 quarter 1: ['I&CSCI45C', 'COMPSCI151', 'HISTORY40A', 'POLSCI21A']
year 2 quarter 2: ['I&CSCI46', 'HISTORY40B', 'COMPSCI122A', 'COMPSCI178']
year 2 quarter 3: ['HISTORY40C', 'COMPSCI143A', 'COMPSCI132', 'IN4MATX43']
year 3 quarter 1: ['COMPSCI161', 'COMPSCI112', 'COMPSCI171', 'COMPSCI141']
year 3 quarter 2: ['COMPSCI116', 'I&CSCI53+53L', 'WRITINGLOW2']
year 3 quarter 3: ['COMPSCI165', 'GEII-1', 'GEIII-1', 'GEIII-2']
year 4 quarter 1: ['COMPSCI113', 'GEVI-1', 'GEVII-1', 'GEVIII-1']
year 4 quarter 2: ['I&CSCI139W']
best upper bound: year 2 quarter 3
"""
