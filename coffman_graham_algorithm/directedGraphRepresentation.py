
from collections import defaultdict


class DirectedGraph:
	def __init__(self):
		self.adjList = defaultdict(set)
	def __contains__(self, item):
		return item in self.adjList

	def createFromDict(self, d):
		self.adjList = defaultdict(set, d)

	def addVertex(self, vertex):
		if vertex not in self.adjList:
			self.adjList.update({vertex: set()})
			return True
		else:
			return False

	def addVertices(self, vertices):
		for v in vertices:
			self.addVertex(v)

	def addEdge(self, edge: tuple):
		self.adjList[edge[0]].add(edge[1])
		self.adjList[edge[1]] = set()

	def addEdges(self, edges):
		for edge in edges:
			self.addEdge(edge)

	def reverse(self):
		reversed = DirectedGraph()
		for v in self.getVertices():
			for w in self.getNeighbors(v):
				reversed.addEdge((w, v))
		return reversed

	def getVertices(self):
		return [v for v in self.adjList]

	def getNeighbors(self, vertex):
		neighbors = self.adjList.get(vertex)
		if not neighbors:
			return []
		else:
			return neighbors

	def edgeExist(self, edge):
		return edge[1] in self.adjList[edge[0]]

	def __str__(self):
		return str(self.adjList)

	def __len__(self):
		return len(self.adjList)


