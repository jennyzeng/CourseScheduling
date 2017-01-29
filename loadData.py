from Course import Course, CoursesGraph
from WebSoc import WebSoc

class DataLoading:
	# def __init__(self, graph, prereqFileName="info/test/prereqs.txt"
	#              #specFileName="info/test/spec.txt",
	#              #coursesFileName="info/text/courses.txt"
	#              ):
	#
	# 	self.loadPrereq(prereqFileName)
	# 	# self.spec = self.loadSpec(specFileName)
	# 	# self.courses = self.loadCourses(coursesFileName)
	def __init__(self):
		self.websoc = WebSoc()
	def loadPrereq(graph: CoursesGraph, prereqFileName="info/test/courses.txt"):
		try:
			file = open(prereqFileName, 'r')
		except:
			print("prereq file %s not exists" % prereqFileName)
			return
		for line in file:
			info = line.strip().split(";")
			graph.addCourse(info[0], Course(name=info[1], prereq=eval(info[2]), units=int(info[3]), quarters=eval(info[4])))

	def loadSpec(self, specFileName):
		pass

	def loadCourses(self, coursesFileName):
		pass


if __name__ == "__main__":
	graph = CoursesGraph()
	DataLoading.loadPrereq(graph)
	graph.updateSatisfies()
	print(graph)
