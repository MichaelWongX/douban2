# -*- coding: utf-8 -*-
import string
import scrapy
import json
from scrapy import Request
from random import sample
from ..items import DoubanItem
from scrapy.loader import ItemLoader
import requests
import json
import random
import re
from scrapy.spidermiddlewares.httperror import HttpError
from scrapy.http import TextResponse
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
from scrapy.exceptions import CloseSpider
from urllib.parse import unquote
import os
import datetime


class DoubanmovieSpider(scrapy.Spider):
    name = 'doubanmovie'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/subject/1292052/', 'https://movie.douban.com/subject/1295644/',
                  'https://movie.douban.com/subject/3541415/', 'https://movie.douban.com/subject/1292720/',
                  'https://movie.douban.com/subject/1292722/', 'https://movie.douban.com/subject/1291561/',
                  'https://movie.douban.com/subject/3793023/', 'https://movie.douban.com/subject/1291546/',
                  'https://movie.douban.com/subject/1292001/', 'https://movie.douban.com/subject/3742360/',
                  'https://movie.douban.com/subject/1849031/', 'https://movie.douban.com/subject/1929463/',
                  'https://movie.douban.com/subject/3319755/', 'https://movie.douban.com/subject/1652587/',
                  'https://movie.douban.com/subject/1292215/', 'https://movie.douban.com/subject/1292370/',
                  'https://movie.douban.com/subject/1292213/', 'https://movie.douban.com/subject/4920528/',
                  'https://movie.douban.com/subject/2129039/', 'https://movie.douban.com/subject/2131459/',
                  'https://movie.douban.com/subject/1291549/', 'https://movie.douban.com/subject/1292064/',
                  'https://movie.douban.com/subject/3011091/', 'https://movie.douban.com/subject/4739952/',
                  'https://movie.douban.com/subject/1292223/', 'https://movie.douban.com/subject/1291560/',
                  'https://movie.douban.com/subject/1889243/', 'https://movie.douban.com/subject/25662329/',
                ]

    savepage_status = True # whether or not save the douban movie subject page

    def __init__(self):
        self.max_error_count = 30  # the max num of error ,exceed the num will close the crawler
        self.error403_count = 0
        self.timeout_error_count = 0
        super().__init__()

        if DoubanmovieSpider.savepage_status and not(os.path.exists('html')):
            self.logger.debug('make the data file: html')
            os.makedirs('html')

    def start_requests(self):
        for url in self.start_urls:
            yield self.gen_request(url)

    def parse(self, response):
        if re.search('https://movie\.douban\.com/subject/\d+', response.url):
            # save the subject pages
            if self.savepage_status:
                self.save_page(response)

            yield self.get_item(response)  # get the movie item

        for url in response.xpath('//a/@href').extract():
            url = response.urljoin(url)
            if re.search('douban.com/subject/\d+', url)  or 'tag' in url:
                yield self.gen_request(url)

    def parse_err(self, failure):
        """
        deal with the error and exception
        :param failure: the failure
        :return: None
        """
        if failure.check(HttpError):
            response = failure.value.response
            url = response.request.url
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            if 'sec.douban.com' or 'misc/sorry' in response.url:
                tmp_url = unquote(response.url.split('=', maxsplit=1)[-1])
                self.logger.error('HttpError sec.douban or captcha on %s', tmp_url)
                yield self.gen_request(tmp_url, dont_filter=True)
                self.error403_count += 1
                if self.error403_count > self.max_error_count:
                    raise CloseSpider('close the spider because douban block error exceeds %d' % self.max_error_count)
            else:
                self.logger.error('HttpError  on %s', url)

        elif failure.check(DNSLookupError):
            # this is the original request
            self.logger.error('DNSLookupError on %s', failure.request.url)
            yield self.gen_request(failure.request.url, dont_filter=True)

        elif failure.check(TimeoutError, TCPTimedOutError):
            self.logger.error('TimeoutError on %s', failure.request.url)
            yield self.gen_request(failure.request.url, dont_filter=True)
            self.timeout_error_count += 1
            if self.timeout_error_count > self.max_error_count:
                raise CloseSpider('close the spider because douban block error exceeds %d' % self.max_error_count)

        else:
            self.logger.error('%s on %s' % (repr(failure), failure.request.url))


    def gen_request(self, url, **kwargs):
        """
        generate a Request
        :param url: the url to generate requests
        :return: Request
        """
        r = Request(
            url=url,
            callback=self.parse,
            errback=self.parse_err,
        )
        if 'dont_filter' in kwargs:
            r.dont_filter = True
        return r

    def save_page(self, response):
        """save the page content"""
        tmp = response.url.split('/')
        try:
            filename = 'html/' + '_'.join(tmp[-3:-1])
        except:
            filename = 'html/errorfilename'
        with open(filename, 'wb') as file:
            file.write(response.body)

    def get_item(self, response):
        """get the item from the response"""
        loader = ItemLoader(item=DoubanItem(), response=response)
        loader.add_xpath('title', '//span[@property="v:itemreviewed"]/text()')
        info = loader.nested_xpath('//div[@id="info"]')
        info.add_xpath('directors', '//a[@rel="v:directedBy"]/text()')
        info.add_xpath('writers', '/span[2]//a/text()')
        info.add_xpath('actors', '//a[@rel="v:starring"]/text()')
        info.add_xpath('types', '//span[@property="v:genre"]/text()')
        info.add_xpath('releasedate', '//span[@property="v:initialReleaseDate"]/text()')
        content = response.xpath('//div[@id="info"]/text()').extract()
        if content:
            tmp = []
            for line in content:
                line = line.strip()
                if len(line) > 1:
                    tmp.append(line)

            if len(tmp) ==5:
                loader.add_value('regions', tmp[0])
                loader.add_value('language', tmp[1])
                loader.add_value('length', tmp[2] + '*' + tmp[3])
                loader.add_value('alias', tmp[4])
            elif len(tmp) == 4:
                loader.add_value('regions', tmp[0])
                loader.add_value('language', tmp[1])
                loader.add_value('length', tmp[2])
                loader.add_value('alias', tmp[3])
            elif len(tmp) == 3:
                loader.add_value('regions', tmp[0])
                loader.add_value('language', tmp[1])
                if r'分钟' in tmp[-1]:
                    loader.add_value('length', tmp[-1])
                else:
                    loader.add_value('alias', tmp[-1])
            elif len(tmp) == 2:
                loader.add_value('regions', tmp[0])
                loader.add_value('language', tmp[1])
            else:
                loader.add_value('info', tmp)

        stars = response.xpath('//div[@class="ratings-on-weight"]//span/text()').extract()
        if stars:
            loader.add_value('stars5', stars[1])
            loader.add_value('stars4', stars[3])
            loader.add_value('stars3', stars[5])
            loader.add_value('stars2', stars[7])
            loader.add_value('stars1', stars[9])
        loader.add_xpath('scores', '//strong[@property="v:average"]/text()')
        loader.add_xpath('descriptions', '//span[@property="v:summary"]/text()')
        info.add_xpath('length', '//span[@property="v:runtime"]/text()')
        info.add_xpath('IMDblink', '//a[contains(@href,"imdb")]/@href')
        loader.add_value('url', response.url)
        loader.add_value('savetime', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return loader.load_item()

    def reader(self,filename):
        """used to parse saved response body"""
        with open(filename, 'rb') as file:
            url = 'https://movie.douban.com/subject/%s' % filename.split('_')[-1]
            content = TextResponse(url=url,body=file.read())
            return self.get_item(content)