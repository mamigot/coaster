import time
from scrapy import Spider, Request, log

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from utils.sql import get_session, handlers
from utils.sql.models.course import Course

from edx_bot.spiders import EdXLoggerIn


class EdXCourseDownloader(Spider):
    '''
    Provided a link to a course, it downloads its content (sections,
    subsections, units and videos --for videos, it queries YouTube and
    retrives popularity-oriented statistics).
    '''
    name = 'course_downloader'
    allowed_domains = ['edx.org', 'youtube.com', 'googleapis.com']
    session = None

    def start_requests(self):
        self.session = get_session()
        self.edx_logger = EdXLoggerIn()

        # Get courses that haven't been crawled yet and register for them
        for c in self.session.query(Course).filter(Course.crawled_on == None):
            yield Request(
                url = c.href,
                meta = {'db_course': Course},
                callback = self.register_for_course)


    def register_for_course(self, response):
        '''
        Registers for course (or checks that it has been registered) before
        sending it to be crawled. Discards courses that are not in English
        or problematic.
        '''
        course_homepage_url = response.url

        driver = self.edx_logger.driver
        driver.maximize_window()
        driver.get(course_homepage_url)
        # Space requests out by 2 seconds
        time.sleep(2)

        try:
            enroll_or_open_button_xpath = \
                '//*[@id="course-info-page"]/header/div/div/div[3]/div/div/a'
            enroll_or_open_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, enroll_or_open_button_xpath)))

            if enroll_or_open_button.text == "Enroll Now":
                if self.course_is_in_english(driver):
                    enroll_or_open_button.click()
                    # Allow enough time for edX to process the registration
                    time.sleep(6)

                    if driver.current_url != course_homepage_url:
                        msg = "Enrolled into course with url=%s" % (course_homepage_url)
                        log.msg(msg, level=log.INFO)
                    else:
                        msg = "Trouble enrolling into course with url=%s. Discarding." % (course_homepage_url)
                        log.msg(msg, level=log.ERROR)
                        return None
                else:
                    msg = "Course with url=%s is not in English. Discarding." % (course_homepage_url)
                    log.msg(msg, level=log.INFO)
                    return None

            else:
                msg = "Was already enrolled into course with url=%s" % (course_homepage_url)
                log.msg(msg, level=log.INFO)

        except TimeoutException:
            msg = "TimeoutException for course with url=%s. Discarding." % (course_homepage_url)
            log.msg(msg, level=log.ERROR)
            return None


        # SCRAPE THE COURSE'S CONTENTS... Request(url=..., callback=...)
        return None


    def course_is_in_english(self, driver):
        '''
        Provided a driver that's at the course's homepage (i.e.
        driver.current_url = course_homepage_url), returns True
        if the course is in English.
        '''
        description_elements = driver.find_elements_by_xpath(
            '//*[@id="course-summary-area"]/ul/li')

        for e in description_elements:
            if 'Languages: English' in e.text:
                return True

        return False


    def crawl_course(self, response):
        '''
        if course is current, etc.:
            go to courseware page

        sections = []
        for s in section_elements:
            sections.append(self.crawl_section(s))

        # create course item and add sections to it
        '''


    def crawl_section(self, response):
        '''
        subsections = []
        for s in subsection_elements:
            subsections.append(self.crawl_subsection(s))

        # create section items and add subsections to it
        '''
        pass


    def crawl_subsection(self, response):
        '''
        units = []
        for u in unit_elements:
            units.append(self.crawl_unit(u))
        '''
        pass


    def crawl_unit(self, response):
        '''
        description = ...
        videos = []
        for v in video_elements:
            add youtube stats to v
        '''
        pass


    def get_youtube_stats(self, video_href):
        '''
        identify youtube_id from link and call the API

        return stats in a dictionary
        '''
        pass


    def closed(self, reason):
        self.session.close()
        self.edx_logger.close()
