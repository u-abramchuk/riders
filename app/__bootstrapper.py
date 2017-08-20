import random

def bootstrap(app):
    def get_randomized_ride():
        return {
            'user_id': str(round(10 * random.random())),
            'from_lat': 40.745392 + random.random() / 10,
            'from_lon': -73.978364 + random.random() / 10,
            'to_lat': 41.308273 + random.random() / 10,
            'to_lon': -72.927887 + random.random() / 10
        }

    rides = [get_randomized_ride() for i in range(0, 1000)]

    for ride in rides:
        app.store.store(ride)