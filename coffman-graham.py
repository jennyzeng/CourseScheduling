from directedGraphRepresentation import DirectedGraph
from collections import Counter, deque



def widthFunc(level):
	return len(level) == 2

def coffman_graham(graph, widthFunc):
	"""
	in this function, vertices' dependents are unknown,
	we only know the neighbors of vertices
	"""
	# get topological Order
	tp = topologicalOrder(graph)
	L = [[]]    # output
	while tp:
		cur = tp.popleft()
		# if the highest level has dependents, it has to be assigned to a new level
		for v in L[-1]:
			if cur in graph.getNeighbors(v):
				L.append([cur])
				assigned = True
				break
		else: # it means that the highest level does not has cur's dependents
			step = len(L)-2
			assigned = False
			if widthFunc(L[-1]): #highest level is full, should add a new level
				L.append([])
			lastStep = len(L)-1 # last step is an accepted level for cur
		# start to check from the second highest level to the lowest
		# if cur's dependents are in the current step, it will be added to the closest
		# accepted step (last step)
		while not assigned and step >= 0:

			if not widthFunc(L[step]):# only check those levels that are not full
				for v in L[step]:# check if there are dependents in this level
					if cur in graph.getNeighbors(v): # there are dependents in this level
						L[lastStep].append(cur) # it cannot be assigned to a higher level
						assigned = True
						break
				else:
					lastStep = step
			step -= 1
		if not assigned:
			L[lastStep].append(cur)
	return L







"""
Suppose we have tasks A and B, with all their dependencies already ordered in our list and we have to pick which one is going to come next. From A’s dependencies, we take the one most recently placed in the ordering and we check if it comes before or after the most recently placed task from B’s dependencies. If it comes before, then we choose A, if it comes after then we chose B. If it turns out A and B’s most recently placed dependency is actually the same task that both depend on, we look at the next most recent dependency etc. This way, by picking the next task as the one whose closest dependency is the furthest away, at every step we space out dependencies in our ordering as much as possible.
"""


def topologicalOrder(graph: DirectedGraph):
	C = deque()  # collection of vertices with no incoming edges
	# D is dictionary mapping each vertex to a number,
	# the # of incoming edges that come from vertices that have not yet
	# been output. Initially D[v] = total # of incoming edges to v
	D = Counter()
	for v in graph.getVertices():
		D[v]
		for w in graph.getNeighbors(v):
			D[w] += 1
	for v in graph.getVertices():
		if D[v] == 0:
			C.append(v)

	output = deque()
	while C:  # happen <= n times because n vertices
		vertex = C.popleft()
		output.append(vertex)
		for w in graph.getNeighbors(vertex):  # happen <= m times
			D[w] -= 1
			if D[w] == 0:
				C.append(w)
	if len(output) == len(graph):
		return output
	else:
		# print(output)
		return False  # not acyclic


graph = DirectedGraph()
graph.addEdges(
	[("a", "b"), ("a", "e"), ("a", "c"), ("b", "c"), ("c", "d"), ("c", "e"), ("c", "f"), ("d", "f"), ("e", "f"),
	 ("e", "g")])
# print(topologicalOrder(graph))  # ['a', 'b', 'c', 'e', 'd', 'g', 'f']
graph2 = DirectedGraph()
graph2.addEdges(
	[("a", "b"), ("a", "e"), ("a", "c"), ("b", "c"), ("c", "d"), ("c", "e"), ("c", "f"), ("d", "f"), ("e", "f"),
	 ("e", "g"), ("c", "b")])  # ['a', 'b', 'c', 'e', 'd', 'g', 'f']

# print(topologicalOrder(graph2))

print(coffman_graham(graph, widthFunc))
print(coffman_graham(graph2, widthFunc))