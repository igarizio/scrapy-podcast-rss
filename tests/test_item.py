import unittest

from scrapy_podcast_rss import PodcastDataItem, PodcastEpisodeItem


class TestPodcastDataItem(unittest.TestCase):
    def test_parametrization(self):
        test_title = "Test title"
        item = PodcastDataItem(title=test_title)
        self.assertEqual(item['title'], test_title)


class TestPodcastEpisodeItem(unittest.TestCase):
    def test_parametrization(self):
        test_title = "Test title"
        item = PodcastEpisodeItem(title=test_title)
        self.assertEqual(item['title'], test_title)
