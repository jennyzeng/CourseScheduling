import unittest
from Course import Course
from WebSoc import WebSoc
# class testCourse(unittest.TestCase):
#
# 	def setUp(self):
# 		self.course = Course("DES&ANALYS OF ALGO")
# 	#
	# def testSetWebSocInfo(self):
	#
	# 	self.course.setWebSocInfo(
	# 	)
	# 	self.assertEqual(self.course.weekdays, [0,2,4])
	# 	print(self.course)


class testWebSoc(unittest.TestCase):
	def setUp(self):
		self.websoc = WebSoc()

	def testGetInfoByCourseNum(self):
		self.assertEqual(self.websoc.getInfoByCourseNum("COMPSCI", "161"),
		                 {"quarter":1,"units":4})

if __name__ == '__main__':
    unittest.main()