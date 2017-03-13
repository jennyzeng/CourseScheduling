from Course import Course
from CoursesGraph import CoursesGraph
import re


class DataLoading:
	def __init__(self):
		pass

	def loadWidthFuncTable(self,filename):
		wdict= {}
		with open(filename, 'r') as f:
			for line in f:
				line = line.strip().split(":")
				if line[0]=="else":
					wdict["else"] = int(line[1])
				else:
					wdict[int(line[0])] = int(line[1])
		return wdict

	def loadCourses(self, graph: CoursesGraph, prereqFileName):
		with open(prereqFileName, 'r') as f:
			for line in f:
				info = line.strip().split(";")
				graph.addCourse("".join(info[0:2]), Course(name=info[2], prereq=eval(info[3]),
				                                           units=int(info[4]), quarters=eval(info[5]),
				                                           isUpperOnly=eval(info[6])))

	def loadSpec(self, major, specs, filename):
		hashTable = {}
		hashTable2 = {}
		with open(filename) as f:
			first = f.readline().strip()
			if first != major:
				return
			content = f.read().split(";")
			for spec in content:
				spec = spec.strip().split('\n')
				if spec[0] not in specs:
					continue
				hashTable[spec[0]] = []  # store Course nums set for each spec
				hashTable2[spec[0]] = []  # store the corresponding require num for that course nums set
				i = 1

				while i < len(spec):
					if re.match("^(all)$|^([1-9][0-9]*)$", spec[i]):
						hashTable[spec[0]].append(set())
						hashTable2[spec[0]].append(spec[i])
						i += 1  # skip {

					elif spec[i] == "}":
						# change keys at end
						if hashTable2[spec[0]][-1] == "all":
							hashTable2[spec[0]][-1] = len(hashTable[spec[0]][-1])
						elif hashTable2[spec[0]][-1] == "recommend":  # TODO: need modify later
							hashTable2[spec[0]][-1] = len(hashTable[spec[0]][-1]) // 2
						else:
							hashTable2[spec[0]][-1] = eval(hashTable2[spec[0]][-1])
						i += 1
					elif "{" in spec[i]:
						i+=1
					else:
						hashTable[spec[0]][-1].add(spec[i].replace(" ", ""))
						i += 1

		return hashTable, hashTable2

	def loadTaken(self, graph, specsTable, filename):
		with open(filename) as f:
			startQ = int(f.readline())
			totalUnits = int(f.readline())
			for cname in f.readlines():
				cname = cname.replace(" ", "").strip()
				course = graph[cname]
				if course:
					for specName, index in course.getSpecs():
						if specsTable[specName][index] > 0:
							specsTable[specName][index] -= 1
					graph.delCourse(cname,True)
		if totalUnits >= 90:
			graph.delUpper()
		return startQ, totalUnits

	def loadAvoid(self, graph, filename):
		with open(filename) as f:
			for cname in f.readlines():
				cname = cname.replace(" ", "").strip()
				course = graph[cname]
				if course:
					graph.delCourse(cname, False)



if __name__ == "__main__":
	# graph = CoursesGraph()
	# DataLoading.loadCourses(graph)
	# graph.updateSatisfies()
	# print(graph)
	print(DataLoading().loadSpec(major="Computer Science",
	                           specs=["Lower-division", "Upper-division", "Intelligent Systems"],
	                           filename="info/specializations.txt"))
