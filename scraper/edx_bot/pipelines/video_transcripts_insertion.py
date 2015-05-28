from utils.sql import get_session
from utils.sql.handlers import get_row
from utils.sql.models.course_video import CourseVideo

from clean_up import Cleaner


class VideoTranscriptInsertion(object):
    session = None

    def process_item(self, item, spider):
        if spider.name not in ['video_transcripts']:
            return item

        self.session = get_session()
        video = get_row(self.session, CourseVideo, CourseVideo.id, item['_id'])

        video.transcript = self.clean_transcript(item['transcript'])

        self.session.add(video)
        self.session.commit()
        self.session.close()


    def clean_transcript(self, transcript):
        return Cleaner.rm_whitespace(transcript)
