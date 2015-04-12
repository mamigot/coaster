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
        course_homepage_url = response.url

        driver = self.edx_logger.driver
        driver.maximize_window()
        driver.get(course_homepage_url)

        try:
            enroll_or_open_button_xpath = \
                '//*[@id="course-info-page"]/header/div/div/div[3]/div/div/a'
            enroll_or_open_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, enroll_or_open_button_xpath)))

            if enroll_or_open_button.text == "Enroll Now":
                if self.course_is_in_english(driver):
                    enroll_or_open_button.click()
                    time.sleep(6)
                    msg = "Enrolled for course with url=%s" % (course_homepage_url)
                else:
                    raise
            else:
                msg = "Was already enrolled for course with url=%s" % (course_homepage_url)

            log.msg(msg, level=log.INFO)
            time.sleep(2)

        except TimeoutException:
            msg = "Course with url=%s deemed INVALID." % (course_homepage_url)
            log.msg(msg, level=log.WARNING)

        return None


    def course_is_in_english(self, driver):
        '''
        Provided a driver that's at the course's homepage, returns True
        if the course is in English.
        '''
        description_elements = driver.find_elements_by_xpath(
            '//*[@id="course-summary-area"]/ul/li')

        for e in description_elements:
            if e.text == 'Languages: English':
                return True

        return False


    def crawl_course(self, response):
        '''
        assemble all course data (yield full course)
        '''
        print "\n\nSUP SON\n\n"
        print response.url
        course = response.meta['db_course']
        print course.__mapper__.columns.__dict__


    def crawl_section(self, response):
        pass


    def crawl_subsection(self, response):
        pass


    def crawl_unit(self, response):
        pass


    def get_youtube_stats(self, video_id):
        pass


    def closed(self, reason):
        self.session.close()
        self.edx_logger.close()
