# -*- coding: utf-8 -*-

# Scrapy settings for AVMOO project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import time

# Retry many times since proxies often fail
RETRY_TIMES = 5
# Retry on most error codes since proxies fail for different reasons
RETRY_HTTP_CODES = [500, 503, 504, 403, 400, 404, 408]

BOT_NAME = 'AVMOO'

SPIDER_MODULES = ['AVMOO.spiders']
NEWSPIDER_MODULE = 'AVMOO.spiders'

DOWNLOAD_TIMEOUT = 10

# HTTPERROR_ALLOW_ALL = True

# JOBDIR = 'JOB'

# LOG_ENABLED = True  # 是否启动日志记录，默认True
# LOG_ENCODING = 'UTF-8'
# # LOG_FILE = None
# LOG_FILE = 'AVMOO_SPIDER_{}.LOG'.format(time.strftime("%Y-%m-%d", time.localtime()))  # 日志输出文件，如果为NONE，就打印到控制台
# LOG_LEVEL = 'WARNING'  # 日志级别，默认debug


# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'Mozilla/5.0 (Windows NT 9.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 64

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 64
CONCURRENT_REQUESTS_PER_IP = 64

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'AVMOO.middlewares.AvmooSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'AVMOO.middlewares.AvmooDownloaderMiddleware': 543,
   'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': None,
   'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
   # 'AVMOO.middlewares.GenreDownloadFilterMiddleWare': 100,
   # 'AVMOO.randomproxy.RandomProxy': 100,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
EXTENSIONS = {
   # 'scrapy.extensions.telnet.TelnetConsole': None,
   'scrapy.extensions.logstats.LogStats': None,
   'AVMOO.extensions.SpeedLogExtension': 100,
}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   # 'AVMOO.pipelines.AvmooPipeline': 300,
   'AVMOO.pipelines.GenreItemPipeline': 100,
   'AVMOO.pipelines.AVStarItemPipeline': 200,
   'AVMOO.pipelines.AVItemPipeline': 300,

}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
