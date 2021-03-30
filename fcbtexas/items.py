import scrapy


class FcbtexasItem(scrapy.Item):
    title = scrapy.Field()
    description = scrapy.Field()
