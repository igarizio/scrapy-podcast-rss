"""This module defines the items that will contain the podcast information.
"""

import scrapy


class PodcastDataItem(scrapy.Item):
    """General information about the podcast."""
    title = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()
    image_url = scrapy.Field()


class PodcastEpisodeItem(scrapy.Item):
    """Information about each episode of the podcast."""
    title = scrapy.Field()
    description = scrapy.Field()
    publication_date = scrapy.Field()
    audio_url = scrapy.Field()
    guid = scrapy.Field()
