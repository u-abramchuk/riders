from .__rider import Rider


class Store:
    def __init__(self, N):
        self.riders = {}
        self.__N = N

    def store(self, ride):
        user_id = ride['user_id']
        
        if not user_id in self.riders:
            self.riders[user_id] = Rider(user_id, self.__N)

        self.riders[user_id].add_ride(ride)
