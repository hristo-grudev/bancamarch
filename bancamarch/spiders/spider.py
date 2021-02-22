import scrapy

from scrapy.loader import ItemLoader
from ..items import BancamarchItem
from itemloaders.processors import TakeFirst


class BancamarchSpider(scrapy.Spider):
	name = 'bancamarch'
	start_urls = ['https://www.bancamarch.es/en/cargarAplicacionNoticia.do?texto=&fechaHasta=&fechaDesde=&idCategoria=0&csrfToken=40798AF64B5CDD15CB761F4F2E6009DD']

	def parse(self, response):
		post_links = response.xpath('//p[@class="nombre"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//li[@class="sigpag"]/a/@href').getall()
		yield from response.follow_all(next_page, self.parse)


	def parse_post(self, response):
		title = response.xpath('//div[@class="ficha_tipo1"]/h2/text()').get()
		description = response.xpath('//div[@class="modulo100"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="ficha_tipo1"]/p[@class="fecha"]/text()').get()

		item = ItemLoader(item=BancamarchItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
