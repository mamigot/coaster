import sys, os

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
    from scrapy.settings import Settings
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

    else:
        print "spider '%s' is not listed" % spider_name

    # Working around bug in Scrapy's source code
    # http://stackoverflow.com/a/29874137/2708484
    settings = Settings()
    os.environ['SCRAPY_SETTINGS_MODULE'] = 'scraper.edx_bot.settings'
    settings_module_path = os.environ['SCRAPY_SETTINGS_MODULE']
    settings.setmodule(settings_module_path, priority='project')
    crawler = Crawler(settings)

    crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()
    log.start(loglevel=log.INFO)
    reactor.run()


def build_inverted_index():
    from search_engine import indexing
    indexing.index_video_transcripts()


def test_search_results(raw_query):
    from search_engine.driver import process_search
    return process_search(raw_query)


if __name__ == '__main__':
    if sys.argv[1] == 'create_course_tables':
        create_course_tables()

    elif sys.argv[1] == 'scrapy':
        if sys.argv[2] == 'crawl':
            if sys.argv[3] in ['course_list', 'general_course_content', \
                'video_transcripts', 'youtube_stats']:

                    scrapy_crawl_spider(sys.argv[3])
            else:
                print "spider name: '%s' is not listed" % sys.argv[3]
        else:
            print "command: '%s' is not listed" % sys.argv[2]

    elif sys.argv[1] == 'build_inverted_index':
        build_inverted_index()


    elif sys.argv[1] == 'search_for':
        if sys.argv[2]:
            print test_search_results(sys.argv[2])
        else:
            print "term: '%s' cannot be searched" % sys.argv[2]

    else:
        print "'%s' is not supported" % sys.argv[1]
