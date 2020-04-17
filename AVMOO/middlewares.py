# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import psycopg2
from scrapy import signals
from AVMOO.ProxyService.ProxyHolder import ProxyHolder
import scrapy.exceptions
# from AVMOO.ProxyService.Proxy import Proxy
# from twisted.internet.error import TimeoutError, DNSLookupError, \
#         ConnectionRefusedError, ConnectionDone, ConnectError, \
#         ConnectionLost, TCPTimedOutError
# from twisted.web.client import ResponseFailed
#
# from scrapy.exceptions import NotConfigured
# from scrapy.utils.response import response_status_message
# from scrapy.core.downloader.handlers.http11 import TunnelError
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

    ProxyHolder = ProxyHolder()

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        return s

    def process_request(self, request, spider):
        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called

        proxy = self.ProxyHolder.get_one()

        if proxy is None:
            if "proxy" in request.meta.keys():
                request.meta.pop("proxy")
            if "proxy_obj" in request.meta.keys():
                request.meta.pop("proxy_obj")
            delay = self.ProxyHolder.delay
            time.sleep(delay)
        else:
            request.meta['proxy_obj'] = proxy
            request.meta['proxy'] = proxy.to_string()
            proxy.last_request_time = time.time()
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
            if response.status == 403:
                if "proxy_obj" in request.meta.keys():
                    request.meta["proxy_obj"].baned = True
                    spider.logger.warning("oops! this proxy is being baned".format(request.meta["proxy"]))

            if "proxy_obj" in request.meta.keys():
                request.meta['proxy_obj'].bad_proxy()
            new_req = request.copy()
            new_req.dont_filter = True

            return new_req
        else:
            if "proxy_obj" in request.meta.keys():
                request.meta['proxy_obj'].good_proxy()
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        if "proxy_obj" in request.meta.keys():
            request.meta["proxy_obj"].bad_proxy()

        new_req = request.copy()

        new_req.dont_filter = True
        return new_req

    def spider_opened(self, spider):
        # self.ProxyProvider.updater.update()
        spider.logger.info('Spider opened: %s' % spider.name)

    def spider_closed(self, spider):
        self.ProxyHolder.save_proxy()


