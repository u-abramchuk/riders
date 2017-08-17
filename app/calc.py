import math


def distance(from_lat, from_lon, to_lat, to_lon):
    def to_rad(degrees):
        return degrees * math.pi / 180

    from_lat_rad = to_rad(from_lat)
    from_lon_rad = to_rad(from_lon)
    to_lat_rad = to_rad(to_lat)
    to_lon_rad = to_rad(to_lon)

    R = 6371

    return R * math.sqrt((from_lat_rad - to_lat_rad)**2 + (to_lon_rad - from_lon_rad)**2 * (math.cos((from_lat_rad + to_lat_rad) / 2))**2)
