"""This module defines a pipeline to create RSS feeds.

The module takes PodcastEpisodeItems and PodcastDataItems and exports them using
PodcastToS3ItemExporter or PodcastToFileItemExporter depending on the URI defined.
Remember that to use PodcastToS3ItemExporter you need to have boto3 installed.
"""
from urllib.parse import urlparse

from scrapy_podcast_rss.exceptions import InvalidItemException
from scrapy_podcast_rss.exporters import PodcastToS3ItemExporter, PodcastToFileItemExporter
from scrapy_podcast_rss.items import PodcastEpisodeItem, PodcastDataItem


class PodcastPipeline:
    """Pipeline that takes podcast items to the exporter.

    This class takes PodcastEpisodeItems and at one PodcastDataItem,
    and depending on the URI defined in the settings, exports them using
    either PodcastToS3ItemExporter or PodcastToFileItemExporter.
    """

    def __init__(self):
        """Initializes the pipeline.
        It creates an empty (_episodes_item_list) list to store
        PodcastEpisodeItems and a variable (_podcast_data_item) to store
        one PodcastDataItem.
        """
        self._episodes_item_list = []
        self._podcast_data_item = None

    def close_spider(self, spider):
        """Exports each item and closes the exporter.

        Args:
            spider: A spider.
        """
        exporter = self._get_exporter(spider)
        exporter.start_exporting()

        for episode_item in self._episodes_item_list:
            exporter.export_item(episode_item)

        exporter.finish_exporting()

    def _get_exporter(self, spider):
        """Initializes and returns a exporter.

        The exporter selected depends on the type of URI defined in the settings
        under OUTPUT_URI.

        Args:
            spider: A spider.

        Returns:
            PodcastToS3ItemExporter or PodcastToFileItemExporter
        """
        if self._podcast_data_item is None:
            raise ValueError("You need to yield at least one PodcastDataItem.")

        title = self._podcast_data_item.get('title')
        description = self._podcast_data_item.get('description')
        url = self._podcast_data_item.get('url')
        image_url = self._podcast_data_item.get('image_url')

        uri = spider.settings.get('OUTPUT_URI')
        if self._uri_for_s3(uri):
            exp = PodcastToS3ItemExporter(uri, title=title, description=description, url=url, image_url=image_url)
        else:
            exp = PodcastToFileItemExporter(uri, title=title, description=description, url=url, image_url=image_url)

        return exp

    def process_item(self, item, spider):
        """Processes each yielded item.

        This function only allows PodcastEpisodeItems and PodcastDataItems.
        It only stores the last PodcastDataItem received.

        Args:
            item: PodcastEpisodeItem or PodcastDataItem.
            spider: A spider.

        Returns:
            item: PodcastEpisodeItem or PodcastDataItem.
        """
        if isinstance(item, PodcastEpisodeItem):
            self._episodes_item_list.append(item)
        elif isinstance(item, PodcastDataItem):
            self._podcast_data_item = item
        else:
            raise InvalidItemException(f"Only PodcastEpisodeItem and PodcastDataItem are allowed, not {type(item)}")

        return item

    @staticmethod
    def _uri_for_s3(uri):
        """Checks if the URI corresponds to an S3 url."""
        url = urlparse(uri)
        return url.scheme == 's3'
