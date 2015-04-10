import json
from scrapy import Spider, Request

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from edx_bot.spiders import EdXLoggerIn
from edx_bot.items import CourseItem, SubjectItem, InstructorItem, InstitutionItem
from edx_bot.spiders.config import EDX_LOGIN, EDX_PASSWORD


class EdxCourseFinder(Spider):
    '''
    Fetch a list of the courses on edX and register for them
    '''

    name = 'edx_course_finder'
    allowed_domains = ['edx.org']
    edx_search_url = 'https://www.edx.org/search/api/all'


    def start_requests(self):
        # Fetch cookies by calling self.edx_account_logger.get_sign_in_cookies()
        self.edx_logger = EdXLoggerIn()
        return [Request(url=self.edx_search_url, callback=self.parse)]


    def parse(self, response):
        js = json.loads(response.body_as_unicode())

        for course_info in js:
            subjects = []
            if course_info['subjects']:
                subjects = [SubjectItem(name=s) for s in course_info['subjects']]

            instructors = []
            if course_info['staff']:
                for i in range(len(course_info['staff'])):
                    instructors.append(
                        InstructorItem(
                            edx_nid = course_info['staff-nids'][i],
                            name = course_info['staff'][i],
                        )
                    )

            course = CourseItem(
                edx_guid = course_info['guid'],
                edx_code = course_info['code'],
                name = course_info['l'],
                href = course_info['url'],
                availability = course_info['availability'],
                start = course_info['start'],
            )

            institution = InstitutionItem(name = course_info['schools'][0])

            course['institution'] = dict(institution)
            course['subjects'] = [dict(s) for s in subjects]
            course['instructors'] = [dict(i) for i in instructors]

            yield self.course_register(course)


    def course_register(self, course):
        print "\n\n\nTOPOPTPOTPOTPOTPOT\n\n\n\n"
        #self.edx_logger.get_signin_cookies()
        return course


    def closed(self, reason):
        self.edx_logger.delete_signin_cookies()
