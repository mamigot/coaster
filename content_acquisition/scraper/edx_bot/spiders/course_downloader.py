import time
from scrapy import Spider, Request, log

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from utils.sql import get_session, handlers
from utils.sql.models.course import Course

from edx_bot.spiders import EdXLoggerIn
from edx_bot.items import CourseItem, CourseSectionItem, CourseSubsectionItem \
    CourseUnitItem, CourseVideoItem


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
        '''
        # Get courses that haven't been crawled yet and register for them
        for c in self.session.query(Course).filter(Course.crawled_on == None):
            yield Request(
                url = c.href,
                callback = self.register_for_course
            )
        TESTING TESTING TESTING'''
        yield Request(
            url = 'https://www.edx.org/course/signals-systems-part-1-iitbombayx-ee210-1x',
            callback = self.register_for_course
        )


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

        return Request(
            url = course_homepage_url,
            callback = self.crawl_course,
            dont_filter=True
        )


    def crawl_course(self, response):
        driver = self.edx_logger.driver
        driver.maximize_window()
        driver.get(response.url)

        if self.course_is_accessible(driver):
            '''
            Go to the courseware page
            '''
            pass

        else:
            return None

        '''
        initialize section and subsection items
        with former's names and latter's names and links
        '''
        course_nav_elements = driver.find_elements_by_xpath(
            '//*[@id="accordion"]/nav'
        )
        sections = []
        for section in course_nav_elements:
            '''
            initialize section
            initialize list of subsections

            crawl each subsection
            '''
            pass
        '''
        assemble sections into course item and return it
        '''


    def crawl_subsection(self, response):
        '''
        build unit elements as long as they're video-oriented
        '''
        pass


    def crawl_unit(self, response):
        '''
        description = ...
        videos = []
        for v in video_elements:
            add youtube stats to v

            get transcript if possible
            (if not possible through scrapy (and response.body), use
            the requests library)
        '''
        pass


    def get_youtube_stats(self, video_href):
        '''
        identify youtube_id from link and call the API

        return stats in a dictionary
        '''
        pass


    def course_is_in_english(self, driver):
        '''
        Provided a driver that's at the course's homepage (i.e.
        driver.current_url = course_homepage_url), returns True
        if the course is in English.
        '''
        description_elements = driver.find_elements_by_xpath(
            '//*[@id="course-summary-area"]/ul/li'
        )

        for e in description_elements:
            if 'Languages: English' in e.text:
                return True

        return False


    def course_is_accessible(self, driver):
        '''
        Provided a driver that's at the course's homepage, returns
        True if the course is currently accessible. Otherwise,
        returns False (possibly because the course hasn't started yet, etc.).
        '''
        pass


    def closed(self, reason):
        self.session.close()
        self.edx_logger.close()
