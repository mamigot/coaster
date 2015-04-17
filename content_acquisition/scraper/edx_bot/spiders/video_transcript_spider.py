import time

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
        driver.maximize_window()
        time.sleep(3)

        for module in driver.find_elements_by_xpath('//*[@id="seq_content"]/div/div/div'):
            module = module.find_element_by_xpath('.//div')
            data_type = module.get_attribute('data-block-type')

            if data_type == 'video':
                try:
                    # Check if there's a txt transcript (TODO: support .srt format)
                    transcript_hov = module.find_element_by_class_name('a11y-menu-container')

                    if transcript_hov:
                        # https://groups.google.com/d/msg/selenium-users/fj1RVXKvAew/4Ye0X8feafcJ
                        ActionChains(driver).move_to_element(transcript_hov).perform()
                        time.sleep(2)

                        for format_element in transcript_hov.find_elements_by_class_name('a11y-menu-item-link'):
                            if format_element.get_attribute('data-value') == 'txt':
                                # http://stackoverflow.com/a/11956130/2708484
                                driver.execute_script('javascript:window.scrollBy(250,350)')
                                driver.execute_script('arguments[0].click();', format_element);
                                time.sleep(2)
                                break

                        # Get download URL
                        for download_button in module.find_elements_by_class_name('video-download-button'):
                            sub_element = download_button.find_element_by_xpath('//a')
                            if sub_element.text == 'Download transcript':
                                transcript_href = sub_element.get_attribute('href')

                                print "\n\nGOT DOWNLOAD URL!\n\n"
                                print transcript_href


                except NoSuchElementException:
                    msg = "No txt transcript found for video in unit with url=%s" \
                        % (response.url)
                    log.msg(msg, level=log.DEBUG)

        # for video in videos
            # if video.has_transcript
                # select txt option if possible
                # get URL to download and cookies
                # use the requests library to download the content


        return None


    def closed(self, reason):
        self.session.close()
        self.edx_logger.close()
