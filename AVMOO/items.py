# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AV_Item(scrapy.Item):
    origin_url = scrapy.Field()     # 页面地址
    cover_url = scrapy.Field()      # 封面图片地址
    title = scrapy.Field()      # 标题
    AV_CODE = scrapy.Field()    # 番号
    publish_date = scrapy.Field()    # 发行日期
    video_length = scrapy.Field()    # 视频长度
    director = scrapy.Field()       # 导演
    studio = scrapy.Field()  # 制作商
    label = scrapy.Field()  # 发行商
    genres = scrapy.Field()  # 类别
    series = scrapy.Field()     # 系列
    stars = scrapy.Field()  # 女星
    sample_imgs = scrapy.Field()    # 样品影像


class Star_Item(scrapy.Item):
    origin_url = scrapy.Field()  # 页面地址
    cover_url = scrapy.Field()  # 封面图片地址
    name = scrapy.Field()  # 姓名
    birthday = scrapy.Field()  # 生日
    age = scrapy.Field()  # 年龄
    height = scrapy.Field()  # 身高
    cup = scrapy.Field()  # 罩杯
    bust = scrapy.Field()  # 胸围
    waist = scrapy.Field()  # 腰围
    hipline = scrapy.Field()  # 臀围
    birth_place = scrapy.Field()  # 出生地
    hobby = scrapy.Field()  # 爱好


class Genre_Item(scrapy.Item):
    title = scrapy.Field()   # 类别名称
    origin_url = scrapy.Field()  # 页面地址
    genre_group = scrapy.Field()    # 分组
