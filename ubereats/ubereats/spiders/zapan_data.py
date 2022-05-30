
#
# -*- coding: utf-8 -*-
from ubereats import db_config as dbc
import json
import re
from geopy import Nominatim
# import Nominatim as Nominatim
import Utility as Utility
import html2text as html2text
import pymongo
import scrapy
from ubereats.util import Utility


page_save1 = "E:\\uberetas pagesave\\zapan_april\\"

class InstaDataSpider(scrapy.Spider):
    name = 'zapan_data'
    i = 1
    handle_httpstatus_list = [404, 410, 401]

    db_name = dbc.db_name
    cur = db_name['link_ZP']
    cur2 = db_name['Data_ZP']

    def __init__(self, a='', b='', **kwargs):
        self.a = a
        self.b = b

    def start_requests(self):

        query = self.cur.find({'status': "Pending"})
        urls = list(query)
        print(len(urls))
        for link in urls[int(self.a):int(self.b)]:
            url1 = link['link']
            try:
                offer = link['offer']
            except Exception as e:
                offer = ''
            try:
                delivery_fee = link['delivery_fee']
            except Exception as e:
                delivery_fee = ''
            try:
                delivery_time = link['delivery_time']
            except:
                delivery_time = ''
            #
            # offer = ''
            # delivery_fee = ''
            # delivery_time = ''


            # link = url1

            # url1 = 'https://www.ubereats.com/nz/store/mcdonalds-papamoa/9j727SxLS9WosMihzy9MLw'
            link = 'http://api.scraperapi.com/?api_key=ecc27f34d621ea63ffe41feecc07c4e9' \
                   '9&keep_headers=false&premium=false&url=' + url1
            # link = 'http://api.scraperapi.com/?api_key=df1a32d04b794153ad1c51a152bf520f&keep_headers=false&premium=false&url=' + url1
            # link = 'http://api.scraperapi.com/?api_key=ec46668b42a54199b95f52ab3d9ba6f8&keep_headers=false&premium=false&url=' + url1

            header = {"Upgrade-Insecure-Requests": "1",
                      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36",
                      "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                      "Sec-Fetch-Site": "same-origin",
                      "Sec-Fetch-Mode": "navigate",
                      "Sec-Fetch-User": "?1",
                      "Sec-Fetch-Dest": "document"}
            yield scrapy.FormRequest(url=link, method='get', callback=self.get_res_detail, headers=header,meta={'delivery': delivery_time, 'offer': offer, 'delivery_fee': delivery_fee,'links': url1}, dont_filter=True)

    def get_res_detail(self, response):
        if response.status in self.handle_httpstatus_list:
           pass
        else:
            links = response.meta['links']
            try:
                item = {}
                main_cont = response.xpath('//script[@id="__REDUX_STATE__"]/text()').get(default='').strip()
                main_cont = main_cont.replace('\\u0022', '"').replace('%5C"', '').replace(' % 5 C ', '')
                data1 = response.xpath('//script[@type="application/ld+json"]//text()').get(default='')
                data = json.loads(data1)

                content = json.loads(main_cont)


                if content['stores']:

                    try:
                        link = links.split("https://www.ubereats.com/jp-en/")[1]
                        a = link.replace("-", "_").replace("/", "-")
                        AB = page_save1
                        page_save = f'{AB}{a}.html'
                        f = open(AB + str(
                            a) + '.html', 'wb')
                        f.write(main_cont.encode('utf-8'))
                        f.close()
                        print("page save")
                    except Exception as e:
                        print(e)
                        page_save = ''


                    store_key = store_id = re.findall(',"stores":\{\"(.*?)"', main_cont)[0]
                    # print(store_key)
                    stores = content['stores'][store_key]['data']
                    location_data = stores['location']

                    item['Refernce_URL'] = links

                    item['Restaurant_ID'] = store_id

                    try:
                        Restaurant_Name = data['name']
                        item['Restaurant_Name'] = Restaurant_Name
                    except Exception as e:
                        item['Restaurant_Name'] = ''
                        print(e)

                    try:
                        Desc = content['stores'][store_key]['data']['seoMeta']['description']
                        item['description'] = Desc
                    except:
                        item['description'] = ''


                    try:
                        item['Country'] = 'JP'
                    except Exception as e:
                        print(e)

                    try:
                        FullAddress = response.xpath('//a[contains(text(),"More")]/../text()[1]').get(default='')
                        item['FullAddress'] = FullAddress
                    except Exception as e:
                        item['FullAddress'] = ''
                        print(e)

                    try:
                        item['Phone'] = data['telephone']
                    except:
                        item['Phone'] = ''

                    try:
                        item['Price_Range'] = data['priceRange']
                        if item['Price_Range']:
                            item['Price_Range'] = item['Price_Range'].strip()
                    except:
                        item['Price_Range'] = ''

                    try:

                        text = html2text.HTML2Text()
                        text.ignore_images = True
                        text.ignore_links = True
                        text.ignore_emphasis = True
                        text.body_width = 0
                        text.ignore_tables = True
                        hours = response.xpath('//table/tbody').get()
                        final_hours = text.handle(hours)
                        hours2 = Utility.Beautifier(final_hours)

                        item['Hours_of_Operation'] = hours2
                    except Exception as e:
                        hours = store_id['data']['hours'][0]['dayRange']
                        print(e)

                    try:  # servesCuisine
                        cuisine = data['servesCuisine']
                        # content['stores'][store_key]['data']['cuisineList']
                        # print(cuisine)
                        item['Cuisine_Type'] = ' ,'.join(cuisine)
                    except Exception as e:
                        print(e)

                    try:
                        Rating = content['stores'][store_key]['data']['rating']['ratingValue']
                        item[
                            'Rating'] = Rating  # stores['f86d73a3-f511-4399-9e9c-6aca20ba378e'].data.rating.reviewCount
                    except Exception as e:
                        item['Rating'] = ''
                        print(e)

                    try:
                        item['review_count'] = data['aggregateRating']['reviewCount']
                        item['new_added'] = ''
                    except:
                        item['new_added'] = 'new'
                        item['review_count'] = ''

                    try:
                        No_of_Ratings = content['stores'][store_key]['data']['rating']['reviewCount']
                        item['No_of_Ratings'] = No_of_Ratings
                    except Exception as e:
                        item['No_of_Ratings'] = ''
                        print(e)

                    try:
                        item['Delivery'] = 'Y'
                    except Exception as e:
                        print(e)

                    try:
                        if 'DeliveryModePickUp' in response.text:
                            pic = 'Y'
                        else:
                            pic = ' '

                        item['Pickup_Takeout'] = pic
                    except Exception as e:
                        print(e)

                    try:
                        item['service_fee'] = stores['fareInfo']['serviceFeeCents']
                    except Exception as e:
                        item['service_fee'] = ''
                        print(e)

                    # ==========State=========================

                    item['state'] = location_data.get('region', '')
                    try:
                        state = ''.join(content['stores'][store_key]['data']['location']['region']).upper()
                        if state == '':
                            state = ''.join(content['stores'][store_key]['data']['location']['geo']['region']).upper()
                        else:
                            pass
                        item['state'] = state

                    except:
                        item['state'] = ''

                    # ==========city=========================
                    try:
                        city = ''.join(content['stores'][store_key]['data']['location']['city']).upper()
                        if city == '':
                            city = ''.join(content['stores'][store_key]['data']['location']['geo']['city']).upper()
                        else:
                            pass
                        item['city'] = city

                    except:
                        item['city'] = ''

                    # ===========Postal Code =======================

                    try:
                        item['postal_code'] = content['stores'][store_key]['data']['location']['postalCode']
                    except:
                        item['postal_code'] = ''

                    if item['postal_code'] == '':
                        item['postal_code'] = location_data.get('postalCode', '')
                    elif item['postal_code'] == '':
                        locator = Nominatim(user_agent="myGeocoder")
                        coordinates = str(item['latitude']) + ', ' + str(item['longitude'])
                        location = locator.reverse(coordinates)
                        print(location.raw)
                        ldict = location.raw

                        locator = Nominatim(user_agent="myGeocoder")
                        coordinates = str(item['latitude']) + ', ' + str(item['longitude'])
                        location = locator.reverse(coordinates)
                        print(location.raw)
                        ldict = location.raw

                        try:
                            item['postal_code'] = ldict['address']['postcode']
                        except:
                            item['postal_code'] = ''

                    address = response.xpath('//a[contains(text(),"More")]/../text()[1]').get(default='')

                    try:
                        item['street_address_1'] = content['stores'][store_key]['data']['location']['streetAddress']
                    except:
                        item['street_address_1'] = ''

                    if item['street_address_1'] == '':
                        item['street_address_1'] = location_data.get('streetAddress', '')
                        if item['street_address_1'] == '':
                            item['street_address_1'] = data['name'].split('(')[0].split(')')[0]
                    item['street_address_2'] = ''

                    if item['street_address_1'] == '':
                        address_split_params = ('unit ', 'suit ', 'ste ', 'suite ', 'units ', 'ste. ')
                        for address_split_param in address_split_params:
                            if address_split_param in (address.lower()):
                                item['street_address_1'] = \
                                (item['street_address_1'].lower()).split(address_split_param)[0]
                                item[
                                    'street_address_2'] = f"{address_split_param} {((address.lower()).split(address_split_param)[1])}"
                                break
                    item['latitude'] = location_data.get('latitude', '')
                    item['longitude'] = location_data.get('longitude', '')

                    if item['city'] == '':
                        item['city'] = location_data.get('city', '')

                    try:
                        if item['state'] == '':
                            locator = Nominatim(user_agent="myGeocoder")
                            coordinates = str(item['latitude']) + ', ' + str(item['longitude'])
                            location = locator.reverse(coordinates)
                            print(location.raw)
                            ldict = location.raw

                            locator = Nominatim(user_agent="myGeocoder")
                            coordinates = str(item['latitude']) + ', ' + str(item['longitude'])
                            location = locator.reverse(coordinates)
                            print(location.raw)
                            ldict = location.raw

                            try:
                                item['state'] = ldict['address']['state']
                                item['postal_code'] = ldict['address']['postcode']
                            except:
                                item['state'] = ''




                        elif item['city'] == '':
                            locator = Nominatim(user_agent="myGeocoder")
                            coordinates = str(item['latitude']) + ', ' + str(item['longitude'])
                            location = locator.reverse(coordinates)
                            print(location.raw)
                            ldict = location.raw

                            try:
                                item['city'] = ldict['address']['city']
                            except:
                                item['city'] = ''
                                if item['city'] == '':
                                    try:
                                        item['city'] = ldict['address']['town']
                                    except:
                                        try:

                                            item['city'] = ldict['address']['village']
                                        except:
                                            item['city'] = location_data.get('city', '')

                    except Exception as e:
                        print(e)

                    try:
                        item['Offer'] = response.meta['offer']
                    except Exception as e:
                        print(e)

                    item['HtmlPath'] = page_save
                    yield item

                    try:
                        self.cur2.insert(dict(item))
                        print("Insertedd child3..")
                    except Exception as e:
                        print("Error in Insertion child3-->", e)

                    try:
                        self.cur.update({'link': links}, {"$set": {"status": 'done'}})
                        print("link updated")
                    except Exception as e:
                        print(e, "error in done pending")


            except Exception as e:
                print(e)



if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl zapan_data -a a=0 -a b=10000'.split())
