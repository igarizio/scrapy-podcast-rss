# scrapy-podcast-rss
This package provides a Scrapy pipeline and items to create podcast RSS files 
from scraped information. It also allows to save the file locally or in an S3 
bucket. You can then point your podcast player to the URL of the file and 
listen to its content.

## Installation
Install scrapy-podcast-rss using ``pip``:
```console
$ pip install scrapy-podcast-rss
```

## Configuration
1. You need to define an ``OUTPUT_URI`` pointing to where you want to store the
file, For example:
    ```python
    OUTPUT_URI = './my-podcast.xml'  # Local file.
    OUTPUT_URI = 's3://my-bucket/my-podcast.xml'  # S3 bucket.
    ```
2. Add ``PodcastPipeline`` in ``ITEM_PIPELINES`` in your ``settings.py`` file:
    ```python
    ITEM_PIPELINES = {
        'scrapy_podcast_rss.pipelines.PodcastPipeline': 300,
    }
    ```
   
## Usage:
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
    
## Example:
You can find a minimal example of a spider using this package in this repo 
[scrapy-podcast-rss-example](https://github.com/igarizio/scrapy-podcast-rss-example).