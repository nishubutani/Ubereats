from ubereats import db_config as dbc
import requests
import scrapy
from scrapy.http import HtmlResponse

def get_useragent():
    pass
    # software_names = [SoftwareName.CHROME.value]
    # operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
    # user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems,limit=100)
    # return user_agent_rotator.get_random_user_agent()


class UberCitySpider(scrapy.Spider):
    name = 'australiya_city'
    allowed_domains = ['www.example.com']
    i=1
    start_urls = ['https://quotes.toscrape.com/']
    handle_httpstatus_list = [403]


    db_name = dbc.db_name
    cur = db_name['citylink_AU']
    unique = cur.create_index("City", unique=True)


    def parse(self, response):


        header = {"Upgrade-Insecure-Requests": "1",
                  "User-Agent": get_useragent(),
                  "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                  "Sec-Fetch-Site": "same-origin",
                  "Sec-Fetch-Mode": "navigate",
                  "Sec-Fetch-User": "?1",
                  "Sec-Fetch-Dest": "document"}

        link='https://www.ubereats.com/au/location'
        res=requests.get(url=link,headers=header)
        res=HtmlResponse(url=link,body=res.content)
        if res.status ==200:
            links5=res.xpath('//a[contains(@href,"/city")]//@href').getall()
            for link6 in links5:
                link6=f'https://www.ubereats.com{link6}'
                item = {}
                item['City']=link6
                item['status'] = 'pending'
                yield item

                try:
                    self.cur.insert(dict(item))
                    print("Insertedd child3..")
                except Exception as e:
                    print("Error in Insertion child3-->", e)

                yield scrapy.FormRequest(
                    url=link6,callback=self.get_city, dont_filter=True, headers=header)

    def get_city(self,response):
        header = {"Upgrade-Insecure-Requests": "1",
                  "User-Agent": get_useragent(),
                  "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                  "Sec-Fetch-Site": "same-origin",
                  "Sec-Fetch-Mode": "navigate",
                  "Sec-Fetch-User": "?1",
                  "Sec-Fetch-Dest": "document"}

        links = response.xpath('//h2[contains(text(),"Nearby cities")]/../../following-sibling::div//a//@href').getall()
        for link in links:
            link = f'https://www.ubereats.com{link}'
            item = {}
            item['City'] = link
            item['status'] = 'pending'
            yield item

            try:
                self.cur.insert(dict(item))
                print("Insertedd child3..")
            except Exception as e:
                print("Error in Insertion child3-->", e)
            yield scrapy.FormRequest(
                url=link, callback=self.get_city_1, dont_filter=True, headers=header)

    def get_city_1(self,response):
        header = {"Upgrade-Insecure-Requests": "1",
                  "User-Agent": get_useragent(),
                  "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                  "Sec-Fetch-Site": "same-origin",
                  "Sec-Fetch-Mode": "navigate",
                  "Sec-Fetch-User": "?1",
                  "Sec-Fetch-Dest": "document"}

        links = response.xpath('//h2[contains(text(),"Nearby cities")]/../../following-sibling::div//a//@href').getall()
        for link in links:
            link = f'https://www.ubereats.com{link}'
            item = {}
            item['City'] = link
            item['status'] = 'pending'
            yield item

            try:
                self.cur.insert(dict(item))
                print("Insertedd child3..")
            except Exception as e:
                print("Error in Insertion child3-->", e)
            yield scrapy.FormRequest(
                url=link, callback=self.get_city_2, dont_filter=True, headers=header)

    def get_city_2(self,response):
        header = {"Upgrade-Insecure-Requests": "1",
                  "User-Agent": get_useragent(),
                  "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                  "Sec-Fetch-Site": "same-origin",
                  "Sec-Fetch-Mode": "navigate",
                  "Sec-Fetch-User": "?1",
                  "Sec-Fetch-Dest": "document"}

        links = response.xpath('//h2[contains(text(),"Nearby cities")]/../../following-sibling::div//a//@href').getall()
        for link in links:
            link = f'https://www.ubereats.com{link}'
            item = {}
            item['City'] = link
            item['status'] = 'pending'
            yield item

            try:
                self.cur.insert(dict(item))
                print("Insertedd child3..")
            except Exception as e:
                print("Error in Insertion child3-->", e)


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl australiya_city'.split())
