from math import ceil
import copy
import heapq


class CourseScheduling:
	upperUnits = 90

	def __init__(self, graph, SpecsTable, unitPerQ,startQ, defaultUnits):
		self.graph = graph
		self.specsTable = SpecsTable
		self.unitPerQ = unitPerQ
		self.upperLevel = ceil((self.upperUnits-defaultUnits) / self.unitPerQ) - 1  # -1 for zero indexing
		if self.upperLevel<0: self.upperLevel=0
		self.startQ = startQ

	def widthFunc(self, level, courseUnit):
		total = courseUnit
		for c in level:
			total += self.graph[c].units
		return total > self.unitPerQ

	def findBestSchedule(self, boundRange):
		L = None
		bestBound = None
		for bound in range(self.upperLevel, self.upperLevel + boundRange):
			self._resetGraph()
			specsTable = copy.deepcopy(self.specsTable)
			curSchedule = self.courseScheduling([[]], specsTable, bound)

			if self._isValidSchedule(curSchedule, specsTable):
				if not L or len(L) > len(curSchedule):
					L = curSchedule
					bestBound = bound
		if not L: raise Exception("cannot get a valid schedule")
		return L, bestBound

	def courseScheduling(self, L, specsTable, upperBound):
		# initialize heap
		Q = self._iniHeap(specsTable)
		while Q:
			cur = heapq.heappop(Q)[1]
			# check if satisfy specializations
			if not self._checkSpec(cur, specsTable):
				continue

			# if the highest level has dependents, it has to be assigned to a new level
			assigned = self._highestLevelDependents(cur, L, upperBound)

			if not assigned:  # it means that the highest level does not have cur's dependents
				step = len(L) - 2
				if self.widthFunc(L[-1], self.graph[cur].units):  # highest level is full, should add a new level
					L.append([])
				self._lastAccpetedLevel(self.graph[cur], L, upperBound)

				lastStep = len(L) - 1  # highest step is an accepted level for cur

			# start to check from the second highest level to the lowest
			# if cur's dependents are in the current step, it will be added to the closest
			# accepted step (last step)
			while not assigned and step >= 0:

				for v in L[step]:  # check if there are dependents in this level
					if self.graph.isPrereq(v, cur):  # there are dependents in this level
						L[lastStep].append(cur)  # it cannot be assigned to a higher level
						assigned = True
						break
				else:
					if self.graph[cur].isUpperOnly and step < upperBound:
						# upper standing only, cannot assign to a lower one
						L[lastStep].append(cur)
						assigned = True
						break

					elif not self.widthFunc(L[step], self.graph[cur].units) \
							and self.graph[cur].isValidQuarter(step+self.startQ):
						# if step is not full and cur will be offered this quarter, this is a possible level
						lastStep = step
				step -= 1

			if not assigned:
				L[lastStep].append(cur)
			self._expandQueue(Q, cur, specsTable)

		self._clearEmptyLevels(L)
		return L

	def _resetGraph(self):
		self.graph.resetGraph()

	def _isValidSchedule(self, L, specsTable):
		total = 0
		if any( any(i) for i in specsTable.values()): return False
		for step in range(len(L)):
			levelTotal = 0
			for cname in L[step]:
				course = self.graph[cname]
				if course.isUpperOnly and total < self.upperUnits:
					return False
				levelTotal += course.units
			total += levelTotal
		return True

	def _iniHeap(self, specsTable):
		"""
		it will put all the courses without prereq to deque and return the deque
		"""
		Q = []
		for name, course in self.graph.getCourses():
			courseValue = self.graph.courseValue(course, specsTable)
			if not course.hasPrereq() and courseValue:
				heapq.heappush(Q,(courseValue, name))
			# Q.append(name)

		return Q

	def _expandQueue(self, Q, course, specsTable):
		# add those courses that are satisfied into the Q
		satisfies = self.graph.tagSatisfy(course)
		for sat in satisfies:
			courseValue = self.graph.courseValue(self.graph[sat], specsTable)
			if self.graph[sat].prereqIsSatisfied() and courseValue:
				heapq.heappush(Q, (courseValue, sat))
			# Q.append(sat)

	def _lastAccpetedLevel(self, course, L, bound):
		"""
		after expanding L, last level of L is accepted for course
		"""
		# find highest avail quarter
		if course.isUpperOnly:
			while len(L) - 1 < bound:
				L.append([])

		while not course.isValidQuarter(len(L)+self.startQ - 1):
			L.append([])
		return L

	def _clearEmptyLevels(self, L):
		while L and not L[-1]:
			L.pop()
		return L

	def _checkSpec(self, cur, specsTable):
		# check if satisfy specializations
		satSpecs = self.graph[cur].getSpecs()  # {('Lower-division', 1)}
		remain = False
		for specName, index in satSpecs:
			if specsTable[specName][index] > 0:
				remain = True
				specsTable[specName][index] -= 1
		return remain  # this course is not required if remain=False

	def _highestLevelDependents(self, cur, L, bound):
		# if the highest level has dependents, it has to be assigned to a new level
		for v in L[-1]:
			if self.graph.isPrereq(v, cur):
				# find highest avail quarter
				L.append([])
				self._lastAccpetedLevel(self.graph[cur], L, bound)
				L[-1].append(cur)
				return True  # cur is assigned
		return False
