import scrapy
import time
from momik_douban.items import DoubanRecordItem


class RecordSpider(scrapy.Spider):
    name = "douban_record"
    start_urls = ["https://movie.douban.com/people/203204069/collect", "https://movie.douban.com/people/203204069/wish",
                  "https://movie.douban.com/people/203204069/do"]

    def parse(self, response):
        result = response.css('.article .grid-view div.item')
        for sel in result:
            item = DoubanRecordItem()
            title = sel.css('.info .title a *::text').extract()
            # 处理title中无用字符
            # title = "".join(title).replace(' ', '').replace('\n','')
            # title = re.sub('', repl, string, count=0, flags=0)
            if len(title) > 0:
                title = title[1:3]
                title[1] = title[1].replace('\n', '').strip()
            item['title'] = "".join(title)  # .replace(' / ','/').replace(' /','/').replace('/ ','/')
            item['href'] = sel.css('.info .title a::attr(href)')[0].extract()
            item['pic'] = sel.css('.pic img::attr(src)')[0].extract()
            item['intro'] = sel.css('.info .intro::text')[0].extract()
            item['date'] = sel.css('.info li .date::text')[0].extract()
            item['type'] = response.url.split('/')[-1].split('?')[0]
            item['rating'] = ''
            item['comment'] = ''
            if item['type'] == 'collect':
                rating = sel.css('.info li:nth-child(3) span[class^="rating"]::attr(class)')
                if len(rating):
                    item['rating'] = rating[0].extract()
                comment = sel.css('.info li span.comment::text')
                if len(comment):
                    item['comment'] = comment[0].extract()
            item["modiTime"] = time.time()
            yield item

        next = response.css('.article .paginator span.next a::attr(href)').extract()
        if next:
            next = next[0]
            next = "https://movie.douban.com" + next
            yield scrapy.Request(url=next, callback=self.parse)
