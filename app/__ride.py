import collections
from .__ride_stats import calculate_distance

Ride = collections.namedtuple(
    'Ride', 'from_lat, from_lon, to_lat, to_lon, distance, user_id')


def create_ride(ride):
    distance = calculate_distance(ride)

    return Ride(ride['from_lat'],
                ride['from_lon'],
                ride['to_lat'],
                ride['to_lon'],
                distance,
                ride['user_id'])
