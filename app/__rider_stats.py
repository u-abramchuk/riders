class RiderStats:
    def __init__(self):
        self.__M = 0
        self.__S = 0
        self.rides_count = 0

    def new_ride(self, distance):
        self.rides_count += 1

        if self.rides_count == 1:
            self.__M = distance
            self.__S = 0
        else:
            old_m = self.__M
            self.__M += (distance - old_m) / self.rides_count
            self.__S += (distance - old_m) * (distance - self.__M)
    
    def get_variance(self):
        return 0 if self.rides_count <= 1 else self.__S / (self.rides_count - 1)
