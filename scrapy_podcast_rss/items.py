"""This module defines the items that will contain the podcast information.
"""
from itertools import count

import scrapy


class PodcastDataItem(scrapy.Item):
    """General information about the podcast."""
    title = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()
    image_url = scrapy.Field()


class PodcastEpisodeItem(scrapy.Item):
    """Information about each episode of the podcast.

    Note: The variable episode_order is an autoincremental
    counter, but it can be overwritten if necessary.
    """
    __episode_counter = count()
    episode_order = scrapy.Field()

    title = scrapy.Field()
    description = scrapy.Field()
    publication_date = scrapy.Field()
    audio_url = scrapy.Field()
    guid = scrapy.Field()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self['episode_order'] = next(PodcastEpisodeItem.__episode_counter)
