
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
		self.courseValue = None

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
			spec=self.satSpecs, upp=self.isUpperOnly)


	def delPrereq(self, cname, sat):
		for i in range(len(self.prereq)):
			if cname in self.prereq[i]:
				if sat:
					del self.prereq[i]
					del self.prereqBool[i]
				else:
					self.prereq[i].remove(cname)
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

	def getNeighbors(self):
		"""
		:return: all its prereqs
		"""

		return [i for pset in self.prereq for i in pset]



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
		isTagged = False
		for i in range(len(self.prereq)):
			if not self.prereqBool[i]:
				if name in self.prereq[i]:
					self.prereqBool[i] = name
					isTagged = True
		return isTagged

	def prereqIsSatisfied(self):
		return all(self.prereqBool)

	def isValidQuarter(self, quarter):
		return quarter % 6 in self.quarters

