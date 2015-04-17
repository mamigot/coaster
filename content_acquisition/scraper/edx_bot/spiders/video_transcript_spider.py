import time

from scrapy import Spider, Request, log
from scrapy.selector import Selector

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException

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

        # Select a video without a transcript.
        # Go to its unit and fetch the transcript (TODO: if a transcript is not
        # in one unit, it might be in the others).
        # Return the unit, video pair.
        for unit, video in self.session.query(CourseUnit, CourseVideo)\
            .filter(CourseUnit.videos.any(CourseVideo.transcript == None)).all():

            yield Request(
                url = unit.href,
                meta = {'video_id':video.id, 'unit_id':unit.id},
                cookies = driver.get_cookies(),
                callback = self.fetch_transcript
            )


    def fetch_transcript(self, response):
        driver = self.edx_logger.driver
        driver.get(response.url)
        time.sleep(3)

        print "\nRESPONSE\n"
        print response.url
        print "\n\n"


        return None


    def closed(self, reason):
        self.session.close()
        self.edx_logger.close()
