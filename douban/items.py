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
    title = scrapy.Field(output_processor=TakeFirst())
    directors = Field()
    writers = Field()
    actors = Field()
    types = Field()
    regions = Field(output_processor=TakeFirst())
    language = Field(output_processor=TakeFirst())
    length = Field(output_processor=TakeFirst())
    releasedate = Field()
    descriptions = Field(
        input_processor=MapCompose(remove_blank,),
        output_processor=Join(),
    )
    IMDblink = Field(output_processor=TakeFirst())
    scores = Field(output_processor=TakeFirst())
    stars5 = Field(output_processor=TakeFirst())
    stars4 = Field(output_processor=TakeFirst())
    stars3 = Field(output_processor=TakeFirst())
    stars2 = Field(output_processor=TakeFirst())
    stars1 = Field(output_processor=TakeFirst())
    alias = Field(output_processor=TakeFirst())
    info = Field()
    url = Field(output_processor=TakeFirst())  # housekeep fileds
    savetime = Field(output_processor=TakeFirst())

