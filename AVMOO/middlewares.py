# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import psycopg2
from scrapy import signals
from AVMOO.ProxyService.ProxyProvider import ProxyProvider
import scrapy.exceptions
from AVMOO.ProxyService.Proxy import Proxy
from twisted.internet.error import TimeoutError, DNSLookupError, \
        ConnectionRefusedError, ConnectionDone, ConnectError, \
        ConnectionLost, TCPTimedOutError
from twisted.web.client import ResponseFailed

from scrapy.exceptions import NotConfigured
from scrapy.utils.response import response_status_message
from scrapy.core.downloader.handlers.http11 import TunnelError
import time


class AvmooSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class AvmooDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    ProxyProvider = ProxyProvider()

    def __init__(self):
        self.DownloadDelay = 1

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        if len(self.ProxyProvider.proxies) == 0:
            delay = self.DownloadDelay
        else:
            delay = self.DownloadDelay/len(self.ProxyProvider.proxies)
        proxy = self.ProxyProvider.get_proxy()
        request.meta['proxy_obj'] = proxy
        request.meta['proxy'] = proxy.to_string()
        time.sleep(delay)
        # return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        # # 如果返回的response状态不是200，重新生成当前request对象
        if response.status != 200:
            if response.status == 404:
                raise scrapy.exceptions.IgnoreRequest('404 Page Not Found')
            if request.meta['proxy_obj'] is not None:
                request.meta['proxy_obj'].bad_proxy()
            # proxy = self.ProxyProvider.get_proxy()
            new_req = request.copy()
            new_req.dont_filter = True
            # new_req.meta['proxy_obj'] = proxy
            # new_req.meta['proxy'] = proxy.to_string()
            return new_req
        else:
            if request.meta['proxy_obj'] is not None:
                request.meta['proxy_obj'].good_proxy()
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.
        # if 'proxy' not in request.meta:
        #     return
        proxy_obj = request.meta['proxy_obj']
        if isinstance(exception, (TunnelError, ConnectionRefusedError, ConnectionAbortedError, TCPTimedOutError,
                                  TimeoutError)):
            print(exception, "exception to loose")

            if request.meta['proxy_obj'] is not None:
                request.meta['proxy_obj'].bad_proxy()

        elif isinstance(exception, (ConnectionLost, ConnectionResetError)):
            print(exception, "exception to retry")

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain

        new_req = request.copy()
        # proxy = self.ProxyProvider.get_proxy()
        # if proxy is not None:
        #     new_req.meta['proxy_obj'] = proxy
        #     new_req.meta['proxy'] = proxy.to_string()
        new_req.dont_filter = True
        # print("using proxy ", new_req.meta['proxy'])
        # new_req.priority = request.priority
        # request.meta["exception"] = True
        return new_req
        #  return request.__setitem__("proxy", self.ProxyProvider.get_proxy())

    def spider_opened(self, spider):
        # self.ProxyProvider.updater.update()
        spider.logger.info('Spider opened: %s' % spider.name)


class GenreDownloadFilterMiddleWare(object):

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.
        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        # sql = '''SELECT title, origin_url, genre_group FROM public."AVMOO_GENRE" WHERE origin_url = '{}';'''.format(request.url)
        # result = self.cursor.execute(sql)
        # if result is not None:
        #     spider.logger.info("already in records")
        #     raise scrapy.exceptions.IgnoreRequest("already in records")
        # request.meta['proxy'] = self.ProxyProvider.get_proxy()
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

