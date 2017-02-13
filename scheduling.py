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


class CourseScheduling:
	def __init__(self, graphList, SpecsTable):
		self.L = [[]]
		# self._widthFunc = widthFunc
		self.graphList = graphList
		self.totalUnits = 0  # total units assigned
		self.specsTable = SpecsTable

	def widthFunc(self, level, courseUnit):
		theSum = courseUnit
		for c in level:
			for graph in self.graphList:
				if graph[c]:
					theSum += graph[c].units
					break

		return theSum > 16

	def iniQueue(self, graph: CoursesGraph):
		"""
		it will put all the courses without prereq to deque and return the deque
		"""
		Q = deque()
		Q2 = deque()
		for name, course in graph.getCourses():
			if not course.hasPrereq():
				if self.courseConditions(course):
					Q.append(name)
				else:
					Q2.append(name)
		return Q, Q2

	def expandQueue(self, Q, Q2, graph, course):
		# add those courses that are satisfied into the Q
		satisfies = graph.tagSatisfy(course)
		for sat in satisfies:
			if graph[sat].prereqIsSatisfied():
				if self.courseConditions(graph[sat]):
					Q.append(sat)
				else:
					Q2.append(sat)

	def lastAccpetedLevel(self, course):
		"""
		after expanding L, last level of L is accepted for course
		"""
		while True:  # find highest avail quarter
			if not course.isValidQuarter(len(self.L) - 1):
				self.L.append([])
			else:
				return

	def clearEmptyLevels(self):
		while self.L and not self.L[-1]:
			self.L.pop()

	def multiGraphScheduling(self):
		# L = [[]]
		for graph in self.graphList:
			self.L = self.courseScheduling(graph)
		return self.L

	def courseConditions(self, course: Course):
		bools = True
		for condi in course.condition:
			if condi == 'UPPERDIVISIONST':
				bools = bools and self.totalUnits > 90.0
			elif condi == 'LOWERDIVISIONWRITING':
				bools = bools and sum([s for s in self.specsTable["Writing"]])==0  # all satisfyied
		return bools

	def courseScheduling(self, graph: CoursesGraph):
		# initialize my queue
		Q, Q2 = self.iniQueue(graph)
		# Q2 is the queue for special conditions

		while Q:
			cur = Q.popleft()
			while Q and not self.courseConditions(graph[cur]):
					Q.append(cur)
					cur = Q.pop()

			# check if satisfy specifications
			satSpecs = graph[cur].getSpecs()  # {('Lower-division', 1)}
			remain = False
			for specName, index in satSpecs:
				if self.specsTable[specName][index] > 0:
					remain = True
					self.specsTable[specName][index] -= 1
			if not remain:  # this course is not required
				continue

			# if the highest level has dependents, it has to be assigned to a new level
			for v in self.L[-1]:
				if graph.isPrereq(v, cur):
					# find highest avail quarter
					self.L.append([])
					self.lastAccpetedLevel(graph[cur])
					self.L[-1].append(cur)
					assigned = True
					break
			else:  # it means that the highest level does not has cur's dependents
				step = len(self.L) - 2
				assigned = False
				if self.widthFunc(self.L[-1], graph[cur].units):  # highest level is full, should add a new level
					self.L.append([])
				self.lastAccpetedLevel(graph[cur])
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
					if not self.widthFunc(self.L[step], graph[cur].units) and graph[cur].isValidQuarter(step):
						# if step is not full and cur will be offered this quarter, this is a possible level
						lastStep = step
				step -= 1
			if not assigned:
				self.L[lastStep].append(cur)
			self.expandQueue(Q,Q2, graph, cur)
			self.totalUnits += graph[cur].units
		self.clearEmptyLevels()
		return self.L

	# if __name__ == "__main__":
	# adjList = {
	# 	"a": Course(units=4.0, quarter=[0], prereq=[]),
	# 	"b": Course(units=4.0, quarter=[1], prereq=[{"a"}]),
	# 	"c": Course(units=2.0, quarter=[1, 2], prereq=[{"b"}]),
	# 	"d": Course(units=1.5, quarter=[1, 2], prereq=[{"a", "c"}, {"k", "e"}]),  # k is not in the adjList
	# 	"e": Course(units=3.5, quarter=[1, 2], prereq=[]),
	# 	"f": Course(units=2.0, quarter=[1, 2], prereq=[{"a", "c"}])
	# }
	# graph = CoursesGraph(adjList)
	# graph.updateSatisfies()
	# print(iniQueue(graph))
	# print(courseScheduling(graph, widthFunc))
