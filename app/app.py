from flask import Flask, request, jsonify, make_response
import collections
import pandas
import math
from scipy.spatial.distance import pdist
from .calc import distance


def create_app(config_name):
    app = Flask(__name__)
    app.rides = {}
    app.N = 10

    @app.route('/')
    def index():
        return 'index'

    @app.route('/api/v1/store', methods=['POST'])
    def store():
        payload = request.get_json()
        user_id = str(payload['user_id'])
        payload['distance'] = distance(
            payload['from_lat'], payload['from_lon'], payload['to_lat'], payload['to_lon'])

        if not user_id in app.rides:
            app.rides[user_id] = {
                'rides': collections.deque([payload], app.N),
                'total_rides': 1
            }
        else:
            app.rides[user_id]['rides'].append(payload)
            app.rides[user_id]['total_rides'] += 1

        return jsonify({'status': 'success'}), 201

    def _get_stats(app):
        all_records = [
            record for user_id in app.rides
            for record in app.rides[user_id]['rides']
        ]
        df = pandas.DataFrame.from_records(all_records)

        return df.sort_values('distance').drop('distance', axis=1)

    @app.route('/api/v1/stats', methods=['GET'])
    def stats():
        df = _get_stats(app)
        csv = df.to_csv(index=False)

        output = make_response(csv)
        output.headers["Content-Disposition"] = "attachment; filename=stats.csv"
        output.headers["Content-type"] = "text/csv"
        return output

    return app

    @app.route('/api/v1/chart', method=['GET'])
    def chart():
        pass
