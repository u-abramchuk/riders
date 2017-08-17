from flask import Flask, request, jsonify, make_response
import collections
import pandas
import math
from scipy.spatial.distance import pdist
from .calc import distance
import random


def create_app(config_name):
    app = Flask(__name__)
    app.rides = {}
    app.N = 10

    @app.route('/')
    def index():
        return 'index'

    def _store(payload):
        user_id = str(payload['user_id'])
        payload['distance'] = distance(
            payload['from_lat'],
            payload['from_lon'],
            payload['to_lat'],
            payload['to_lon']
        )

        if not user_id in app.rides:
            app.rides[user_id] = {
                'rides': collections.deque([payload], app.N),
                'total_rides': 1,
                'M': payload['distance'],
                'S': 0
            }
        else:
            rider = app.rides[user_id]
            dist = payload['distance']
            total_rides = rider['total_rides']
            old_m = rider['M']
            old_s = rider['S']

            total_rides += 1
            m = old_m + (dist - old_m) / total_rides
            s = old_s + (dist - old_m) * (dist - m)

            rider['rides'].append(payload)
            rider['total_rides'] = total_rides
            rider['M'] = m
            rider['S'] = s

            print(payload['distance'])
            print(rider['M'])
            print(rider['S'])

    @app.route('/api/v1/store', methods=['POST'])
    def store():
        payload = request.get_json()
        _store(payload)

        return jsonify({'status': 'success'}), 201

    def _get_stats(app):
        all_records = [
            record for user_id in app.rides
            for record in app.rides[user_id]['rides']
        ]
        df = pandas.DataFrame.from_records(all_records)

        if not df.empty:
            return df.sort_values('distance').drop('distance', axis=1)
        else:
            return df

    @app.route('/api/v1/stats', methods=['GET'])
    def stats():
        df = _get_stats(app)
        csv = df.to_csv(index=False)

        output = make_response(csv)
        output.headers["Content-Disposition"] = "attachment; filename=stats.csv"
        output.headers["Content-type"] = "text/csv"

        return output

    @app.route('/api/v1/chart', methods=['GET'])
    def chart():
        all_records = [{
            'user_id': user_id,
            'num_of_rides': app.rides[user_id]['total_rides'],
            'variance': 0 if app.rides[user_id]['total_rides'] == 1 else app.rides[user_id]['S'] / (app.rides[user_id]['total_rides'] - 1)
        } for user_id in app.rides]
        print(all_records)
        df = pandas.DataFrame.from_records(all_records)
        df.plot(x='num_of_rides', y='variance')

        return 200
    if config_name == 'development':
        print('configuring')

        def get_randomized_ride():
            return {
                'user_id': str(round(10 * random.random())),
                'from_lat': 40.745392 + random.random() / 10,
                'from_lon': -73.978364 + random.random() / 10,
                'to_lat': 41.308273 + random.random() / 10,
                'to_lon': -72.927887 + random.random() / 10
            }

        records = [get_randomized_ride() for i in range(0, 300)]

        for i in range(0, 300):
            single_record = records[i]
            _store(single_record)

    return app
