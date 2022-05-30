import random
import pymongo
import scrapy
from ubereats import db_config as dbc
class UberLinkSpider(scrapy.Spider):
    name = 'zapana_categorylink'
    allowed_domains = ['example.com']
    i=1
    start_urls = ['http://www.example.com/']

    db_name = dbc.db_name
    cur = db_name['citylink_ZP']
    cur1 = db_name['categorylink_ZP']

    unique = cur1.create_index("link", unique=True)

    def __init__(self, name=None, start='', end='', **kwargs):
        super().__init__(name, **kwargs)
        self.start = start
        self.end = end

    def start_requests(self):

        query = self.cur.find({'status':"pending"})
        urls = list(query)
        print(len(urls))

        for row in urls:
            links1 = row['City']

            # link = 'http://api.scraperapi.com/?api_key=df1a32d04b794153ad1c51a152bf520f&keep_headers=false&premium=false&url=' + links1
            link = 'http://api.scraperapi.com/?api_key=ec46668b42a54199b95f52ab3d9ba6f8&keep_headers=false&premium=false&url=' + links1

            if '?' in link:
                links=link.split('?')[0]
            header={"Upgrade-Insecure-Requests": "1",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36",
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                        "Sec-Fetch-Site": "same-origin",
                        "Sec-Fetch-Mode": "navigate",
                        "Sec-Fetch-User": "?1",
                        "Sec-Fetch-Dest": "document"}
            yield scrapy.FormRequest(url=link,callback=self.parse,dont_filter=True,headers=header,meta={'link':links1})


    def parse(self,response):

        link12 = response.meta['link']
        if response.status == 200:
            cat = response.xpath("//*[contains(text(),'View all')]/@href").getall()
            for i in cat:
                if 'category' in i:
                    url = 'https://www.ubereats.com'+i
                    url = 'http://api.scraperapi.com/?api_key=df1a32d04b794153ad1c51a152bf520f&keep_headers=false&premium=false&url=' + url

                    yield scrapy.Request(url=url,callback=self.parse1,dont_filter=True,meta={'link':link12})
                else:
                    pass

    def parse1(self,response):
        item = {}
        link13 = response.meta['link']
        if response.status == 200:
            cat_link = response.xpath('//*[@id="main-content"]//a//@href').getall()
            for j in cat_link:
                link = 'https://www.ubereats.com'+str(j)
                item['link'] = link
                item['status'] = 'pending'

                yield item

                try:
                    self.cur1.insert(dict(item))
                    print("Insertedd child3..")
                except Exception as e:
                    print("Error in Insertion child3-->", e)


            try:
                self.cur.update({'City': link13}, {"$set": {"status": 'done'}})
                print("link updated")
            except Exception as e:
                print(e, "error in done pending")


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl zapana_categorylink'.split())#-a start=0 -a end=4000
