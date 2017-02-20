"""

1. create a graph for courses,( assuming that there is no AND/OR relation currently) and
	clean up the graph so that only direct dependencies are represented. 

2. make a topological list for those courses, tracing the prerequisite
  so it will start from those courses that would satisfy nothing to make a topological order.

   Suppose we have tasks A and B, with all their dependencies already ordered in our list
   and we have to pick which one is going to come next.
  From A’s dependencies, we take the one most recently placed in the ordering and we check
  if it comes before or after the most recently placed task from B’s dependencies. If it
  comes before, then we choose A, if it comes after then we chose B. If it turns out A and
   B’s most recently placed dependency is actually the same task that both depend on, we
   look at the next most recent dependency etc.

3. Assign the vertices of G to levels in the reverse of the topological ordering constructed
in the previous step. For each vertex v, add v to a level that is at least one step higher
than the highest level of any outgoing neighbor of v, that does not already have W elements
 assigned to it, and that is as low as possible subject to these two constraints.

note:
- Each step is a quarter, and since I use 1, 2, 3(or 0,1,2) to represent Fall, Winter, Spring, using i
 to represent the ith step, I can do 3 mod i to determine the quarter of that step.
 If that course is available in that step, I will add the course to a level as high as possible.

- the width of a step w can be easily modified to be a constraint for maximum number of units in a quarter.

- if I want to add the time for the courses, and if courses are conflicting, I will have to find
	a way to decide which course could remain in the current step, and which one will be moved to
	the next possible step.

- This method will assigning all courses into the schedule. I will solve this problem later

"""
from Course import Course, CoursesGraph
from collections import deque
from math import ceil


class CourseScheduling:
	upperUnits = 90

	def __init__(self, graphList, SpecsTable, unitPerQ):
		self.L = [[]]
		# self._widthFunc = widthFunc
		self.graphList = graphList
		self.levelUnits = [0]  # total units assigned
		self.specsTable = SpecsTable
		self.totalUnits = 0
		self.unitPerQ = unitPerQ
		self.upperLevel = ceil(self.upperUnits / self.unitPerQ)-1 # -1 for zero indexing


	def multiGraphScheduling(self):
		# L = [[]]
		for graph in self.graphList:
			self.L = self.courseScheduling(graph, self.upperLevel)
		return self.L, self.specsTable

	def widthFunc(self, level, courseUnit):
		theSum = courseUnit
		for c in level:
			for graph in self.graphList:
				if graph[c]:
					theSum += graph[c].units
					break

		return theSum > self.unitPerQ

	def _iniQueue(self, graph: CoursesGraph):
		"""
		it will put all the courses without prereq to deque and return the deque
		"""
		Q = deque()
		Q2 = deque()
		for name, course in graph.getCourses():
			if not course.hasPrereq():
				if not course.isUpperOnly:
					Q.append(name)
				else:
					Q2.append(name)
		return Q, Q2

	def _expandQueue(self, Q, Q2, graph, course):
		# add those courses that are satisfied into the Q
		satisfies = graph.tagSatisfy(course)
		for sat in satisfies:
			if graph[sat].prereqIsSatisfied():
				if graph[sat].isUpperOnly and self.totalUnits < self.upperUnits:
					Q2.append(sat)
				else:
					Q.append(sat)

	def _lastAccpetedLevel(self, course):
		"""
		after expanding L, last level of L is accepted for course
		"""
		# find highest avail quarter
		if course.isUpperOnly:
			while len(self.L)-1 < self.upperLevel:
				self.L.append([])

		while not course.isValidQuarter(len(self.L) - 1):
			self.L.append([])
		return

	def _clearEmptyLevels(self):
		while self.L and not self.L[-1]:
			self.L.pop()

	def _isUpperLevel(self, levelIndex):
		return

	def _checkSpec(self, cur, graph):
		# check if satisfy specializations
		satSpecs = graph[cur].getSpecs()  # {('Lower-division', 1)}
		remain = False
		for specName, index in satSpecs:
			if self.specsTable[specName][index] > 0:
				remain = True
				self.specsTable[specName][index] -= 1
		return remain  # this course is not required if remain=False

	def _highestLevelDependents(self, cur, graph):
		# if the highest level has dependents, it has to be assigned to a new level
		for v in self.L[-1]:
			if graph.isPrereq(v, cur):
				# find highest avail quarter
				self.L.append([])
				self._lastAccpetedLevel(graph[cur])
				self.L[-1].append(cur)
				return True  # cur is assigned
		return False

	def courseScheduling(self, graph: CoursesGraph, upperBound):
		# initialize my queue
		Q, Q2 = self._iniQueue(graph)
		# Q2 is the queue for special conditions
		while Q or Q2:
			if self.totalUnits > self.upperUnits and Q2:
				cur = Q2.popleft()
			elif Q:
					cur = Q.popleft()
			else:
				raise Exception("Cannot assign all")

			# check if satisfy specializations
			if not self._checkSpec(cur, graph):
				continue

			# if the highest level has dependents, it has to be assigned to a new level
			assigned = self._highestLevelDependents(cur, graph)

			if not assigned:  # it means that the highest level does not have cur's dependents
				step = len(self.L) - 2
				if self.widthFunc(self.L[-1], graph[cur].units):  # highest level is full, should add a new level
					self.L.append([])
				self._lastAccpetedLevel(graph[cur])

				lastStep = len(self.L) - 1  # highest step is an accepted level for cur

			# start to check from the second highest level to the lowest
			# if cur's dependents are in the current step, it will be added to the closest
			# accepted step (last step)
			while not assigned and step >= 0:

				for v in self.L[step]:  # check if there are dependents in this level
					if graph.isPrereq(v, cur):  # there are dependents in this level
						self.L[lastStep].append(cur)  # it cannot be assigned to a higher level
						assigned = True
						break
				else:
					if graph[cur].isUpperOnly and step < upperBound: # upper standing only, cannot assign to a lower one
						self.L[lastStep].append(cur)
						assigned = True
						break

					elif not self.widthFunc(self.L[step], graph[cur].units) and graph[cur].isValidQuarter(step):
						# if step is not full and cur will be offered this quarter, this is a possible level
						lastStep = step
				step -= 1

			if not assigned:
				self.L[lastStep].append(cur)
			self._expandQueue(Q,Q2, graph, cur)
			self.totalUnits += graph[cur].units
		self._clearEmptyLevels()
		return self.L

	def _findCourse(self, course):
		for g in self.graphList:
			if course in g:
				return g[course]
		else: raise Exception("course not exist")

	def isValidSchedule(self, L):
		total = 0
		for step in range(1, len(L)):
			for cname in self.L[step]:
				course = self._findCourse(cname)
				if course.isUpperOnly and total < self.upperUnits:
					return False
				total += course.units
		return True


