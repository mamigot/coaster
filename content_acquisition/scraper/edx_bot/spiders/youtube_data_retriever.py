import json
from datetime import datetime

from scrapy import Spider, Request, log
from scrapy.exceptions import CloseSpider

from edx_bot.items import CourseVideoItem
from edx_bot.spiders.config import YOUTUBE_SERVER_API_KEY as API_KEY

from utils.sql import get_session
from utils.sql.models.course_video import CourseVideo


class YouTubeDataRetriever(Spider):
    '''
    Using the YouTube IDs on the CourseVideo model, queries the YouTube API
    for relevant stats and sends them off to the pipelines.
    '''
    name = 'youtube_data_retriever'
    allowed_domains = ['youtube.com', 'googleapis.com']
    # http://doc.scrapy.org/en/latest/topics/spider-middleware.html#scrapy.contrib.spidermiddleware.httperror.HttpErrorMiddleware
    handle_httpstatus_list = [403, 404]
    session = None

    def start_requests(self):
        self.session = get_session()
        # http://stackoverflow.com/questions/17868743/doing-datetime-comparisons-in-filter-sqlalchemy
        one_month_ago = datetime.utcnow() - datetime.timedelta(weeks=2)

        for c in self.session.query(CourseVideo)\
            .filter(CourseVideo.stats_as_of < one_month_ago):

            yield Request(
                url = self.get_api_url(c.youtube_id),
                meta = {'course_video_id':c.id},
            )


    def get_api_url(self, youtube_video_id):
        return 'https://www.googleapis.com/youtube/v3/videos?id=%s&key=%s&part=statistics' \
            % (youtube_video_id, API_KEY)


    def parse(self, response):
        if response.status in self.handle_httpstatus_list:
            msg = "HTTP %d. Failed to parse url=%s." % (response.status, response.url)
            msg += "\nMore info: https://developers.google.com/youtube/v3/docs/errors"
            msg += "\nresponse.body:\n" + response.body
            raise CloseSpider(msg)

        js = json.loads(response.body_as_unicode())
        stats = js['items'][0]['statistics']

        yield CourseVideoItem(
            identifier = response.meta['course_video_id'],
            yt_views = stats['viewCount'],
            yt_likes = stats['likeCount'],
            yt_dislikes = stats['dislikeCount'],
            yt_favorites = stats['favoriteCount'],
            yt_comments = stats['commentCount'],
        )


    def closed(self, reason):
        self.session.close()
