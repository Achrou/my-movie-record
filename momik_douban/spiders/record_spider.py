import scrapy
from momik_douban.items import DoubanRecordItem

class RecordSpider(scrapy.Spider):
	name = "douban_record"
	start_urls = ["https://movie.douban.com/people/203204069/collect"]

	def parse(self,response):
		result = response.css('.article .grid-view div.item')
		next = response.css('.article .paginator span.next a::attr(href)')
		if ("/" in next):
			next = "https://movie.douban.com" + next
			# yield scrapy.Request(url=next)
		for sel in result:
			item  = DoubanRecordItem()
			item['title'] = sel.css('.info .title a *::text').extract()
			# item['href'] = sel.css('.info .title a::attr(href)').extract()
			# item['pic'] = sel.css('.pic img::attr(src)').extract()
			# item['intro'] = sel.css('.info .intro::text').extract()
			# item['date'] = sel.css('.info li .date::text').extract()
			# item['rating'] = sel.css('.info li:last-child span:first-of-type::attr(class)').extract()
			yield item
