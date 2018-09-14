import googlemaps


class GoogleDistance():
    def __init__(self, key):
        self.gmaps = googlemaps.Client(key=key)

    def distance_by_mode(self, origin, destinations, travelmode):
        dist_matrix = self.gmaps.distance_matrix(origin, destinations,
                                                 mode=travelmode,
                                                 language="en-GB",
                                                 avoid="tolls",
                                                 units="metric")
        
        travel_time = [e['duration']['value'] for row in dist_matrix['rows'] for e in row['elements']]
        return travel_time

    def get_distance(self, from_coord, to_coord):
        travelmodes = ["walking", "transit", "driving"]
        travel_dist = [self.distance_by_mode(from_coord, to_coord, travelmode) for travelmode in travelmodes]
        return travel_dist