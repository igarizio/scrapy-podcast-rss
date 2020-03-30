from os.path import dirname, join
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open(join(dirname(__file__), 'scrapy_podcast_rss/VERSION'), 'rb') as f:
    version = f.read().decode('ascii').strip()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="scrapy-podcast-rss",
    version=version,
    author="Iacopo Garizio",
    author_email="info@iacopogarizio.com",
    description="Scrapy pipeline and items to create and store podcasts rss files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/igarizio/scrapy-podcast-rss",
    packages=setuptools.find_packages('scrapy_podcast_rss'),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
