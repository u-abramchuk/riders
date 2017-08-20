import unittest
import json
from app import create_app
import pandas
from scipy.spatial.distance import pdist
import random
import math
from app.__ride_stats import calculate_distance
from app.__rider_stats import RiderStats


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client

    def test_distance_calculation(self):
        ride = {
            'user_id': '1',
            'from_lat': 40.745392,
            'from_lon': -73.978364,
            'to_lat': 41.308273,
            'to_lon': -72.927887
        }
        distance = calculate_distance(ride)
        self.assertEqual(distance, 108.0859922018123)

    def test_variance_calculation(self):
        distances = [108.085992,112.438246,195.151068]
        stats = RiderStats()
        for distance in distances:
            stats.new_ride(distance)
        self.assertAlmostEqual(stats.get_variance(), 2406.7800828283)

    def test_store(self):
        """Test store"""
        single_record = {
            'user_id': '1',
            'from_lat': 40.745392,
            'from_lon': -73.978364,
            'to_lat': 41.308273,
            'to_lon': -72.927887
        }

        response = self._post('/api/v1/store', single_record)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.app.store.riders['1'].stats.rides_count, 1)

        ride = self.app.store.riders['1'].rides[0]
        self.assertEqual(ride.from_lat, single_record['from_lat'])
        self.assertEqual(ride.from_lon, single_record['from_lon'])
        self.assertEqual(ride.to_lat, single_record['to_lat'])
        self.assertEqual(ride.to_lon, single_record['to_lon'])
        self.assertAlmostEqual(ride.distance, 108.0859922018123)

    def test_store_no_more_than_N(self):
        """Test store more than N records"""

        def get_randomized_ride():
            return {
                'user_id': '1',
                'from_lat': 40.745392 + random.random(),
                'from_lon': -73.978364 + random.random(),
                'to_lat': 41.308273 + random.random(),
                'to_lon': -72.927887 + random.random()
            }

        records = [get_randomized_ride() for i in range(0, self.app.N + 1)]

        for i in range(0, self.app.N + 1):
            single_record = records[i]
            response = self._post('/api/v1/store', single_record)
            self.assertEqual(response.status_code, 201)

        for i in range(0, self.app.N):
            rider = self.app.store.riders['1']
            actual = rider.rides[i]
            expected = records[i + 1]
            self.assertEqual(actual.from_lat, expected['from_lat'])
            self.assertEqual(actual.from_lon, expected['from_lon'])
            self.assertEqual(actual.to_lat, expected['to_lat'])
            self.assertEqual(actual.to_lon, expected['to_lon'])
        self.assertEqual(len(rider.rides), self.app.N)
        self.assertEqual(rider.stats.rides_count, self.app.N + 1)

    def test_stats(self):
        rides = [
            {
                'user_id': '1',
                'from_lat': 39.745392,
                'from_lon': -73.978364,
                'to_lat': 41.308273,
                'to_lon': -72.927887
            },
            {
                'user_id': '1',
                'from_lat': 40.745392,
                'from_lon': -73.978364,
                'to_lat': 41.308273,
                'to_lon': -72.927887
            },
            {
                'user_id': '2',
                'from_lat': 41.945392,
                'from_lon': -73.978364,
                'to_lat': 41.308273,
                'to_lon': -72.927887
            }
        ]
        self.app.N = 10

        self._post('/api/v1/store', rides[0])
        self._post('/api/v1/store', rides[1])
        self._post('/api/v1/store', rides[2])

        response = self.client().get('/api/v1/stats')

        expected = b'from_lat,from_lon,to_lat,to_lon,user_id\n40.745392,-73.978364,41.308273,-72.927887,1\n41.945392,-73.978364,41.308273,-72.927887,2\n39.745392,-73.978364,41.308273,-72.927887,1\n'

        self.assertEqual(response.data, expected)

    def _post(self, url, data):
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = self.client().post(url, data=json.dumps(data), headers=headers)

        return response


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
