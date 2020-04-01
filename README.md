# scrapy-podcast-rss
[![Build Status](https://travis-ci.org/igarizio/scrapy-podcast-rss.svg?branch=master)](https://travis-ci.org/igarizio/scrapy-podcast-rss)  
This package provides a Scrapy pipeline and items to generate a podcast RSS feed 
from scraped information. It also allows to save the content locally or in an S3 
bucket. You can then point your podcast player to the URL of the file and 
listen to its content.

## Installation
Install scrapy-podcast-rss using ``pip``:
```console
$ pip install scrapy-podcast-rss
```

## Configuration
1. You need to define ``OUTPUT_URI`` in your ``settings.py`` file, this will
determine where your feed will be stored. For example:
    ```python
    OUTPUT_URI = './my-podcast.xml'  # Local file.
    OUTPUT_URI = 's3://my-bucket/my-podcast.xml'  # S3 bucket (read note on S3 storage).
    ```
2. Add ``PodcastPipeline`` in ``ITEM_PIPELINES`` in your ``settings.py`` file:
    ```python
    ITEM_PIPELINES = {
        'scrapy_podcast_rss.pipelines.PodcastPipeline': 300,
    }
    ```
   
## Usage
scrapy-podcast-rss defines two special items:
* ``PodcastDataItem``: Stores information about the podcast.
* ``PodcastEpisodeItem``: Stores information about each episode of the podcast.

You must yield one ``PodcastDataItem`` and one ``PodcastEpisodeItem`` for each
episode you want to export, before your spider closes.

Here is the information you can currently store in each item (you need to use
the same names):
* ``PodcastDataItem``:
    * ``title``: Title of the podcast.
    * ``description``: Description of the podcast.
    * ``url``: URL referencing the podcast.
    * ``image_url``: Main image of the podcast.
* ``PodcastDataItem``:
    * ``title``: Title of the episode.
    * ``description``: Description of the episode.
    * ``publication_date``: Date of publication (``datetime`` object with timezone).
    * ``audio_url``: URL of the audio.
    * ``guid``: Unique identifier of the episode.
    
## Example
You can find a minimal example of a spider using this package here: 
[scrapy-podcast-rss-example](https://github.com/igarizio/scrapy-podcast-rss-example).  
You can also find an example of the package being used in an AWS Lambda function here: [scrapy-podcast-rss-serverless](https://github.com/igarizio/scrapy-podcast-rss-serverless).

### Spider example:
```python
import datetime
import scrapy
import pytz
from scrapy_podcast_rss import PodcastEpisodeItem, PodcastDataItem


class SimpleSpider(scrapy.Spider):
    name = "simple_spider"
    start_urls = ['http://example.com/']
    custom_settings = {
        'OUTPUT_URI': './my-podcast.xml',
        'ITEM_PIPELINES': {'scrapy_podcast_rss.pipelines.PodcastPipeline': 300, }
    }

    def parse(self, response):
        podcast_data_item = PodcastDataItem()
        podcast_data_item['title'] = "Podcast title"
        podcast_data_item['description'] = "Description of the podcast."
        podcast_data_item['url'] = "Podcast's URL"
        podcast_data_item['image_url'] = "https://live.staticflickr.com/4211/35400224382_9edcb984e5_c.jpg"  # Sample image
        yield podcast_data_item

        episode_item = PodcastEpisodeItem()
        episode_item['title'] = "Episode title"
        episode_item['description'] = "Episode description"
        pub_date_tz = datetime.datetime.strptime("01/01/2020", "%m/%d/%Y").replace(tzinfo=pytz.UTC)
        episode_item['publication_date'] = pub_date_tz  # Publication date NEEDS to have a TIME ZONE.
        episode_item['guid'] = "Episode guid"  # Simulated identifier.
        episode_item['audio_url'] = "https://ia801803.us.archive.org/13/items/MOZARTSerenadeEineKleineNachtmusikK." \
                                    "525-NEWTRANSFER01.I.Allegro/01.I.Allegro.mp3 "  # Sample audio url.
        yield episode_item
```

### Note on using S3 as storage
To use S3 storage locations, you can install scrapy-podcast-rss by doing:
```console
$ pip install scrapy-podcast-rss[s3_storage]
```
This will simply include ``boto3`` in the dependencies.  
Once installed, you will need to have your credentials configured
([boto3 quickstart guide](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html)).
