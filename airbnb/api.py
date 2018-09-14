import requests
import json
from urlparse import urljoin

API_KEY = None
# API_KEY = "None"

URL = "https://api.airbnb.com/v2/"


class API():
    def __init__(self):
        self._session = requests.Session()

        self._session.headers = {
            "accept": "application/json",
            "accept-encoding": "gzip, deflate",
            "content-type": "application/json",
            "user-agent": "Airbnb/18.23 AppVersion/18.23 iPhone/12.0 Type/Phone",
            "x-airbnb-device-id": "9120210f8fb1ae837affff54a0a2f64da821d227",
            "x-airbnb-advertising-id": "16CE6BF7-90CC-41A8-8305-B7B3183A2787",
            "x-airbnb-carrier-name": "T-Mobile",
            "x-airbnb-network-type": "wifi",
            "x-airbnb-currency": "USD",
            "x-airbnb-locale": "en",
            "x-airbnb-carrier-country": "us",
            "accept-language": "en-us"
        }

    def search_listing(self, num_guest=1, location=None, min_bathrooms=0,
                       min_bedrooms=0, min_beds=1, price_min=10, price_max=200,
                       limit=100, offset=0, user_lat=None, user_lng=None):
        SEARCH_URL = urljoin(URL, "search_results")

        params = {
            "currency": "GBP",
            "_format": "for_search_results_with_minimal_pricing",
            "_limit": limit,
            "_offset": offset,
            "guests": num_guest,
            "client_id": API_KEY,
            "ib": False, # instant bookable
            "min_bathrooms": min_bathrooms,
            "min_bedrooms": min_bedrooms,
            "min_beds": min_beds,
            "price_min": price_min,
            "price_max": price_max,
            "min_num_pic_urls": 5,
            "sort": 1
            }

        if location:
            params['location'] = location.replace(' ', '%20')

        elif user_lat and user_lng:
            params['user_lat'] = user_lat
            params['user_lng'] = user_lng

        return self._session.get(SEARCH_URL, params=params).json()

    def get_listing_info(self, listing_id):
        LISTINGS_URL = urljoin(URL, "listings/{}".format(listing_id))

        params = {"client_id": API_KEY,
                  "_format": "v1_legacy_for_p3"}

        self.listing_info = self._session.get(LISTINGS_URL, params=params).json()
        return self.listing_info

    def get_rating_summary(self):
        listing = self.listing_info['listing']
        return {k: v for k, v in listing.iteritems() if k.startswith("review")}

    def get_listing_summary(self):
        listing = self.listing_info['listing']
        summary = ['min_nights', 'name', 'bathrooms', 'bedrooms', 'beds', 'lat', 'lng', 'neighborhood', 'city', 'person_capacity', 'property_type', 'room_type', 'rate']
        return {s: listing[s] for s in summary}
