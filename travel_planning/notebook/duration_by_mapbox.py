from mapbox import DirectionsMatrix, Directions
from geojson import Point, Feature


class MapboxDistance():
    def __init__(self, key):
        self.service = DirectionsMatrix(access_token=key)

    def duration_by_mode(self, origin, destination, service, travelmode):
        """returns origin-dest and dest-origin in seconds"""
        resp = self.service.matrix([Feature(geometry=Point(origin)),
                                    Feature(geometry=Point(destination))],
                                   profile='mapbox/{}'.format(travelmode))

        rate_limit = resp.headers['X-Rate-Limit-Limit']

        response = resp.json()
        if "durations" in response:
            durations = response['durations']
            return sum(durations[0]), sum(durations[1])
        else:
            print("SOMETHING WRONG: ", response)

    def get_duration(self, from_coord, to_coord, service):
        travelmodes = ["walking", "driving"]
        travel_dist = [self.duration_by_mode(from_coord, to_coord, service, travelmode) for travelmode in travelmodes]
        return travel_dist
