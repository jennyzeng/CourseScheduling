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

def iniQueue(graph:CoursesGraph):
	"""
	it will put all the courses without prereq to deque and return the deque
	"""
	queue = deque()

	for name, course in graph.getCourses():
		if not course.hasPrereq():
			queue.append((name, course))

	for c in queue:
		graph.delCourse(c[0])
	return queue

def widthFunc(level):
	return len(level) == 2

def courseScheduling(graph, widthFunc):
	queue = iniQueue(graph)
	schedule = []
	while queue:
		curCourse = queue.popleft()
		if not schedule or widthFunc(schedule[-1]): # add a higher level
			schedule.append([])
		# one level lower than its prepreqs
		schedule[-1].append(curCourse)
		# delete the requirement in the satisfying course
		satisfySet = curCourse[1].getSatisfy()
		for sat in satisfySet:
			satCourse = graph.getCourse(sat)
			if satCourse in graph and satCourse.delPrereq(curCourse[0]):# no prereq anymore
				queue.append((sat, satCourse))
				graph.delCourse(sat)

	return schedule



if __name__ == "__main__":
	adjList = {
		"a": Course(units=4.0, quarter=[1], prereq=[]),
		"b": Course(units=4.0, quarter=[2], prereq=[{"a"}]),
		"c": Course(units=2.0, quarter=[2, 3], prereq=[{"b"}]),
		"d": Course(units=1.5, quarter=[2, 3], prereq=[{"a", "c"}, {"k","e"}]),  # k is not in the adjList
		"e": Course(units=3.5, quarter=[2, 3], prereq=[])
	}
	graph = CoursesGraph(adjList)
	graph.updateSatisfies()
	# print(iniQueue(graph))
	print(courseScheduling(graph, widthFunc))