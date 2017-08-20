import collections
import math
from .__rider_stats import RiderStats
from .__ride import create_ride


class Rider:
    def __init__(self, user_id, N):
        self.user_id = user_id
        self.rides = collections.deque([], N)
        self.stats = RiderStats()

    def add_ride(self, new_ride):
        ride = create_ride(new_ride)

        self.rides.append(ride)
        self.stats.new_ride(ride.distance)
