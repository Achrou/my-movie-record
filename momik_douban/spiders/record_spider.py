import scrapy
import re
from momik_douban.items import DoubanRecordItem

class RecordSpider(scrapy.Spider):
	name = "douban_record"
	start_urls = ["https://movie.douban.com/people/203204069/collect"]

	def parse(self,response):
		result = response.css('.article .grid-view div.item')
		for sel in result:
			item  = DoubanRecordItem()
			title = sel.css('.info .title a *::text').extract()
			# 处理title中无用字符
			# title = "".join(title).replace(' ', '').replace('\n','')
			# title = re.sub('', repl, string, count=0, flags=0)
			if len(title)>0:
				title = title[1:3]
				title[1] = title[1].replace('\n','').strip()
			item['title'] = "".join(title) # .replace(' / ','/').replace(' /','/').replace('/ ','/')
			item['href'] = sel.css('.info .title a::attr(href)').extract()
			item['pic'] = sel.css('.pic img::attr(src)').extract()
			item['intro'] = sel.css('.info .intro::text').extract()
			item['date'] = sel.css('.info li .date::text').extract()
			item['rating'] = sel.css('.info li:last-child span:first-of-type::attr(class)').extract()
			yield item

		next = response.css('.article .paginator span.next a::attr(href)').extract()
		if next:
			next = next[0]
			next = "https://movie.douban.com" + next
			yield scrapy.Request(url=next,callback = self.parse)
		