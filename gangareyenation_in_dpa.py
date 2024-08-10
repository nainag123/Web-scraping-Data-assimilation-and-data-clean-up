import scrapy
import pycountry
import uuid
from locations.categories import Code
from locations.items import GeojsonPointItem

class GangaReyeNationSpider(scrapy.Spider):
    name = "gangareyenation_dac"
    brand_name = "Gangar Eyenation"
    spider_type = "chain"
    spider_chain_id = "23945"
    spider_categories = [
        Code.OPTICAL.value
    ]
    spider_countries = [
        pycountry.countries.lookup("IN").alpha_3
    ]
    start_urls = [
        'https://www.gangareyenation.com/wp-admin/admin-ajax.php?action=asl_load_stores&nonce=d5b458912e&load_all=1&layout=1'
    ]

    def parse(self, response):
        list_of_places = response.json()
        
        for place in list_of_places:
            mappedAttributes = {
                'chain_name': self.brand_name,
                'chain_id': self.spider_chain_id,
                'ref': uuid.uuid4().hex,
                # 'addr_full': place.get('street') + ' ' + place.get('city') + ', ' + place.get('state') + ', ' + place.get('postal_code') + ', ' + place.get('country'),
                'street' : place.get('street', ''),
                'city': place.get('city',''),
                'state': place.get('state',''),
                'postcode': place.get('postal_code',''),
                'country' : place.get('country', ''),
                'phone': place.get('phone',''),
                'email': place.get('email', ''),
                'opening_hours': place.get('open_hours', ''),
                'website': place.get('website', ''),
                'lat': place.get('lat',''),
                'lon': place.get('lng',''),
            }

            yield GeojsonPointItem(**mappedAttributes)

