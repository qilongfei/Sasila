#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import sys


from bs4 import BeautifulSoup as bs

from downloader.spider_request import Request

reload(sys)
sys.setdefaultencoding('utf-8')


class BaseProcessor(object):
    def __init__(self, scheduler):
        self.scheduler = scheduler

    def nice_join(self, base, url):
        url1 = urljoin(base, url)
        arr = urlparse(url1)
        path = normpath(arr[2])
        return urlunparse((arr.scheme, arr.netloc, path, arr.params, arr.query, arr.fragment))

    def is_url(self, url):
        if re.match(r'^https?:/{2}\w.+$', url):
            return True
        else:
            return False

    def add_url(self, url):
        if self.is_url(url):
            self.scheduler.push(Request(url))

    def process(self, request):
        soup = bs(request.content)
        a_list = soup.select('a')
        for a in a_list:
            if 'href' in a.attrs:
                url = self.nice_join(request.request.url, a['href'])
                if 'download' not in url and '.apk' not in url:
                    self.add_url(url)


