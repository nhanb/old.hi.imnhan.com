#!/usr/bin/env python
# -*- coding: utf-8 -*- #
import os
import sys

sys.path.append(os.curdir)

from pelicanconf import *  # noqa

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

SITEURL = "https://old.hi.imnhan.com"
RELATIVE_URLS = True

DELETE_OUTPUT_DIRECTORY = True

# Following items are often useful when publishing

DISQUS_SITENAME = "nerdyweekly"
