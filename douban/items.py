# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field
from scrapy.loader.processors import MapCompose, Join, TakeFirst
import string


def remove_blank(content):
    return content.strip()


class DoubanItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    directors = Field()
    writers = Field()
    actors = Field()
    types = Field()
    regions = Field()
    language = Field()
    marketing = Field()
    length = Field()
    alias = Field()
    descriptions = Field(
        input_processor=MapCompose(remove_blank,),
        output_processor=Join()
    )
    IMDblink = Field()
    scores = Field()
    stars5 = Field()
    stars4 = Field()
    stars3 = Field()
    stars2 = Field()
    stars1 = Field()
    url = Field()  # housekeep fileds
    savetime = Field()

