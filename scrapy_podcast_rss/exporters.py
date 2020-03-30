"""Custom exporters that generate and save rss feeds.
"""
import abc
from urllib.parse import urlparse

from feedgen.feed import FeedGenerator
from scrapy.exporters import BaseItemExporter

try:
    import boto3
except ImportError:
    boto3 = None


class PodcastBaseItemExporter(BaseItemExporter, metaclass=abc.ABCMeta):
    """Item exporter base class designed to generate rss feeds.

    The class uses feedgen to generate the rss content.
    Subclasses are expected to implement the method save_to_storage.
    """

    def __init__(self, uri, title, description, url, image_url, **kwargs):
        """Initializes the exporter.

        Args:
            uri: Where to save the feed.
            title: Podcast title.
            description: Description of the podcast.
            url: Url of the podcast.
            image_url: Main image of the podcast.
            **kwargs: Any extra argument for BaseItemExporter.
        """
        super().__init__(**kwargs)
        self.uri = uri

        self.fg = FeedGenerator()
        self.fg.load_extension('podcast')

        self.fg.title(title)
        self.fg.description(description)
        self.fg.link(href=url)
        self.fg.image(image_url)
        self.fg._FeedGenerator__rss_lastBuildDate = None  # This prevents Plex from confusing pubDate with lastBuildDate

    def export_item(self, item):
        """Adds a new entry to the rss feed.

        Args:
            item: A PodcastEpisodeItem.
        """
        fe = self.fg.add_entry()

        title = item.get('title')
        description = item.get('description')
        publication_date = item.get('publication_date')
        audio_url = item.get('audio_url')
        guid = item.get('guid')

        fe.title(title)
        fe.description(description)
        fe.published(publication_date)
        fe.enclosure(audio_url, 0, 'audio/mpeg')
        fe.guid(guid)

    def finish_exporting(self):
        """Generates the rss content and saves it to a file"""
        rss_content = self.fg.rss_str(pretty=True)
        self.save_to_storage(rss_content)

    @abc.abstractmethod
    def save_to_storage(self, rss_content):
        """Subclasses must implement a way of saving the content.
        """
        pass


class PodcastToFileItemExporter(PodcastBaseItemExporter):
    """Exporter that saves the rss feed to a local file."""

    def save_to_storage(self, content):
        """Saves the content to a local file."""
        f = open(self.uri, 'wb')
        f.write(content)
        f.close()


class PodcastToS3ItemExporter(PodcastBaseItemExporter):
    """Exporter that saves the rss feed to an S3 bucket

    NOTE 1: This exporter needs boto3 in order to operate.
    NOTE 2: By default, the file is configured as PUBLIC-READ.
    """
    def __init__(self, *args, **kwargs):
        """Checks if boto3 is installed."""
        super().__init__(*args, **kwargs)
        if boto3 is None:
            raise ImportError("You need to install boto3 to export items to S3. More information here: "
                              "https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html")

    def save_to_storage(self, content):
        """Saves the content with PUBLIC-READ permission to an S3 bucket.

        The uri defined in the settings under the name OUTPUT_URI needs
        to have the following format:
            s3://{bucket-name}/{rss-feed-filename}.xml
        (the extension can also be changed.)
        """
        url = urlparse(self.uri)
        bucket = url.netloc
        filename = url.path.split("/")[-1]

        s3 = boto3.resource('s3')
        s3_object = s3.Object(bucket, filename)
        s3_object.put(Body=content, ACL='public-read')
