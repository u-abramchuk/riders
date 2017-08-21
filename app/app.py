from flask import Flask, request, jsonify, make_response
import pandas
from scipy.spatial.distance import pdist
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from collections import namedtuple
from ._store import Store
from ._bootstrapper import bootstrap

matplotlib.use('Agg')

def create_app():
    app = Flask(__name__)

    app.config.from_envvar('APP_SETTINGS')
    app.N = app.config['N']
    app.store = Store(app.N)

    @app.route('/')
    def index():
        return 'riders'

    @app.route('/api/v1/store', methods=['POST'])
    def store():
        payload = request.get_json()
        app.store.store(payload)

        return jsonify({'status': 'success'}), 201

    def _get_stats(app):
        all_records = [
            record._asdict() for user_id in app.store.riders
            for record in app.store.riders[user_id].rides
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
        all_riders = [{
            'user_id': user_id,
            'num_of_rides': app.store.riders[user_id].stats.rides_count,
            'variance': app.store.riders[user_id].stats.get_variance()
        } for user_id in app.store.riders]
        df = pandas.DataFrame.from_records(all_riders)

        fig, ax = plt.subplots(1)
        
        if not df.empty:
            scatterplot = df.plot.scatter(x='num_of_rides', y='variance', ax=ax)

        def annotate_df(row):
            ax.annotate(row.user_id, (row.num_of_rides, row.variance),
                        xytext=(10, -5),
                        textcoords='offset points')

        ab = df.apply(annotate_df, axis=1)
        img = io.BytesIO()
        canvas = FigureCanvas(fig)
        png_output = io.BytesIO()
        canvas.print_png(png_output)

        response = make_response(png_output.getvalue())
        response.headers['Content-Type'] = 'image/png'
        
        return response

    if app.config['DEVELOPMENT']:
        # generate some sample data
        bootstrap(app)

    return app
