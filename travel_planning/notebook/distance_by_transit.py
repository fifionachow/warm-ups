import requests

from operator import itemgetter
from duration_by_mapbox import MapboxDistance

md = MapboxDistance(mapbox_api_key)

def get_closest_transit(lat, lon, service):
    r = requests.get('http://transit.land/api/v1/stops.geojson?lon={}&lat={}&r=200'.format(lon, lat))
    features = r.json()['features']
    close_stops = {feature["properties"]["onestop_id"]: md.duration_by_mode((lon, lat), feature['geometry']["coordinates"], service=service, travelmode="walking")[0] for feature in features}
    return sorted(close_stops.items(), key=itemgetter(1))[0]

def get_transit_duration():
    return