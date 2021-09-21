# tumblr-scraper

*tumblr-scraper* is a command-line tool written in Python for scraping photos and videos from tumblr blogs.

<a href="https://pypi.org/project/tumblr-scraper/"><img src="https://img.shields.io/pypi/pyversions/tumblr-scraper" alt="Python versions"></a>
<a href="https://pypi.org/project/tumblr-scraper/"><img src="https://img.shields.io/pypi/v/tumblr-scraper" alt="PyPI"></a>
<a href="https://github.com/giosali/tumblr-scraper/blob/main/LICENSE"><img src="https://img.shields.io/pypi/l/tumblr-scraper" alt="license"></a>
<a href="https://github.com/giosali/tumblr-scraper"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="code-style: black"></a>

## Installation

To get started, you can install *tumblr-scraper* by using `pip`:

```console
$ pip install tumblr-scraper
```

*tumblr-scraper* supports Python 3.7+.

## Usage

You can scrape the media from a blog by running:

```console
$ tumblr-scraper <blog>
```

All of the media will be downloaded in a directory named after the blog in your current working directory: `<cwd>/<blog>`

### Arguments

Here are the command-line arguments available:

```
usage: tumblr-scraper [-h] [-v] blog

positional arguments:
    blog            The name of the tumblr blog

optional arguments:
    -h, --help      show this help message and exit
    -v, --verbose   Enable debugging
```