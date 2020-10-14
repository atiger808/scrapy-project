# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem

class UmeiPipeline:
    def process_item(self, item, spider):
        return item

class MyImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        img_link = item["img_link"]
        yield scrapy.Request(img_link)
    
    def item_completed(self, results, item, info):
        image_paths = [x["path"] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item["img_paths"] = image_paths
        return item