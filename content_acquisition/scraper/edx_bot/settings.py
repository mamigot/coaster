PROJECT_DIRECTORY_PATH = '/Users/miguelamigot/Software/NYU/WSE/Coaster/'

BOT_NAME = 'edx_bot'

SPIDER_MODULES = ['edx_bot.spiders']
NEWSPIDER_MODULE = 'edx_bot.spiders'

# http://doc.scrapy.org/en/latest/topics/item-pipeline.html#activating-an-item-pipeline-component
ITEM_PIPELINES = {
    'edx_bot.pipelines.course_placement.CoursePlacement': 100,
    'edx_bot.pipelines.content_placement.ContentPlacement': 150,
    'edx_bot.pipelines.youtube_data_placement.YouTubeDataPlacement': 200,
}
