import os

import setuptools

here = os.path.abspath(os.path.dirname(__file__))


def read(file_name):
    return open(os.path.join(here, file_name)).read()


about = {}
with open(os.path.join(here, 'scrapy_podcast_rss', '__version__.py'), 'r') as f:
    exec(f.read(), about)

setuptools.setup(
    name="scrapy-podcast-rss",
    version=about["__version__"],
    author=about["__author__"],
    author_email=about["__author_email__"],
    description=about["__description__"],
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/igarizio/scrapy-podcast-rss",
    packages=['scrapy_podcast_rss'],
    install_requires=["Scrapy>=1.7.3", "feedgen==0.9.0"],
    extras_require={
        's3_storage': ["boto3"],
        'tests': ["pytest==5.2.4"]
    },
    python_require='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
