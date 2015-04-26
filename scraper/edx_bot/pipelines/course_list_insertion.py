from utils.sql import get_session
from utils.sql.handlers import get_row

from utils.sql.models.institution import Institution
from utils.sql.models.instructor import Instructor
from utils.sql.models.subject import Subject
from utils.sql.models.course import Course

from scrapy import log


class CourseListInsertion(object):
    '''
    Places the course in the database, along with the higher
    models that it entails: institution, subjects and instructors.
    '''
    session = None

    def process_item(self, item, spider):
        if spider.name not in ['course_list']:
            return item

        self.session = get_session()
        course = get_row(self.session, Course, Course.edx_guid, item['edx_guid'])

        if not course:
            institution = get_row(self.session, Institution,
                Institution.name, item['institution']['name'])
            if not institution:
                institution = Institution(name = item['institution']['name'])

            subjects = []
            for item_subject in item['subjects']:
                if not item_subject['name']: continue

                subject = get_row(self.session, Subject, Subject.name, item_subject['name'])
                if not subject:
                    subject = Subject(name = item_subject['name'])
                subjects.append(subject)

            instructors = []
            for item_instructor in item['instructors']:
                if not item_instructor['edx_nid']: continue

                instructor = get_row(self.session, Instructor,
                    Instructor.edx_nid, item_instructor['edx_nid'])
                if not instructor:
                    instructor = Instructor(
                        name = item_instructor['name'],
                        edx_nid = item_instructor['edx_nid'])
                instructors.append(instructor)

            course = Course(
                edx_guid = item['edx_guid'],
                edx_code = item['edx_code'],
                name = item['name'],
                href = item['href'],
                availability = item['availability'],
                start = item['start'],
            )

            institution.courses.append(course)
            for s in subjects:
                course.subjects.append(s)
            for i in instructors:
                course.instructors.append(i)

            try:
                self.session.add(institution)
                self.session.commit()
            except:
                self.session.rollback()
                self.session.close()
                raise

        self.session.close()
