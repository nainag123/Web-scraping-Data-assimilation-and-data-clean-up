# -*- coding: utf-8 -*-

import scrapy
import pycountry
import uuid
from locations.categories import Code
from locations.items import GeojsonPointItem


class SKECHERSSpider(scrapy.Spider):
    
    name = "skechers_ind_dpa"
    brand_name = "SKECHERS"
    spider_type = "chain"
    spider_chain_id = "4226"
    spider_categories = [
        Code.CLOTHING_AND_ACCESSORIES.value
    ]
    spider_countries = [
        pycountry.countries.lookup("IND").alpha_3
    ]

    # List of coordinates for major cities in India where Zara stores are likely to be located
    coordinates = [
        (28.6139, 77.2090),  # Delhi
        (19.0760, 72.8777),  # Mumbai
        (12.9716, 77.5946),  # Bangalore
        (22.5726, 88.3639),  # Kolkata
        (13.0827, 80.2707),  # Chennai
        (17.3850, 78.4867),  # Hyderabad
        (23.0225, 72.5714),  # Ahmedabad
        (18.5204, 73.8567),  # Pune
        (26.9124, 75.7873),  # Jaipur
        (30.7333, 76.7794),  # Chandigarh
        (22.3072, 73.1812),  # Vadodara
        (19.9975, 73.7898),  # Nashik
        (21.1458, 79.0882),  # Nagpur
        (26.8467, 80.9462),  # Lucknow
        (22.7196, 75.8577),  # Indore
        (25.3176, 82.9739),  # Varanasi
        (11.0168, 76.9558),  # Coimbatore
        (15.2993, 74.1240),  # Goa
        (9.9312, 76.2673),   # Kochi
        (8.5241, 76.9366),   # Thiruvananthapuram
        (15.8281, 78.0373),  # Kadapa
        (10.8505, 76.2711),  # Palakkad
        (13.6288, 79.4192),  # Tirupati
        (11.6234, 78.1270),  # Salem
        (11.3410, 77.7172),  # Erode
        (14.4426, 79.9865),  # Nellore
        (12.2958, 76.6394),  # Mysore
        (21.1702, 72.8311),  # Surat
        (22.3039, 70.8022),  # Rajkot
        (18.1124, 79.0193),  # Warangal
        (24.5854, 73.7125),  # Udaipur
        (24.8135, 93.9500),  # Imphal
        (25.5788, 91.8933),  # Shillong
        (26.1445, 91.7362),  # Guwahati
        (23.3441, 85.3096),  # Ranchi
        (23.8103, 91.2820),  # Agartala
        (25.0340, 88.1325),  # Maldah
        (22.5688, 88.3478)   # Howrah
    ]

    def start_requests(self):
        for lat, lng in self.coordinates:
            url = f"https://www.skechers.in/on/demandware.store/Sites-skechersin-Site/default/Stores-FindStores?showMap=true&radius=3000&city=&lat={lat}&long={lng}"
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response):
        stores = response.json().get('stores', [])
        
        for store in stores:
            mappedAttributes = {
                'chain_name': self.brand_name,
                'chain_id': self.spider_chain_id,
                'ref': store.get('ID'),
                'addr_full': f"{store.get('address1', '')}, {store.get('address2', '')}".strip(', '),
                'city': store.get('city', '').strip(', '),
                'state': store.get('stateCode', ''),
                'postcode': store.get('postalCode', ''),
                'phone': store.get('phone', ''),
                'email': store.get('email', ''),
                'opening_hours': store.get('storeHours', '').replace("\n", " "),
                'website': f"https://www.skechers.in/store-locator/Skechers/?sid={store.get('ID')}",
                'lat': store.get('latitude'),
                'lon': store.get('longitude'),
            }

            yield GeojsonPointItem(**mappedAttributes)
