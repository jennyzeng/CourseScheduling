from bs4 import BeautifulSoup
import requests
import urllib.parse
import re


class WebSoc:
	url = "https://www.reg.uci.edu/perl/WebSoc"

	def __init__(self):
		self.formData = {
			"YearTerm": "2017-03",
			"ShowComments": "on",
			"ShowFinals": "on",
			"Breadth": "ANY",
			"Dept": "COMPSCI",
			"CourseNum": "",
			"Division": "ANY",
			"CourseCodes": "",
			"InstrName": "",
			"CourseTitle": "",
			"ClassType": "ALL",
			"Units": "",
			"Days": "",
			"StartTime": "",
			"EndTime": "",
			"MaxCap": "",
			"FullCourses": "ANY",
			"FontSize": 100,
			"CancelledCourses": "Exclude",
			"Bldg": "",
			"Room": "",
			"Submit": "Display Web Results"
		}
		self.quarterCode = {0: "2016-92", 1: "2017-03", 2: "2016-14"}
		self.reqURL = "https://www.reg.uci.edu/cob/prrqcgi?"
		self.prereqInfo = {'action': 'view_all', 'term': 201703, 'dept': None}
		self.depts = []

	def main(self, depts, filename):
		for dept in depts:
			print("----------------------------")
			print("writing depts: ", dept)
			lines = self.makeDeptPrereqRequest(dept)
			self._writeDeptCouresInfo(dept, lines, filename)


	def makeDeptPrereqRequest(self, dept):
		self.prereqInfo['dept'] = dept
		url = self.reqURL + urllib.parse.urlencode(self.prereqInfo)
		resp = requests.get(url)
		return BeautifulSoup(resp.content, "lxml"
		                     ).find_all(
			class_=["course", "title", "prereq"])

	def _DBwriteDeptCouresInfo(self, dept, lines):
		# db = MySQLdb.connect(host='localhost', user='root', passwd='Jenny186200@', db='CS-h198')
		# cursor = db.cursor()
		# cursor.execute("")
		pass
	def _writeDeptCouresInfo(self, dept, lines, filename):
		with open(filename,'a') as f:
			for i in range(0, len(lines), 3):
				CourseNum, title, prereqs, condition = self._extractInfoFromLine(lines[i:i + 3])
				units, quarters = self._getMatchingUnitAndQuarter(dept, CourseNum)
				if quarters:
					f.write(dept.replace(" ","") +";"+CourseNum + ";"+title+";"+str(prereqs) +
					        ";" + units + ";" + str(quarters) + ";" + str(condition) +"\n")
					print("wrote course", dept, CourseNum)

	def _extractInfoFromLine(self, info):
		num = info[0].a['name']
		title = [i for i in info[1].stripped_strings][0]
		prereqs,condition = self._getPrereqs(info[2].get_text(""))
		return num, title, prereqs, condition

	def _getMatchingUnitAndQuarter(self, dept, CourseNum):
		quarters = set()
		units = None
		for key, val in self.quarterCode.items():
			temp = self._getInfoByCourseNum(val, dept, CourseNum)
			if temp:
				quarters.add(key)
				units = temp
		if quarters:
			return units, quarters
		else:
			return None, None

	def _getPrereqs(self, prereq):
		condition = set()
		prereq = re.sub('</*b>|<br>|\\r|\\n|<.*?td.*?>', "", prereq).strip()
		if "AND" in prereq:
			L = prereq.split("AND")
		else:
			L = [prereq]
		output = []
		for ors in L:
			courses = ors.split("OR")
			orSet = set()
			for course in courses:
				course = re.sub("\(|\)| (\( min grade.*?\))| (\( min score.*?\))|(coreq)|( )|(recommended)",
				                "", course).replace("&amp;", "&").replace("coreq", "")
				# add upper division standing
				if course in [ 'UPPERDIVISIONST','ENTRYLEVELWRITING','LOWERDIVISIONWRITING']:
					condition.add(course)

				elif course not in [ 'INGONLY', 'BETTERseeSOCcommentsforrepeatpolicy'] \
						and '=' not in course and not course.startswith("AP") and \
						not course.startswith('NO') and not course.startswith(
					'PLACEMENT'):
					orSet.add(course)
			if orSet: output.append(orSet)
		return output, condition

	def _getInfoByCourseNum(self, YearTerm, Dept, CourseNum):
		"""currently I am only getting the quarters and units
		['34260', 'Lec', 'A', '4', 'HIRSCHBERG, D.', 'MWF  10:00-10:50', 'PCB 1100', 'Mon, Mar 20, 10:30-12:30pm','246', '157 / 173', 'n/a', '309', 'A', 'Bookstore', 'Web', 'OPEN']
		"""
		formData = self.formData.copy()
		formData.update({"CourseNum": CourseNum, "Dept": Dept, "YearTerm": YearTerm})
		resp = requests.post(self.url, data=formData)
		soup = BeautifulSoup(resp.content, "lxml")
		lines = soup.find_all(valign="top")

		# get info list
		if lines and [i for i in lines[0].stripped_strings][0].endswith(CourseNum):
			for line in lines[1:]:
				L = [i for i in line.stripped_strings]
				if L[1] == "Lec" or L[1] == "Sem":  # get units
					return L[3]
		return None


	def forSingleCourse(self, dept, CourseNum):
		quarters = set()
		unit = None
		for key, val in self.quarterCode.items():
			print("searching term " + str(key))
			info = self._getInfoByCourseNum(val, dept, CourseNum)
			if info:
				quarters.add(key)
				unit = info
		if unit:
			print(";" + unit + ";" + str(quarters))


if __name__ == "__main__":
	websoc = WebSoc()
	# websoc.main(["I&C SCI", "COMPSCI","MATH","STATS", "IN4MATX"], "fullcourses.txt")
	websoc.main(["POL SCI"], "fullcourses.txt")