import time
import requests

from scrapy import Spider, Request, log
from scrapy.selector import Selector

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

from utils.sql import get_session
from utils.sql.models.course_unit import CourseUnit
from utils.sql.models.course_video import CourseVideo

from edx_bot.spiders import EdXLoggerIn
from edx_bot.spiders.general_course_content_spider import GeneralCoursewareSpider

from edx_bot.items import CourseVideoItem


class VideoTranscriptSpider(Spider):
    name = 'video_transcript_spider'
    allowed_domains = ['edx.org', 'youtube.com']
    session = None


    def start_requests(self):
        self.session = get_session()
        self.edx_logger = EdXLoggerIn()

        driver = self.edx_logger.driver
        driver.maximize_window()

        # TODO: Improve this (should be a single query)
        for video_id in self.session.query(CourseVideo.id).filter(\
            CourseVideo.transcript == None):

            unit_href = self.session.query(CourseUnit.href).filter(\
                CourseUnit.videos.any(CourseVideo.id == video_id)).first()

            yield Request(
                url = unit_href[0],
                meta = {'video_id':video_id[0]},
                cookies = driver.get_cookies(),
                callback = self.fetch_transcript
            )


    def fetch_transcript(self, response):
        driver = self.edx_logger.driver
        driver.get(response.url)
        time.sleep(3)

        for module in driver.find_elements_by_xpath('//*[@id="seq_content"]/div/div/div'):
            module = module.find_element_by_xpath('.//div')
            data_type = module.get_attribute('data-block-type')

            if data_type == 'video':
                try:
                    for download_button in module.find_elements_by_class_name('video-download-button'):
                        sub_element = download_button.find_element_by_xpath('.//a')
                        if sub_element.text == 'Download transcript':
                            transcript_href = sub_element.get_attribute('href')

                            msg = "Got transcript url=%s" % (transcript_href)
                            log.msg(msg, level=log.DEBUG)

                            return self.parse_transcript(transcript_href, \
                                driver.get_cookies(), meta = response.meta)


                except NoSuchElementException:
                    msg = "No txt transcript found for video in unit with url=%s" \
                        % (response.url)
                    log.msg(msg, level=log.DEBUG)

        return None


    def parse_transcript(self, transcript_href, driver_cookies, meta):
        cookies = {}
        for d_cookie in driver_cookies:
            cookies[d_cookie["name"]] = d_cookie["value"]

        r = requests.get(transcript_href, cookies=cookies)
        transcript = r.text

        return CourseVideoItem(
            identifier = meta['video_id'],
            transcript = transcript.strip()
        )


    def closed(self, reason):
        self.session.close()
        self.edx_logger.close()
