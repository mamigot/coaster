import time, json
from scrapy import Spider, Request, log

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from edx_bot.spiders import EdXLoggerIn
from edx_bot.items import CourseItem, SubjectItem, InstructorItem, InstitutionItem
from edx_bot.spiders.config import EDX_LOGIN, EDX_PASSWORD

from utils.sql import get_session, handlers
from utils.sql.models.course import Course


class EdxCourseFinder(Spider):
    '''
    Fetch a list of the courses on edX and register for them.
    '''
    name = 'course_finder'
    allowed_domains = ['edx.org']
    edx_search_url = 'https://www.edx.org/search/api/all'
    session = None

    def start_requests(self):
        self.session = get_session()
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
        # No need to register for the course if it's already in the database
        if handlers.get(self.session, Course, Course.edx_guid, course['edx_guid']):
            msg = "Not parsing course with edx_guid=%s because it's in the DB." \
                % (str(course['edx_guid']))
            log.msg(msg, level=log.INFO)
            return course

        msg = "Parsing course with edx_guid=%s" % (str(course['edx_guid']))
        log.msg(msg, level=log.INFO)

        driver = self.edx_logger.driver
        driver.get(course['href'])
        driver.maximize_window()
        # Space requests out by 2 seconds
        time.sleep(2)

        # Look for element that suggests that we are already enrolled in
        # the course. If it doesn't exist, then register.
        try:
            courseware_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="course-info-page"]/header/div/div/div[3]/div/div/a'))
                )

            # Reject course if the language is not English
            try:
                language = driver.find_element_by_xpath(
                    '//*[@id="course-summary-area"]/ul/li[6]/span[2]').text

                if language != "English":
                    msg = "Rejected course with (edx_guid, url)=(%s, %s) " \
                        " its language is not English" % \
                            (str(course['edx_guid']), course['href'])
                    log.msg(msg, level=log.WARNING)
                    return None

            except:
                msg = "Rejected course with (edx_guid, url)=(%s, %s) because " \
                    "its language could not be determined" % \
                        (str(course['edx_guid']), course['href'])
                log.msg(msg, level=log.WARNING)

                return None


        except TimeoutException, NoSuchElementException:
            try:
                enroll_button = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="course-info-page"]/header/div/div/div[3]/div/div/a'))
                    )
                enroll_button.click()

                msg = "Enrolled into course with edx_guid=%s" % (str(course['edx_guid']))
                log.msg(msg, level=log.INFO)
                
            except TimeoutException:
                msg = "Timed out when enrolling into course with edx_guid=%s" \
                    % (str(course['edx_guid']))
                log.msg(msg, level=log.WARNING)


        msg = "Returned course with edx_guid=%s to the pipelines." \
            % (str(course['edx_guid']))
        log.msg(msg, level=log.INFO)
        return course


    def closed(self, reason):
        self.session.close()
        self.edx_logger.close()
