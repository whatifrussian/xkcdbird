#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
# Currently not used, see below.
#import logging

AUTHOR = u'xkcd'
SITENAME = u'XKCD — по-русски'
 
TIMEZONE = 'Europe/Moscow'

DEFAULT_LANG = u'ru'

PLUGIN_PATHS = [ "plugins" ]
PLUGINS = ["neighbors", "sitemap", "xkcd_json", "num_neighbors"]
THEME = "themes/xkcd"
PATH = 'content'
OUTPUT_PATH = 'output'
DELETE_OUTPUT_DIRECTORY = True

# Feed generation is usually not desired when developing
FEED_ALL_RSS = "feed/index.xml"
CATEGORY_FEED_RSS = "feed/category/%s/index.xml"
TAG_FEED_RSS = "feed/category/%s/index.xml"
FEED_ATOM = None
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
TAG_FEED_ATOM = None
FEED_MAX_ITEMS = 5

# Save as URL
ARTICLE_URL = '{slug}/'
ARTICLE_SAVE_AS = '{slug}/index.html'
ARTICLE_JSON_SAVE_AS = '{slug}/info.0.json'
ARTICLE_JSON_INDEX_SAVE_AS = "articles.json"
ARTICLE_JSON_LAST_SAVE_AS = "info.0.json"
ARTICLE_JSON_CATEGORY_SLUG = 'xkcd'
CATEGORY_URL = '{slug}/'
CATEGORY_SAVE_AS = '{slug}/index.html'
TAGS_SAVE_AS = ''
TAG_SAVE_AS = ''
AUTHOR_SAVE_AS = ''
AUTHORS_SAVE_AS = ''
ARCHIVES_SAVE_AS = ''
CATEGORIES_SAVE_AS = ''

NUMS_SAVE_AS = 'num/index.html'
IMGS_SAVE_AS = 'img/index.html'
RANDOM_SAVE_AS = 'random/index.html'


# Currently that isn’t not working, see
# https://github.com/getpelican/pelican/issues/1594
#LOG_FILTER = [
#    (logging.WARN, 'Empty alt attribute for image %s in %s')
#]

TEMPLATE_PAGES = {
    '404.html': '404.html',
}

SLUG_SUBSTITUTIONS = [
]

DEFAULT_PAGINATION = False

EXTRA_PATH_METADATA = {

}

STATIC_PATHS = [
    'comics',
    'super'
]

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = False
READERS = {'html': None}

SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.5,
        'indexes': 0.5,
        'pages': 0.5
    },
    'changefreqs': {
        'articles': 'monthly',
        'indexes': 'daily',
        'pages': 'monthly'
    }
}

MD_EXTENSIONS = (['extra', 'abbr', 'footnotes'])

import json

def quotes(text):
    return text.replace('"','\\"').replace("'","\'").replace("\n", "\\n").replace("\r", "\\r")

JINJA_FILTERS = { "tojson": json.dumps, "quotes": quotes }
