import scrapy

from scrapy.loader import ItemLoader

from ..items import FcbtexasItem
from itemloaders.processors import TakeFirst


class FcbtexasSpider(scrapy.Spider):
	name = 'fcbtexas'
	start_urls = ['https://www.fcbtexas.com/blog/']

	def parse(self, response):
		post_links = response.xpath('//a[@class="biglink biglink--primary"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="blog__content"]//text()[normalize-space() and not(ancestor::div[@class="blog__content--back"])]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()

		item = ItemLoader(item=FcbtexasItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)

		return item.load_item()
