#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

SITEURL = 'http://blog.nerdyweekly.com'
RELATIVE_URLS = False

FEED_DOMAIN = SITEURL
FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/%s.atom.xml'

DELETE_OUTPUT_DIRECTORY = True

# Copy static files to output
FILES_TO_COPY = (('extra/CNAME', 'CNAME'),
                 ('extra/README.markdown', 'README.markdown'),
                 ('extra/favicon.ico', 'favicon.ico'))

ARTICLE_URL = 'posts/{date:%Y}/{date:%b}/{slug}/'
ARTICLE_SAVE_AS = 'posts/{date:%Y}/{date:%b}/{slug}/index.html'
ARTICLE_LANG_URL = 'posts/{date:%Y}/{date:%b}/{slug}-{lang}/'
ARTICLE_LANG_SAVE_AS = 'posts/{date:%Y}/{date:%b}/{slug}-{lang}/index.html'

# Following items are often useful when publishing

DISQUS_SITENAME = "nerdyweekly"
GOOGLE_ANALYTICS = "UA-40876322-1"
