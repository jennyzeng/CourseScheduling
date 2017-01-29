import scrapy


class csCourseSpider(scrapy.Spider):
	name = "courseInfo"

	def start_requests(self):
		url = "https://www.reg.uci.edu/perl/WebSoc"
		formData = {
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
