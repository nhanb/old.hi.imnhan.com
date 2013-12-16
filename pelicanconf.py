#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Bùi Thành Nhân'
SITENAME = u'Nerdy Weekly'
SITESUBTITLE = u'Thoughts on programming and other stuff that matters'
SITEURL = ''

THEME = u'/home/nhanb/open-source/pelican-octopress-theme'

TIMEZONE = 'Asia/Ho_Chi_Minh'

DEFAULT_LANG = u'en'
TYPOGRIFY = True

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

STATIC_PATHS = ['images', 'extra']

EXTRA_PATH_METADATA = {
    'extra/CNAME': {'path': 'CNAME'},
    'extra/README.markdown': {'path': 'README.markdown'},
    'extra/favicon.ico': {'path': 'favicon.ico'},
    'extra/favicon.png': {'path': 'favicon.png'},
    'extra/cal.html': {'path': 'calendar/index.html'},
    'extra/404.html': {'path': '404.html'},
    'extra/google3f40dbd543a603fa.html':
    {'path': 'google3f40dbd543a603fa.html'}
}

ARTICLE_URL = 'posts/{slug}/'
ARTICLE_SAVE_AS = 'posts/{slug}/index.html'
ARTICLE_LANG_URL = 'posts/{slug}-{lang}/'
ARTICLE_LANG_SAVE_AS = 'posts/{slug}-{lang}/index.html'

PAGE_URL = ('pages/{slug}/')
PAGE_SAVE_AS = ('pages/{slug}/index.html')
PAGE_LANG_URL = ('pages/{slug}-{lang}/')
PAGE_LANG_SAVE_AS = ('pages/{slug}-{lang}/index.html')

AUTHOR_URL = ('author/{slug}/')
AUTHOR_SAVE_AS = ('author/{slug}/index.html')

CATEGORY_URL = ('category/{slug}/')
CATEGORY_SAVE_AS = ('category/{slug}/index.html')

TAG_URL = ('tag/{slug}/')
TAG_SAVE_AS = ('tag/{slug}/index.html')

DEFAULT_PAGINATION = 10

AUTHOR_NAME = u'Bùi Thành Nhân'
AUTHOR_SLUG = "nhanb"

# Social widget
SOCIAL = (('Github', 'https://github.com/nhanb'),
          ('Facebook', 'https://www.facebook.com/thanhnhanb'),
          ('Google+',
           'https://plus.google.com/114388334309097537564?rel=author'),
          )

## Blogroll
#LINKS = (('Pelican', 'http://getpelican.com/'),
         #('Python.org', 'http://python.org/'),
         #('Jinja2', 'http://jinja.pocoo.org/')
         #)

THEME_STATIC_PATHS = ['static']

MENUITEMS = (
    ('Blog', '/'),
)

PLUGIN_PATH = '/home/nhanb/open-source/pelican-plugins'
PLUGINS = ["optimize_images"]
