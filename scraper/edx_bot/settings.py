BOT_NAME = 'edx_bot'

SPIDER_MODULES = ['edx_bot.spiders']
NEWSPIDER_MODULE = 'edx_bot.spiders'

# http://doc.scrapy.org/en/latest/topics/item-pipeline.html#activating-an-item-pipeline-component
ITEM_PIPELINES = {
    'edx_bot.pipelines.course_list_insertion.CourseListInsertion': 100,
    'edx_bot.pipelines.general_course_content_insertion.GeneralCourseContentInsertion': 150,
    'edx_bot.pipelines.video_transcript_insertion.VideoTranscriptInsertion': 200,
    'edx_bot.pipelines.youtube_stats_insertion.YouTubeStatsInsertion': 250,
}
