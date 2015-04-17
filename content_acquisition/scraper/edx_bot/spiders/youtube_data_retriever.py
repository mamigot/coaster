import json
from scrapy import Spider, Request, log

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
    session = None

    def start_requests(self):
        self.session = get_session()

        for c in self.session.query(CourseVideo).filter(CourseVideo.yt_views == None):
            yield Request(
                url = self.get_api_url(c.youtube_id),
                meta = {'course_video_id':c.id},
            )


    def get_api_url(self, youtube_video_id):
        return 'https://www.googleapis.com/youtube/v3/videos?id=%s&key=%s&part=statistics' \
            % (youtube_video_id, API_KEY)


    def parse(self, response):
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
