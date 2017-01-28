import scrapy
import re
import urllib.parse


class csCourseSpider(scrapy.Spider):
	name = "courses"

	def start_requests(self):
		url = "https://www.reg.uci.edu/cob/prrqcgi?"
		departments = ["WRITING"]
		info = {'action': 'view_all', 'term': 201703, 'dept': None}

		for de in departments:
			info['dept'] = de
			self.log(de)
			curRequest = scrapy.Request(url=url + urllib.parse.urlencode(info), callback=self.parse)
			curRequest.meta['department'] = de.replace(" ", "")
			yield curRequest

	def parse(self, response):
		self.log(response.meta['department'])
		filename = response.meta['department']+".txt"
		with open(filename, 'a') as f:
			for row in response.css("table[width='800'] tr"):
				try:
					ID = response.meta['department'] + row.css("td[class='course'] a").xpath('@name').extract()[-1]
					cname = row.css("td[class='title']::text").extract()[-1].strip()
					prereq = getPrereqs(row.css("td[class='prereq']").extract()[-1])
					f.write(ID + ";" + cname + ";" + str(prereq) + '\n')
				except:
					pass
		self.log('Saved file %s' % filename)


def getPrereqs(prereq):
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
			if course not in ['UPPERDIVISIONST' ,'INGONLY','BETTERseeSOCcommentsforrepeatpolicy'] and '='not in course\
					and not course.startswith("AP") and not course.startswith('NO') and not course.startswith('PLACEMENT'):
				orSet.add(course)
		if orSet: output.append(orSet)
	return output
# scrapy crawl courses
