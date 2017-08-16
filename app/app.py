from flask import Flask, request, jsonify, make_response
import collections
import pandas
from scipy.spatial.distance import pdist


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

        if not user_id in app.rides:
            app.rides[user_id] = {
                'rides': collections.deque([payload], app.N),
                'total_rides': 1
            }
        else:
            app.rides[user_id]['rides'].appendleft(payload)
            app.rides[user_id]['total_rides'] += 1

        return jsonify({'status': 'success'}), 201

    def _get_stats(app):
        all_records = [
            record for user_id in app.rides for record in app.rides[user_id]['rides']]
        df = pandas.DataFrame.from_records(all_records)
        dist = df.apply(lambda x: pdist(
            [[x.from_lat, x.from_lon], [x.to_lat, x.to_lon]])[0], axis=1)
        # dist = ((df['from_lat'] - df['to_lat'])**2 +
        #         (df['from_lon'] - df['to_lon'])**2)**0.5
        if not dist.empty:
            df = df.assign(dist=dist).sort_values('dist').drop('dist', axis=1)

        return df

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
