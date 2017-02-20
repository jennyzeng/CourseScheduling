from Course import Course, CoursesGraph
from collections import deque
from math import ceil
import copy


class CourseScheduling:
	upperUnits = 90

	def __init__(self, graphList, SpecsTable, unitPerQ):
		self.graphList = graphList
		self.specsTable = SpecsTable
		self.totalUnits = 0
		self.unitPerQ = unitPerQ
		self.upperLevel = ceil(self.upperUnits / self.unitPerQ) - 1  # -1 for zero indexing

	def widthFunc(self, level, courseUnit):
		total = courseUnit
		for c in level:
			total += self._findCourse(c).units
		return total > self.unitPerQ

	def findBestSchedule(self, boundRange):
		L = None
		bestBound = None
		for bound in range(self.upperLevel, self.upperLevel + boundRange):
			self._resetGraphs()
			self.totalUnits = 0
			specsTable = copy.deepcopy(self.specsTable)
			curSchedule = self.multiGraphScheduling(specsTable, bound)

			if self._isValidSchedule(curSchedule):
				if not L or len(L) > len(curSchedule):
					L = curSchedule
					bestBound = bound
		if not L: raise Exception("cannot get a valid schedule")
		return L, bestBound

	def multiGraphScheduling(self, specsTable, upperBound):
		L = [[]]
		for graph in self.graphList:
			self.courseScheduling(L, graph, specsTable, upperBound)
		return L

	def courseScheduling(self, L, graph: CoursesGraph, specsTable, upperBound):
		# initialize queue
		Q = self._iniQueue(graph)
		while Q:
			cur = Q.popleft()

			# check if satisfy specializations
			if not self._checkSpec(cur, graph, specsTable):
				continue

			# if the highest level has dependents, it has to be assigned to a new level
			assigned = self._highestLevelDependents(cur, graph, L, upperBound)

			if not assigned:  # it means that the highest level does not have cur's dependents
				step = len(L) - 2
				if self.widthFunc(L[-1], graph[cur].units):  # highest level is full, should add a new level
					L.append([])
				self._lastAccpetedLevel(graph[cur], L, upperBound)

				lastStep = len(L) - 1  # highest step is an accepted level for cur

			# start to check from the second highest level to the lowest
			# if cur's dependents are in the current step, it will be added to the closest
			# accepted step (last step)
			while not assigned and step >= 0:

				for v in L[step]:  # check if there are dependents in this level
					if graph.isPrereq(v, cur):  # there are dependents in this level
						L[lastStep].append(cur)  # it cannot be assigned to a higher level
						assigned = True
						break
				else:
					if graph[cur].isUpperOnly and step < upperBound:
						# upper standing only, cannot assign to a lower one
						L[lastStep].append(cur)
						assigned = True
						break

					elif not self.widthFunc(L[step], graph[cur].units) and graph[cur].isValidQuarter(step):
						# if step is not full and cur will be offered this quarter, this is a possible level
						lastStep = step
				step -= 1

			if not assigned:
				L[lastStep].append(cur)
			self._expandQueue(Q, graph, cur)
			self.totalUnits += graph[cur].units

		self._clearEmptyLevels(L)
		return L


	def _resetGraphs(self):
		for graph in self.graphList:
			graph.resetGraph()


	def _isValidSchedule(self, L):
		total = 0
		for step in range(len(L)):
			levelTotal = 0
			for cname in L[step]:
				course = self._findCourse(cname)
				if course.isUpperOnly and total < self.upperUnits:
					return False
				levelTotal += course.units
			total += levelTotal
		return True


	def _iniQueue(self, graph: CoursesGraph):
		"""
		it will put all the courses without prereq to deque and return the deque
		"""
		Q = deque()
		for name, course in graph.getCourses():
			if not course.hasPrereq():
				Q.append(name)

		return Q


	def _expandQueue(self, Q, graph, course):
		# add those courses that are satisfied into the Q
		satisfies = graph.tagSatisfy(course)
		for sat in satisfies:
			if graph[sat].prereqIsSatisfied():
				Q.append(sat)


	def _lastAccpetedLevel(self, course, L, bound):
		"""
		after expanding L, last level of L is accepted for course
		"""
		# find highest avail quarter
		if course.isUpperOnly:
			while len(L) - 1 < bound:
				L.append([])

		while not course.isValidQuarter(len(L) - 1):
			L.append([])
		return L


	def _clearEmptyLevels(self, L):
		while L and not L[-1]:
			L.pop()
		return L


	def _isUpperLevel(self, levelIndex):
		return


	def _checkSpec(self, cur, graph, specsTable):
		# check if satisfy specializations
		satSpecs = graph[cur].getSpecs()  # {('Lower-division', 1)}
		remain = False
		for specName, index in satSpecs:
			if specsTable[specName][index] > 0:
				remain = True
				specsTable[specName][index] -= 1
		return remain  # this course is not required if remain=False


	def _highestLevelDependents(self, cur, graph, L, bound):
		# if the highest level has dependents, it has to be assigned to a new level
		for v in L[-1]:
			if graph.isPrereq(v, cur):
				# find highest avail quarter
				L.append([])
				self._lastAccpetedLevel(graph[cur], L, bound)
				L[-1].append(cur)
				return True  # cur is assigned
		return False


	def _findCourse(self, course):
		for g in self.graphList:
			if course in g:
				return g[course]
		else:
			raise Exception("course not exist")
