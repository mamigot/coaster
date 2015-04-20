import time
from collections import OrderedDict

from scrapy import Spider, Request, log
from scrapy.selector import Selector

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException

from utils.sql import get_session
from utils.sql.models.course import Course

from edx_bot.spiders import EdXLoggerIn
from edx_bot.items import CourseItem, CourseSectionItem, CourseSubsectionItem, \
    CourseUnitItem, CourseVideoItem


class GeneralCoursewareSpider(Spider):
    '''
    Provided a link to a course, it downloads its content (sections,
    subsections, units and videos --for videos, it queries YouTube and
    retrives popularity-oriented statistics).
    '''
    name = 'general_course_content_spider'
    allowed_domains = ['edx.org', 'youtube.com']
    session = None

    def start_requests(self):
        self.session = get_session()
        self.edx_logger = EdXLoggerIn()
        self.edx_logger.driver.maximize_window()

        # Get courses that haven't been crawled yet and register for them
        for c in self.session.query(Course).filter(Course.last_crawled_on == None):
            yield Request(
                url = c.href,
                meta = {'course_edx_guid':c.edx_guid},
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
            meta = response.meta,
            callback = self.crawl_course,
            dont_filter=True
        )


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


    def access_course(self, driver, course_homepage_url):
        '''
        Provided a driver that's at the course's homepage, returns the
        button to open the course if it's accessible, and None otherwise.
        '''
        try:
            open_button_xpath = \
                '//*[@id="course-info-page"]/header/div/div/div[3]/div/div/a'
            open_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, open_button_xpath)))

            if open_button.text == "Open Course":
                msg = "May access course with url=%s" % (course_homepage_url)
                log.msg(msg, level=log.INFO)

                open_button.click()
                time.sleep(6)

                courseware_xpath = '//*[@id="content"]/nav/div/ol/li[1]/a'
                courseware_button = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, courseware_xpath)))

                courseware_button.click()
                time.sleep(2)

                if driver.current_url != course_homepage_url:
                    msg = "Opened course with url=%s" % (course_homepage_url)
                    log.msg(msg, level=log.INFO)

                else:
                    msg = "Trouble opening course with url=%s. Discarding." % (course_homepage_url)
                    log.msg(msg, level=log.ERROR)
                    raise

            else:
                msg = "Cannot access course with url=%s. Says: '%s'" % \
                    (course_homepage_url, open_button.text)
                log.msg(msg, level=log.INFO)
                raise

        except TimeoutException:
            msg = "TimeoutException for course with url=%s. Discarding." % (course_homepage_url)
            log.msg(msg, level=log.ERROR)
            raise


    def crawl_course(self, response):
        driver = self.edx_logger.driver
        driver.maximize_window()
        driver.get(response.url)

        try:
            self.access_course(driver, response.url)
        except:
            return None

        # Dict mapping section titles to dicts mapping subsection titles to links
        section_overviews = self.get_section_overviews(driver)
        section_items = []

        for section_title, subsection_mappings in section_overviews.items():
            msg = "Crawling section '%s'." % (section_title)
            log.msg(msg, level=log.INFO)

            subsection_items = []
            for ss_title, ss_link in subsection_mappings.items():
                try:
                    subsection = self.crawl_subsection(driver, ss_title, ss_link)
                    if subsection:
                        subsection_items.append(subsection)
                except:
                    msg = "Error crawling subsection '%s'." % (section_title)
                    log.msg(msg, level=log.ERROR)

            if subsection_items:
                section_items.append(
                    CourseSectionItem(
                        name = section_title,
                        subsections = [dict(s) for s in subsection_items]
                ))

        if section_items:
            course = CourseItem(
                edx_guid = response.meta['course_edx_guid'],
                sections = [dict(s) for s in section_items]
            )

            msg = "Crawled course with edx_guid='%s'." % (response.meta['course_edx_guid'])
            log.msg(msg, level=log.DEBUG)
            print course
            return course

        else:
            msg = "Failed to crawl course with edx_guid='%s'." % (response.meta['course_edx_guid'])
            log.msg(msg, level=log.ERROR)
            return None


    def get_section_overviews(self, driver):
        '''
        Assemble sections (names) and subsections (names and links)
        in order to crawl them later --use an ordered dictionary mapping
        section names to ordered dictionaries mapping subsection names
        to subsection links.
        '''
        sections = OrderedDict()
        for section_el in driver.find_elements_by_class_name('chapter'):
            section_title = section_el.find_element_by_xpath('.//h3/a').text

            subsections = OrderedDict()
            for subsection_el in section_el.find_elements_by_xpath('.//ul/li'):
                source = Selector(text = subsection_el.get_attribute('innerHTML'))

                subsection_title = source.xpath('//a/p[1]/text()').extract()[0]
                subsection_link = subsection_el.find_element_by_xpath('.//a').get_attribute('href')
                subsections[subsection_title] = subsection_link

            sections[section_title] = subsections

        return sections


    def crawl_subsection(self, driver, subsection_title, subsection_link):
        msg = "Crawling subsection '%s' with url=%s" \
            % (subsection_title, subsection_link)
        log.msg(msg, level=log.INFO)

        driver.get(subsection_link)
        time.sleep(6)

        units = []

        for unit_el in driver.find_elements_by_xpath('//*[@id="sequence-list"]/li'):
            sub = unit_el.find_element_by_xpath('.//a')

            if 'seq_video' in sub.get_attribute('class'):
                source = Selector(text = sub.get_attribute('innerHTML'))
                unit_title = source.xpath('//p/text()').extract()[0]

                sub.click()
                time.sleep(2)
                try:
                    unit = self.crawl_unit(driver, unit_title)
                    if unit:
                        units.append(unit)
                except:
                    msg = "Error crawling unit '%s'." % (unit_title)
                    log.msg(msg, level=log.ERROR)

        if units:
            return CourseSubsectionItem(
                name = subsection_title,
                href = subsection_link,
                units = [dict(u) for u in units]
            )
        else:
            return None


    def crawl_unit(self, driver, unit_title):
        msg = "Crawling unit '%s'." % (unit_title)
        log.msg(msg, level=log.INFO)

        videos = []
        written_content = ""

        for module in driver.find_elements_by_xpath('//*[@id="seq_content"]/div/div/div'):
            module = module.find_element_by_xpath('.//div')
            data_type = module.get_attribute('data-block-type')

            if data_type == 'html':
                paragraphs = module.find_elements_by_xpath('.//p/span')
                for p in paragraphs:
                    written_content += "\n" + p.text

            elif data_type == 'video':
                try:
                    name = module.find_element_by_xpath('.//h2').text
                    youtube_embed_url = module.find_element_by_xpath(\
                        './/div/div/article/section/iframe').get_attribute('src')

                    videos.append(CourseVideoItem(
                        name = name,
                        href = youtube_embed_url
                    ))

                    msg = "Got video with url='%s'." % (youtube_embed_url)
                    log.msg(msg, level=log.INFO)

                except:
                    msg = "Error crawling video with url='%s'." % (youtube_embed_url)
                    log.msg(msg, level=log.ERROR)

        if videos:
            return CourseUnitItem(
                name = unit_title,
                href = driver.current_url,
                description = written_content,
                videos = [dict(v) for v in videos]
            )
        else:
            return None


    def closed(self, reason):
        self.session.close()
        self.edx_logger.close()
