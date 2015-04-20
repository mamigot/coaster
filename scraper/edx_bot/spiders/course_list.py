import json
from scrapy import Spider, Request, log
from scraper.edx_bot.items import CourseItem, SubjectItem, \
    InstructorItem, InstitutionItem


class CourseList(Spider):
    '''
    Using edX's search API (see 'edx_search_url' below), retrieves a list
    of its courses and sends them to the pipelines.
    This doesn't mean, however, that all of them will be crawled.
    That will be up to subsequent spiders.
    '''
    name = 'course_list'
    allowed_domains = ['edx.org']
    edx_search_url = 'https://www.edx.org/search/api/all'

    def start_requests(self):
        return [Request(url=self.edx_search_url, callback=self.parse)]


    def parse(self, response):
        js = json.loads(response.body_as_unicode())

        for course_info in js:
            subjects = []
            if course_info['subjects']:
                subjects = [SubjectItem(name=s) for s in course_info['subjects']]

            instructors = []
            if course_info['staff']:
                for i in range(len(course_info['staff'])):
                    instructors.append(
                        InstructorItem(
                            edx_nid = course_info['staff-nids'][i],
                            name = course_info['staff'][i],
                        )
                    )

            course = CourseItem(
                edx_guid = course_info['guid'],
                edx_code = course_info['code'],
                name = course_info['l'],
                href = course_info['url'],
                availability = course_info['availability'],
                start = course_info['start'],
            )

            institution = InstitutionItem(name = course_info['schools'][0])

            course['institution'] = dict(institution)
            course['subjects'] = [dict(s) for s in subjects]
            course['instructors'] = [dict(i) for i in instructors]

            yield course
