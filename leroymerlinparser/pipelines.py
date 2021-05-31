# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from scrapy.pipelines.images import ImagesPipeline
import hashlib
from scrapy.utils.python import to_bytes


class LeroymerlinparserPipeline:
    def process_item(self, item, spider):
        params_dict = {}
        for i, el in enumerate(item['params']):
            if i % 2 != 0:
                try:
                    el = float(el.strip())
                except ValueError:
                    el = el.strip()
                params_dict[item['params'][i - 1]] = el
        item['params'] = params_dict
        return item


class LeroymerlinPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except TypeError as e:
                    print(e)

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [i[1] for i in results if i[0]]
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        return f'full/{item["link"][31:-1]}/{image_guid}.jpg'
