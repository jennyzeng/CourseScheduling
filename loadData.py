from Course import Course, CoursesGraph
from WebSoc import WebSoc
import re
class DataLoading:

	def __init__(self):
		self.websoc = WebSoc()
	def loadCourses(graph: CoursesGraph, prereqFileName="info/test/courses.txt"):
		with open(prereqFileName,'r') as f:
			for line in f:
				info = line.strip().split(";")
				graph.addCourse(info[0], Course(name=info[1], prereq=eval(info[2]),
				                                units=int(info[3]), quarters=eval(info[4])))

	def loadSpec(major = "Computer Science", specs=['Intelligent Systems'], filename = "info/test/spec.txt"):
		hashTable = {}
		hashTable2= {}
		with open(filename) as f:
			first = f.readline().strip()
			if first != major:
				return
			content = f.read().split(";")
			for spec in content:
				spec = spec.strip().split('\n')
				if spec[0] not in specs:
					continue
				hashTable[spec[0]] = [] # store Course nums set for each spec
				hashTable2[spec[0]] = [] # store the corresponding require num for that course nums set
				i = 1

				while i < len(spec):
					if re.match("^(all)$|^([1-9][0-9]*)$", spec[i]):
						hashTable[spec[0]].append(set())
						hashTable2[spec[0]].append(spec[i])
						i+=2 # skip {

					elif spec[i] == "}":
						# change keys at end
						if hashTable2[spec[0]][-1]=="all":
							hashTable2[spec[0]][-1] = len(hashTable[spec[0]][-1])
						else:
							hashTable2[spec[0]][-1] = eval(hashTable2[spec[0]][-1] )
						i+=1

					else:
						hashTable[spec[0]][-1].add(spec[i].replace(" ",""))
						i+=1


		return hashTable, hashTable2







if __name__ == "__main__":
	# graph = CoursesGraph()
	# DataLoading.loadCourses(graph)
	# graph.updateSatisfies()
	# print(graph)
	print(DataLoading.loadSpec())
