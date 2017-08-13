from flask import Flask, request, jsonify
import collections


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
            app.rides[user_id] = collections.deque([payload], app.N)
        else:
            app.rides[user_id].appendleft(payload)

        return jsonify({'status': 'success'}), 201

    return app
