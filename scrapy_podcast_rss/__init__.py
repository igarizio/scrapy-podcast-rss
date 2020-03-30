__all__ = ['__version__', 'PodcastDataItem', 'PodcastEpisodeItem', 'PodcastPipeline']

import pkgutil

__version__ = pkgutil.get_data(__package__, 'VERSION').decode('ascii').strip()
del pkgutil

from scrapy_podcast_rss.items import PodcastDataItem, PodcastEpisodeItem  # noqa
from scrapy_podcast_rss.pipelines import PodcastPipeline  # noqa
