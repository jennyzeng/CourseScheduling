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

	def courseValue(self, cname, specsTable):
		course = self.adjList[cname]
		if course.courseValue:
			return self.adjList[cname].courseValue
		# total = 0
		# for spec, num in course.satSpecs:
		# 	if specsTable[spec][num] != 0:
		# 		total -= 1

		self.adjList[cname].courseValue = -len(self.adjList[cname].satSpecs)
		return self.adjList[cname].courseValue

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

	def delCourse(self, cname, sat):
		for course in self[cname].satisfy:
			if self[course]:
				self[course].delPrereq(cname, sat)
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
		required = set()
		for spec, courseSetList in SpecsCourse.items():
			for i in range(len(courseSetList)):
				for c in courseSetList[i]:
					self.addSpec(c, spec, i)
					required.add(c)
		# clear not required course
		for cname in list(self.adjList.keys()):
			if cname not in required:
				self.delCourse(cname, False)
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
			if self[sat]:
				tag = self[sat].tagPrereq(course)
				if tag:
					L.append(sat)
		return L
