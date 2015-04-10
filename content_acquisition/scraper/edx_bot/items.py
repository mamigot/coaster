from scrapy.item import Item, Field


class CourseItem(Item):
    edx_guid = Field()
    edx_code = Field()

    name = Field()
    href = Field()
    institution = Field()

    availability = Field()
    start = Field()

    # Following fields are plural (see below)
    # http://stackoverflow.com/questions/11184557/how-to-implement-nested-item-in-scrapy
    subjects = Field()
    instructors = Field()


class SubjectItem(Item):
    name = Field()


class InstructorItem(Item):
    edx_nid = Field()
    name = Field()


class InstitutionItem(Item):
    name = Field()
