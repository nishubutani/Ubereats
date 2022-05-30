import pymongo
import scrapy
from ubereats import db_config as dbc
class UberLinkSpider(scrapy.Spider):
    name = 'zapan_link'
    allowed_domains = ['example.com']
    i = 1
    start_urls = ['http://www.example.com/']
    handle_httpstatus_list = [404, 410, 401]

    db_name = dbc.db_name
    cur = db_name['categorylink_ZP']
    cur1 = db_name['link_ZP']
    unique = cur1.create_index("link", unique=True)

    def __init__(self, name=None, a='', b='', **kwargs):
        super().__init__(name, **kwargs)
        self.a = a
        self.b = b

    def start_requests(self):

        query = self.cur.find({'status':"pending"})
        # query = self.cur.find({}).skip(1).limit(1)
        urls = list(query)
        print(len(urls))

        for row in urls[int(self.a):int(self.b)]:
            links1 = row['link']
            print(links1)

            # url = 'http://api.scraperapi.com/?api_key=df1a32d04b794153ad1c51a152bf520f&keep_headers=true&premium=false&url=' + links
            url = 'http://api.scraperapi.com/?api_key=ec46668b42a54199b95f52ab3d9ba6f8&keep_headers=true&premium=false&url=' + links1
            # url =  links
            if '?' in links1:
                links = links1.split('?')[0]
            header = {
                        "Upgrade-Insecure-Requests": "1",
                      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36",
                      "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                      "Sec-Fetch-Site": "same-origin",
                      "Sec-Fetch-Mode": "navigate",
                      "Sec-Fetch-User": "?1",
                      "Sec-Fetch-Dest": "document"

                      }
            yield scrapy.FormRequest(url=url, callback=self.get_cat_list, dont_filter=True, headers=header,
                                     meta={'link': links1, 'id': '' })


    def get_cat_list(self, response):
        if response.status in self.handle_httpstatus_list:
            links = response.meta['link']
            pass
        else:
            links = response.meta['link']
            if response.status == 200:
                divs = response.xpath('//div[@class="ag cf"]')

                for div in divs:
                    try:
                        link = div.xpath('.//a/@href').get(default='')
                        item = {}

                        link = 'https://www.ubereats.com' + link.encode('ascii','ignore').decode('utf8')
                        try:
                            # offer = div.xpath('.//div[@class="bt bu ba bb cc hf bj hg hh dq hi he hj"]//text()').get(default='')
                            offer = div.xpath('.//div[@class="bt bu ba bb cc ho bj hp hq e0 hr hn hs"]//text()').get(default='')
                        except Exception as e:
                            offer = ''
                            print(e)

                        if '$0 Delivery Fee' in offer:
                            item['subscription_eligible'] = 'Yes'
                        else:
                            item['subscription_eligible'] = 'No'#//div[@class="an al di"]//span//text()

                        try:
                            delivery_fee = div.xpath('.//span[contains(text(),"Delivery fee is")]//text()').get(default='')
                            delivery_fee = delivery_fee.split(" ")[-1].strip()
                            if delivery_fee == '':
                                delivery_fee = div.xpath('.//div[contains(text(),"Delivery Fee^")]//text()|.//span[contains(text(),"Delivery Fee^")]//text()|.//span[contains(text(),"Delivery Fee")]//text()').get(default='')
                                delivery_fee = delivery_fee.split(" ")[0].strip()
                        except Exception as e:
                            delivery_fee = ''
                            print(e)

                        try:
                            delivery_time = div.xpath('.//div[contains(text(),"min")]//text()|.//span[contains(text(),"min")]//text()').get(default='')
                        except Exception as e:
                            delivery_time = ''
                            print(e)

                        item['link'] = link
                        item['offer'] = offer
                        item['delivery_fee'] = delivery_fee
                        item['delivery_time'] = delivery_time
                        item['status'] = 'Pending'
                        yield item
                    except Exception as e:
                        pass
                        print(e)

                    try:
                        self.cur1.insert(dict(item))
                        print("Insertedd child3..")
                    except Exception as e:
                        print("Error in Insertion child3-->", e)

                try:
                    self.cur.update({'link': links}, {"$set": {"status": 'done'}})
                    print("link updated")
                except Exception as e:
                    print(e, "error in done pending")


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl zapan_link -a a=0 -a b=10000'.split())
