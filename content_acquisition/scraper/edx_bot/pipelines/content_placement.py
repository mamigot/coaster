import re

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
            section = get_row_from_parent(\
                CourseSection, "name", item_section['name'],\
                course.sections)

            if not section:
                section = CourseSection(
                    name=item_section['name'].strip()
                )
                course.sections.append(section)

            for item_subsection in item_section['subsections']:
                subsection = get_row_from_parent(\
                    CourseSubsection, "name", item_subsection['name'],\
                    section.subsections)

                if not subsection:
                    subsection = CourseSubsection(
                        name=item_subsection['name'].strip(),
                        href=item_subsection['href'].strip()
                    )
                    section.subsections.append(subsection)

                for item_unit in item_subsection['units']:
                    unit = get_row_from_parent(\
                        CourseUnit, "name", item_unit['name'],\
                        subsection.units)

                    if not unit:
                        unit = CourseUnit(
                            name=item_unit['name'].strip(),
                            description=item_unit['description'].strip()
                        )
                        subsection.units.append(unit)

                    for item_video in item_unit['videos']:
                        video = get_row_from_parent(\
                            CourseVideo, "href", item_video['href'],\
                            unit.videos)

                        if not video:
                            video = CourseVideo(
                                name=item_video['name'].strip(),
                                href=item_video['href'].strip(),
                                youtube_id=self.parse_youtube_id(item_video['href'])
                            )
                            unit.videos.append(video)

        self.session.add(course)
        self.session.commit()
        self.session.close()


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
