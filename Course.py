from datetime import time

"""
a course will have info about:
 - the name,
 - the quarter it will be offered,
 - its units, prerequisite,
 - if it is upperstanding only
 -  the courses that it may partially satisfy their prerequisites

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


"""


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
	@property
	def courseValue(self):
		return -(len(self.satSpecs) + len(self.satisfy))

	def delPrereq(self, cname):
		for i in range(len(self.prereq)):
			if cname in self.prereq[i]:
				del self.prereq[i]
				del self.prereqBool[i]
				return True
		return False

	def resetCourse(self):
		self.prereqBool = [None] * len(self.prereq)

	def addQuarter(self, quarter):
		self.quarters.update(quarter)

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

	def values(self):
		return self.adjList.values()

	def delUpper(self):
		for cname in self.adjList:
			self.adjList[cname].isUpperOnly = False

	def courseValue(self, course, specsTable):
		total = 0
		for spec, num in course.satSpecs:
			if specsTable[spec][num]!= 0:
				total -= 1

		for c in course.satisfy:
			if self[c]:
				for spec, num in self[c].satSpecs:
					total -= 0.1 if specsTable[spec][num] > 0 else 0
					break
		return total



	def resetGraph(self):
		for course in self.adjList.values():
			course.resetCourse()

	def mergeGraph(self, graph):
		self.adjList.update(graph.adjList)

	def addCourse(self, name, course):
		"""
		add vertex
		"""
		if name not in self.adjList:
			self[name] = course
			return True
		return False

	def delCourse(self, cname):
		for sat in self[cname].satisfy:
			if self[sat]:
				self[sat].delPrereq(cname)
		self.adjList.pop(cname)

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


