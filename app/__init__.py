from flask import Flask, request, jsonify, make_response
import collections
import pandas


def create_app(config_name):
    app = Flask(__name__)
    app.rides = {
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
        '2':[{
            'user_id': '2',
            'from_lat': 50.745392,
            'from_lon': -73.978364,
            'to_lat': 41.308273,
            'to_lon': -72.927887
        }]
    }
    app.N = 10

    @app.route('/')
    def index():
        return 'index'

    @app.route('/api/v1/store', methods=['POST'])
    def store():
        payload = request.get_json()
        user_id = str(payload['user_id'])

        if not user_id in app.rides:
            app.rides[user_id] = collections.deque([payload], app.N)
        else:
            app.rides[user_id].appendleft(payload)

        return jsonify({'status': 'success'}), 201

    @app.route('/api/v1/stats', methods=['GET'])
    def stats():
        all_records = [record for user_id in app.rides for record in app.rides[user_id]]
        df = pandas.DataFrame.from_records(all_records)

        output = make_response(df.to_csv(index=False))
        output.headers["Content-Disposition"] = "attachment; filename=stats.csv"
        output.headers["Content-type"] = "text/csv"
        return output

    return app
