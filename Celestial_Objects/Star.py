from Celestial_Objects import BaseCelestialObject
import math

class Star(BaseCelestialObject):
    def __init__(self, star_id, hd_id, proper_name, ra, dec, mag):
        BaseCelestialObject.__init__(self, ra, dec)
        self.star_id = star_id
        self.hd_id = hd_id
        self.proper_name = proper_name
        self.magnitude = mag
        self.radius = 0
        self.ha_time = None
        self.ha_degrees = None
        self.altitude = None
        self.azimuth = None

    def calculate_alt_az(self, dec, lat, ha_degrees, t, lon, mst):
        # ha_degrees = self.ha_time_to_degrees(ha_time)
        alt_rad = math.sin(math.radians(dec)) * math.sin(math.radians(lat)) + math.cos(math.radians(dec)) * \
                  math.cos(math.radians(lat)) * math.cos(math.radians(ha_degrees))
        alt_rad = math.asin(alt_rad)
        alt_degrees = math.degrees(alt_rad)

        # ha_degrees = self.ha_time_to_degrees(ha_time)
        az_rad = (math.sin(math.radians(dec)) - (math.sin(math.radians(alt_degrees)) * math.sin(math.radians(lat)))) / \
                 (math.cos(math.radians(alt_degrees)) * math.cos(math.radians(lat)))
        az_rad = math.acos(az_rad)
        az_degrees = math.degrees(az_rad)
        if math.sin(math.radians(ha_degrees)) < 0:
            az_degrees = az_degrees
        else:
            az_degrees = 360 - az_degrees

        return (alt_degrees, az_degrees)

    def calculate_radius(self):
        if self.magnitude <= 1.0:
            self.radius = 5.5
        elif self.magnitude <= 2.0:
            self.radius = 4.5
        elif self.magnitude <= 3.0:
            self.radius = 3.5
        elif self.magnitude <= 4.0:
            self.radius = 2.5
        elif self.magnitude <= 5.0:
            self.radius = 1.5
        elif self.magnitude <= 6.0:
            self.radius = 0.5
        else:
            self.radius = 0
