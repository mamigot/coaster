from utils.sql import get_session
from utils.sql.handlers import get_row

from utils.sql.models.course_video import CourseVideo


class YouTubeDataPlacement(object):
    '''
    Places the course in the database, along with the higher
    models that it entails: institution, subjects and instructors.
    '''
    session = None

    def process_item(self, item, spider):
        if spider.name not in ['youtube_data_retriever']:
            return item

        self.session = get_session()
        video = get_row(self.session, CourseVideo, CourseVideo.id, item['identifier'])

        video.yt_views = item['yt_views']
        video.yt_likes = item['yt_likes']
        video.yt_dislikes = item['yt_dislikes']
        video.yt_favorites = item['yt_favorites']
        video.yt_comments = item['yt_comments']

        self.session.add(video)
        self.session.commit()
        self.session.close()
