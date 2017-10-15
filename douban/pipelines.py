# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem


class DoubanPipeline(object):

    def __init__(self):
        pass

    def process_item(self, item, spider):
        return item

        if not item.get('title', None):
            raise DropItem
        else:
            return item

