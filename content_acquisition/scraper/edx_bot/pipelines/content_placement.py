import re

from scrapy import log
from scrapy.exceptions import DropItem

from utils.sql import get_session
from utils.sql.handlers import get_row, get_row_from_parent

from utils.sql.models.course import Course
from utils.sql.models.course_section import CourseSection
from utils.sql.models.course_subsection import CourseSubsection
from utils.sql.models.course_unit import CourseUnit
from utils.sql.models.course_video import CourseVideo


class ContentPlacement(object):
    '''
    Places the course's content in the database, structured into sections,
    subsections, units and videos.
    '''
    session = None

    def process_item(self, item, spider):
        if spider.name not in ['course_downloader']:
            return item

        self.session = get_session()
        course = get_row(self.session, Course, Course.edx_guid, item['edx_guid'])

        if not course:
            msg = "Cannot store content of course with edx_guid=%s because " \
                "the course cannot be located in the DB." % (item['edx_guid'])
            log.msg(msg, level=log.ERROR)

            self.session.close()
            raise DropItem("Ignoring content from course with edx_guid=%s" \
                % item['edx_guid'])

        for item_section in item['sections']:
            self.process_section(item_section, course.sections)

        self.session.add(course)
        self.session.commit()
        self.session.close()


    def process_section(self, item_section, section_collection):
        item_section['name'] = item_section['name'].strip()

        section = get_row_from_parent(\
            CourseSection, "name", item_section['name'],\
            section_collection)

        if not section:
            section = CourseSection(
                name=item_section['name']
            )
            section_collection.append(section)

        for item_subsection in item_section['subsections']:
            self.process_subsection(item_subsection, section.subsections)


    def process_subsection(self, item_subsection, subsection_collection):
        item_subsection['name'] = item_subsection['name'].strip()

        subsection = get_row_from_parent(\
            CourseSubsection, "name", item_subsection['name'],\
            subsection_collection)

        if not subsection:
            subsection = CourseSubsection(
                name=item_subsection['name'],
                href=item_subsection['href'].strip()
            )
            subsection_collection.append(subsection)

        for item_unit in item_subsection['units']:
            self.process_unit(item_unit, subsection.units)


    def process_unit(self, item_unit, unit_collection):
        item_unit['name'] = item_unit['name'].strip()

        unit = get_row_from_parent(\
            CourseUnit, "name", item_unit['name'],\
            unit_collection)

        if not unit:
            unit = CourseUnit(
                name=item_unit['name'],
                description=item_unit['description'].strip()
            )
            unit_collection.append(unit)

        for item_video in item_unit['videos']:
            self.process_video(item_video, unit.videos)


    def process_video(self, item_video, video_collection):
        item_video['name'] = item_video['name'].strip()

        video = get_row_from_parent(\
            CourseVideo, "href", item_video['href'],\
            video_collection)

        if not video:
            video = CourseVideo(
                name=item_video['name'],
                href=item_video['href'].strip(),
                youtube_id=self.parse_youtube_id(item_video['href'])
            )
            video_collection.append(video)


    def parse_youtube_id(self, youtube_embed_url):
        '''
        Provided a YouTube embed URL, parses the YouTube ID and returns it.
        Sample embed URL:
            https://www.youtube.com/embed/Q-rY8DIwYgg?controls...
        '''
        # This regex pattern will include 'embed/' and end with an additional '?'
        # http://stackoverflow.com/questions/2742813/how-to-validate-youtube-video-ids/4084332#4084332
        pattern = r'embed\/[a-zA-Z0-9_-]{11}\?'
        match = re.search(pattern, youtube_embed_url).group()

        # Slice out 'embed/' and the ending '?'
        youtube_id = match[6:len(match)-1]
        return youtube_id
