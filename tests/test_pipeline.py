import unittest

import scrapy

from scrapy_podcast_rss import PodcastPipeline
from scrapy_podcast_rss import PodcastEpisodeItem, PodcastDataItem
from scrapy_podcast_rss.exporters import PodcastToFileItemExporter, PodcastToS3ItemExporter


class TestPodcastPipeline(unittest.TestCase):
    def test_process_item(self):
        pipeline = PodcastPipeline()
        podcast_item = PodcastDataItem()
        episode_item = PodcastEpisodeItem()
        self.assertEqual(pipeline.process_item(podcast_item, None), podcast_item)
        self.assertEqual(pipeline.process_item(episode_item, None), episode_item)

    def test_get_exporter_local_file(self):
        pipeline = PodcastPipeline()
        pipeline.process_item(PodcastDataItem(), None)
        spider = scrapy.Spider(name="test_spider", settings={})
        spider.settings['OUTPUT_URI'] = './local-file.xml'
        exporter = pipeline._get_exporter(spider)
        self.assertIsInstance(exporter, PodcastToFileItemExporter)

    def test_get_exporter_s3_file(self):
        pipeline = PodcastPipeline()
        pipeline.process_item(PodcastDataItem(), None)
        spider = scrapy.Spider(name="test_spider", settings={})
        spider.settings['OUTPUT_URI'] = 's3://my-bucket/my-podcast.xml'
        exporter = pipeline._get_exporter(spider)
        self.assertIsInstance(exporter, PodcastToS3ItemExporter)
