from Celestial_Objects import BaseCelestialObject
import math

class MessierObject(BaseCelestialObject):
    def __init__(self, ra, dec):
        BaseCelestialObject.__init__(self, ra, dec)
        # A type so that the GUI knows the correct "sprite" to display?
        self.type = None


    # Same as Star
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
