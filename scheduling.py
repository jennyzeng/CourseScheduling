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


def iniQueue(graph: CoursesGraph):
	"""
	it will put all the courses without prereq to deque and return the deque
	"""
	queue = deque()

	for name, course in graph.getCourses():
		if not course.hasPrereq():
			queue.append(name)

	return queue

def expandQueue(Q, graph, course):
	# add those courses that are satisfied into the Q
	satisfies = graph.tagSatisfy(course)
	for sat in satisfies:
		if graph[sat].prereqIsSatisfied():
			Q.append(sat)

# def widthFunc(level):
# 	return len(level) == 2

def lastAccpetedLevel(L, course):
	"""
	after expanding L, last level of L is accepted for course
	"""
	while True:  # find highest avail quarter
		if not course.isValidQuarter(len(L)-1):
			L.append([])
		else:
			return
def clearEmptyLevels(L):
	while L and not L[-1]:
		L.pop()

def courseScheduling(graph, widthFunc):
	# initialize my queue
	Q = iniQueue(graph)

	if not Q: return None
	L = [[]]  # output
	while Q:
		cur = Q.popleft()

		# if the highest level has dependents, it has to be assigned to a new level
		for v in L[-1]:
			if graph.isPrereq(v, cur):
				# find highest avail quarter
				L.append([])
				lastAccpetedLevel(L, graph[cur])
				L[-1].append(cur)
				assigned = True
				break
		else:  # it means that the highest level does not has cur's dependents
			step = len(L) - 2
			assigned = False
			if widthFunc(L[-1], graph[cur]):  # highest level is full, should add a new level
				L.append([])
			lastAccpetedLevel(L, graph[cur])
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
				if not widthFunc(L[step], graph[cur]) and graph[cur].isValidQuarter(step):
					# if step is not full and cur will be offered this quarter, this is a possible level
					lastStep = step
			step -= 1
		if not assigned:
			L[lastStep].append(cur)
		expandQueue(Q, graph, cur)
	clearEmptyLevels(L)
	return L

def addGEs(L, GEgraph, widthFunc):
	step = 0
	for name, ge in GEgraph.getCourses():
		while step < len(L):
			if widthFunc(L[step], ge):
				step += 1
			else:
				L[step].append(name)
				break
		else:
			L.append([name])




if __name__ == "__main__":
	adjList = {
		"a": Course(units=4.0, quarter=[0], prereq=[]),
		"b": Course(units=4.0, quarter=[1], prereq=[{"a"}]),
		"c": Course(units=2.0, quarter=[1, 2], prereq=[{"b"}]),
		"d": Course(units=1.5, quarter=[1, 2], prereq=[{"a", "c"}, {"k", "e"}]),  # k is not in the adjList
		"e": Course(units=3.5, quarter=[1, 2], prereq=[]),
		"f": Course(units=2.0, quarter=[1, 2], prereq=[{"a", "c"}])
	}
	graph = CoursesGraph(adjList)
	graph.updateSatisfies()
	# print(iniQueue(graph))
	print(courseScheduling(graph, widthFunc))
