BOT_NAME = 'edx_bot'

SPIDER_MODULES = ['scraper.edx_bot.spiders']
NEWSPIDER_MODULE = 'scraper.edx_bot.spiders'

# http://doc.scrapy.org/en/latest/topics/item-pipeline.html#activating-an-item-pipeline-component
ITEM_PIPELINES = {
    'scraper.edx_bot.pipelines.course_list_insertion.CourseListInsertion': 100,
    'scraper.edx_bot.pipelines.general_course_content_insertion.GeneralCourseContentInsertion': 150,
    'scraper.edx_bot.pipelines.video_transcripts_insertion.VideoTranscriptInsertion': 200,
    'scraper.edx_bot.pipelines.youtube_stats_insertion.YouTubeStatsInsertion': 250,
}

LOG_LEVEL = 'INFO'
LOG_STDOUT = True
