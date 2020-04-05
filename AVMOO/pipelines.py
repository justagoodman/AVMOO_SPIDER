# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import psycopg2
import scrapy.exceptions
import logging
import json
from .items import AV_Item, Star_Item, Genre_Item


class AvmooPipeline(object):
    def process_item(self, item, spider):
        return item


class DataBasePipeline(object):
    connection = None
    cursor = None

    def open_spider(self, spider):
        hostname = 'localhost'
        port = '5432'
        password = '964719978'
        database = 'postgres'
        username = 'postgres'
        self.connection = psycopg2.connect(database="Scrapy",
                                           user="postgres",
                                           password="964719978",
                                           host="127.0.0.1",
                                           port="5432")
        self.cursor = self.connection.cursor()

    def close_spider(self, spider):
        self.cursor.close()
        self.connection.close()

    def process_item(self, item, spider):
        pass

    @staticmethod
    def _get_key_value_str(item):
        keys = item.keys()
        key_str = ""
        value_str = ""
        for key in keys:
            if key == "AV_CODE":
                key_str = key_str + '"' + key + '", '
            else:
                key_str = key_str + key + ", "

            obj_to_str = json.dumps(item[key], ensure_ascii=False)
            if (obj_to_str[0] == '{') | (obj_to_str[0] == '['):
                obj_to_str = "'" + obj_to_str + "'"
            else:
                obj_to_str = obj_to_str[1:-1]
                obj_to_str = "'" + obj_to_str + "'"
            value_str = value_str + obj_to_str + ", "

        key_str = key_str[:-2]
        value_str = value_str[:-2]

        return {
            "key_str": key_str,
            "value_str": value_str
        }

    def item_to_sql(self, item):
        key_value = self._get_key_value_str(item)
        sql = ""
        if isinstance(item, Genre_Item):
            sql = '''
                                                INSERT INTO public."AVMOO_GENRE"(
                                    	        {}
                                    	            )
                                    	        VALUES ({});
                                                '''.format(
                key_value['key_str'],
                key_value['value_str']
            )
        elif isinstance(item, Star_Item):
            sql = '''
                                    INSERT INTO public."AVMOO_STAR"(
                        	        {}
                        	            )
                        	        VALUES ({});
                                    '''.format(
                key_value['key_str'],
                key_value['value_str']
            )

        elif isinstance(item, AV_Item):
            sql = '''
                                            INSERT INTO public."AVMOO_AV"(
                                	        {})
                                	        VALUES ({});
                                            '''.format(
                key_value['key_str'],
                key_value['value_str']
            )

        return sql


class GenreItemPipeline(DataBasePipeline):
    def process_item(self, item, spider):
        if not isinstance(item, Genre_Item):
            return item
        keys = item.keys()
        if len(keys) != 3:
            raise scrapy.exceptions.DropItem("not enough key")
        else:
            sql = self.item_to_sql(item)
            try:
                self.cursor.execute(sql)
                self.connection.commit()
                logging.info("++++++++++ insert one GENRE ITEM record ++++++++++")
                logging.info(item)
            except Exception as e:
                self.connection.rollback()
                # logging.warning("++++++++++ insert GENRE ITEM failed ++++++++++")
                # logging.warning(e)
        return item


class AVStarItemPipeline(DataBasePipeline):
    def process_item(self, item, spider):
        if not isinstance(item, Star_Item):
            return item
        # 处理item中的字段，将其序列化成符合pg格式的字符串
        keys = item.keys()
        if ("origin_url" in keys) & ("name" in keys):
            sql = self.item_to_sql(item)
            try:
                self.cursor.execute(sql)
                self.connection.commit()
                logging.info("++++++++++ insert one STAR ITEM record ++++++++++")
                logging.info(item)
            except Exception as e:
                self.connection.rollback()
                logging.warning("++++++++++ insert STAR ITEM failed ++++++++++")
                logging.warning(e)
        else:
            raise scrapy.exceptions.DropItem("not enough p_keys")
        return item


class AVItemPipeline(DataBasePipeline):
    def process_item(self, item, spider):
        if not isinstance(item, AV_Item):
            return item
        keys = item.keys()
        if ("origin_url" in keys) & ("title" in keys):
            sql = self.item_to_sql(item)
            try:
                self.cursor.execute(sql)
                self.connection.commit()
                logging.info("++++++++++ insert one AV ITEM record ++++++++++")
                logging.info(item)
            except Exception as e:
                self.connection.rollback()
                logging.warning("++++++++++ insert AV ITEM failed ++++++++++")
                logging.warning(e)
        else:
            raise scrapy.exceptions.DropItem("not enough p_keys")
        return item
