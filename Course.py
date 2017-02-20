from datetime import time

"""
a course will have the name, teaching time(start time, end time),
the quarter it will be offered, its units, prerequisite, and the courses that it may partially satisfy their prerequisites
it is assumed that it will be offered at the same quarter for every year

for weekday: 1-5: represents Mon-Fri
for quarter: 1-3: represents Fall-Spring

I should also show the AND/OR relationship in prereq
cs 161 prereq:
( I&C SCI 23 ( min grade = C ) OR CSE 23 ( min grade = C ) OR I&C SCI H23 ( min grade = C ) OR I&C SCI 46 ( min grade = C ) OR CSE 46 ( min grade = C ) )
AND
I&C SCI 6B
AND
I&C SCI 6D
AND
( MATH 2B OR AP CALCULUS BC ( min score = 4 ) )
some courses, such as AP xxx, if they are not in the courses list, we can simply ignore it
when we are scheduling



Some thoughts:
1. What about the discussion/lab class? should I ignore the time conflict at the current stage?
2. I think currently I may only focus on:
 a. the quarter they are offered,
 b. prereq relationship,
 c. units
"""
weekDayCode = {"M": 0, "Tu": 1, "W": 2, "Th": 3, "F": 4}


class Course:
	def __init__(self, name, isUpperOnly=None, units=None, quarters=None, prereq=None, satisfy=None):
		self.name = name
		self.quarters = quarters if quarters else {}
		self.units = units if units else None
		self.prereq = prereq if prereq else []
		self.satisfy = satisfy if satisfy else set()
		self.prereqBool = [None] * len(self.prereq)
		self.satSpecs = set()
		self.isUpperOnly = isUpperOnly

	def __str__(self):
		return "name: {name}\n" \
		       "units: {units}\n" \
		       "quarters: {quar}\n" \
		       "prereq: {prereq}\n" \
		       "satisfyCourse: {sat}\n" \
		       "satisfySpec:{spec}\n" \
		       "upperOnly: {upp}".format(
			name=self.name, units=self.units,
			quar=self.quarters, prereq=self.prereq, sat=self.satisfy,
			spec=self.satSpecs,upp=self.isUpperOnly)

	def addQuarter(self, quarter):
		self.quarters.update(quarter)

	# def setWeekdaysInWebSoc(self, days):
	# 	i = 0
	# 	while i < len(days):
	# 		code = weekDayCode.get(days[i])
	# 		if code != None:
	# 			self.weekdays.append(code)
	# 			i += 1
	# 		else:
	# 			code = weekDayCode.get(days[i:i + 2])
	# 			self.weekdays.append(code)
	# 			i += 2

	def addPrereq(self, prereq):
		self.prereq.append(prereq)

	def addSatisfy(self, satisfy):
		self.satisfy.add(satisfy)

	def addSpec(self, spec, num):
		self.satSpecs.add((spec, num))  # spec is a tuple

	def getSpecs(self):
		return self.satSpecs

	def getPrereq(self):
		return self.prereq

	def hasPrereq(self):
		return len(self.prereq) != 0

	def getSatisfy(self):
		return self.satisfy

	def isPrereq(self, name):
		return name in self.prereqBool

	def tagPrereq(self, name):
		"""tag the prereq section that are satisfied by the course 'name'
		if the prereq section is not yet satisfied, it will tag 'name' to be
		the satisfied course and return True. else, return False
		"""

		for i in range(len(self.prereq)):
			if not self.prereqBool[i]:
				if name in self.prereq[i]:
					self.prereqBool[i] = name
					return True
		return False

	def prereqIsSatisfied(self):
		return all(self.prereqBool)

	# def conflict(self, course):
	# 	"""time conflict of two courses"""
	# 	return False

	def isValidQuarter(self, quarter):
		return quarter % 3 in self.quarters


class CoursesGraph:
	def __init__(self, adjList=None):
		self.adjList = adjList if adjList else dict()

	def __str__(self):
		return "\n".join(
			"{name}: \n{course}".format(name=name, course=course) for name, course in self.adjList.items()) + "\n"

	def __contains__(self, item):
		return item in self.adjList

	def __getitem__(self, item):
		return self.adjList.get(item)

	def __setitem__(self, key, value):
		self.adjList[key] = value

	def mergeGraph(self, graph):
		self.adjList.update(graph.adjList)

	def loadFromExcel(self, fileName):
		pass

	def addCourse(self, name, course):
		"""
		add vertex
		"""
		if name not in self.adjList:
			self[name] = course
			return True
		return False

	def delCourse(self, name):
		return self.adjList.pop(name)

	def addCourses(self, courses):
		"""
		add vertices
		courses is an adjList
		"""
		for name, course in courses.items():
			self.addCourse(name, course)

	def addPrereq(self, name, prereqSet):
		"""
		this could only be called after all courses are added into the adjList.
		add edge
		a prereqSet is like: {"I&C SCI 45C", "I&C SCI 45J"}
		"""
		if name in self.adjList:
			self[name].addPrereq(prereqSet)
			return True
		return False

	def updateSatisfies(self):
		for name, course in self.adjList.items():
			for preq in course.getPrereq():
				for sat in preq:
					if sat in self.adjList:
						self[sat].addSatisfy(name)

	def addSpec(self, name, spec, num):
		if name in self:
			self[name].addSpec(spec, num)
			return True
		else:
			return False

	def loadSpecs(self, SpecsCourse):
		for spec, courseSetList in SpecsCourse.items():
			for i in range(len(courseSetList)):
				for c in courseSetList[i]:
					self.addSpec(c, spec, i)
		return

	def getCourses(self):
		"""
		:return: a list of course names
		"""
		return self.adjList.items()

	def getCourse(self, name):
		return self[name]

	def getCoursePrereqs(self, name):
		if name in self.adjList:
			return self[name].getPrereq()
		return None

	def getCourseSatisfies(self, name):
		if name in self.adjList:
			return self[name].getSatisfy()
		return None

	def isPrereq(self, dependent, course):
		return self[course].isPrereq(dependent)

	def tagSatisfy(self, course):
		"""
		tag those courses that this course can satisfy and return list of courses"""
		L = []
		for sat in self[course].getSatisfy():
			tag = self[sat].tagPrereq(course)
			if tag:
				L.append(sat)
		return L


if __name__ == "__main__":
	compsci161 = Course("DES&ANALYS OF ALGO")
	print(compsci161)

# SampleAdjList = {"COMPSCI 161": Course(quarter=[1, 2, 3],
#                                        units=4.0,
#                                        startTime=time(11, 00),
#                                        endTime=time(11, 50),
#                                        weekdays=[1, 3, 5],
#                                        prereq=[{"I&C SCI 23", "CSE 23", "I&C SCI H23", "I&C SCI 46", "CSE 46"},
#                                                {"I&C SCI 6B"}, {"I&C SCI 6D"},
#                                                {"MATH 2B", "AP CALCULUS BC"}]),
#                  "I&C SCI 46": Course(quarter=[1, 2, 3],
#                                       units=4.0,
#                                       startTime=time(10, 00),
#                                       endTime=time(11, 20),
#                                       weekdays={2, 4},
#                                       prereq=[{"I&C SCI 45C", "I&C SCI 45J"}],
#                                       satisfy={"COMPSCI 161"})
#                  }
# adjList = {
# 	"a": Course(units=4.0, quarters={0}, prereq=[]),
# 	"b": Course(units=4.0, quarters={1}, prereq=[{"a"}]),
# 	"c": Course(units=2.0, quarters={1, 2}, prereq=[{"b"}]),
# 	"d": Course(units=1.5, quarters={1, 2}, prereq=[{"a", "c"}, {"k"}, {"e"}]),  # k is not in the adjList
# 	"e": Course(units=3.5, quarters={1, 2}, prereq=[])
# }
# graph = CoursesGraph(adjList)
# # print(graph)
# graph.updateSatisfies()
# print(graph)

"""
expected output form for course schedule:
[["a", "e"], ["b","c"],["d"]]
"""
