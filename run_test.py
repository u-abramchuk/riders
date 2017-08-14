import unittest
import json
from app import create_app
import pandas
# from scipy.spatial.distance import pdist

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.single_record = {
            'user_id': '1',
            'from_lat': 40.745392,
            'from_lon': -73.978364,
            'to_lat': 41.308273,
            'to_lon': -72.927887
        }

    def test_store(self):
        """Test store"""
        response = self._post('/api/v1/store', self.single_record)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.app.rides['1'][0], self.single_record)

    def test_store_no_more_than_N(self):
        """Test store more than N records"""
        for i in range(0, self.app.N + 1):
            response = self._post('/api/v1/store', self.single_record)
            self.assertEqual(response.status_code, 201)
        self.assertEqual(len(self.app.rides['1']), self.app.N)

    def test_pdist(self):
        self.app.rides = {
            '1': [{
                'user_id': '1',
                'from_lat': 30.745392,
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
            }],
            '2': [{
                'user_id': '2',
                'from_lat': 50.745392,
                'from_lon': -73.978364,
                'to_lat': 41.308273,
                'to_lon': -72.927887
            }]
        }
        self.app.N = 10

        all_records = [point for user_id in self.app.rides
                       for record in self.app.rides[user_id]
                       for point in [
                           {'lat': record['from_lat'], 'lon': record['from_lon'],
                            'user_id': record['user_id'], 'point': 'from'},
                           {'lat': record['to_lat'], 'lon': record['to_lon'],
                            'user_id': record['user_id'], 'point': 'to'}
                       ]
                       ]
        df = pandas.DataFrame.from_records(all_records)
        # df1 = df.groupby(['user_id', 'point'])[['lat', 'lon']].apply(lambda g: pandas.Series(distance.pdist(g), index=['dist']))
        print(df.to_csv(index=False))

    def _post(self, url, data):
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = self.client().post(url, data=json.dumps(data), headers=headers)

        return response


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
