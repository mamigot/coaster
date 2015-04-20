from scrapy.item import Item, Field


class SubjectItem(Item):
    name = Field()


class InstructorItem(Item):
    edx_nid = Field()
    name = Field()


class InstitutionItem(Item):
    name = Field()


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

    sections = Field()


class CourseSectionItem(Item):
    name = Field()
    subsections = Field()


class CourseSubsectionItem(Item):
    name = Field()
    units = Field()
    href = Field()


class CourseUnitItem(Item):
    name = Field()
    href = Field()
    description = Field()
    videos = Field()


class CourseVideoItem(Item):
    identifier = Field()

    name = Field()
    href = Field()
    transcript = Field()

    youtube_id = Field()
    yt_views = Field()
    yt_likes = Field()
    yt_dislikes = Field()
    yt_favorites = Field()
    yt_comments = Field()
