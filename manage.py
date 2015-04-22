import sys


'''
Creates course content tables on Postgres
'''
def create_course_tables():
    from utils.sql import Base, db_connect

    from utils.sql.models import institution, instructor, subject, \
        course, course_section, course_subsection, course_unit, course_video

    engine = db_connect()
    # MetaData issues CREATE TABLE statements to the database
    # for all tables that don't yet exist
    Base.metadata.create_all(engine)


'''
Crawl Scrapy spider

http://doc.scrapy.org/en/latest/topics/practices.html#run-scrapy-from-a-script
'''
def scrapy_crawl_spider(spider_name):
    from twisted.internet import reactor
    from scrapy.crawler import Crawler
    from scrapy import log, signals
    from scrapy.utils.project import get_project_settings

    spider = None

    if spider_name == 'course_list':
        from scraper.edx_bot.spiders.course_list \
            import CourseList
        spider = CourseList()

    elif spider_name == 'general_course_content':
        from scraper.edx_bot.spiders.general_course_content \
            import GeneralCourseContent
        spider = GeneralCourseContent()

    elif spider_name == 'video_transcripts':
        from scraper.edx_bot.spiders.video_transcripts \
            import VideoTranscripts
        spider = VideoTranscripts()

    elif spider_name == 'youtube_stats':
        from scraper.edx_bot.spiders.youtube_stats \
            import YouTubeStats
        spider = YouTubeStats()

    settings = get_project_settings()
    crawler = Crawler(settings)
    crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()
    log.start(loglevel=log.INFO)
    reactor.run()


if __name__ == '__main__':
    if sys.argv[1] == 'create_course_tables':
        create_postgres_tables()

    elif sys.argv[1] == 'scrapy':
        if sys.argv[2] == 'crawl':
            if sys.argv[3] in ['course_list', 'general_course_content', \
                'video_transcripts', 'youtube_stats']:

                    scrapy_crawl_spider(sys.argv[3])
