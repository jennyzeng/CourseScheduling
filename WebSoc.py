from bs4 import BeautifulSoup
import requests
from Course import Course


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
		self.quarterCode = {0:"2016-92",1:"2017-03",2:"2016-14"}

	# def setYearTerm(self, yearTerm):
	# 	self.formData["YearTerm"] = yearTerm
	# 	self.quarter = int(input("please change quarter correspondingly"))

	def getInfoByCourseNum(self, YearTerm, Dept, CourseNum):
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
				if L[1] == "Lec":# get units
					return L[3]
		return None
	def writeFile(self, readfilename, outfilename, dept):
		readfile = open(readfilename,'r')
		writefile = open(outfilename, 'w')
		for line in readfile:
			info = line.split(";")
			CourseNum = info[0][len(dept.replace(" ", "")):]
			print("writing "+dept + CourseNum)
			quarters=set()
			unit = None
			for key, val in self.quarterCode.items():
				print("searching term "+str(key))
				info = self.getInfoByCourseNum(val, dept, CourseNum)
				if info:
					quarters.add(key)
					unit = info
			if unit:
				writefile.write(line.strip() + ";" + unit + ";"+str(quarters)+"\n")
		readfile.close()
		writefile.close()
	def forSingleCourse(self, dept, CourseNum):
		quarters = set()
		unit = None
		for key, val in self.quarterCode.items():
			print("searching term " + str(key))
			info = self.getInfoByCourseNum(val, dept, CourseNum)
			if info:
				quarters.add(key)
				unit = info
		if unit:
			print(";"+unit+";"+str(quarters))
if __name__ == "__main__":
	websoc = WebSoc()
	# websoc.writeFile("info/test/", "COMPSCI")
	# websoc.writeFile("info/test/", "STATS")
	# websoc.writeFile("info/test/I&CSCI.txt","info/test/fullI&CSCI.txt", "I&C SCI")
	# websoc.writeFile("info/test/", "MATH")
	# websoc.writeFile("info/test/", "IN4MATX")
	websoc.forSingleCourse("I&C SCI", "51")