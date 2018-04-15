from Celestial_Objects import BaseCelestialObject
import math


class MessierObject(BaseCelestialObject):
    def __init__(self, messier_cat, ra_hour, ra_min, ra_sec, dec_deg, dec_min, dec_sec, mag, name, desc):
        BaseCelestialObject.__init__(self, None, None)
        self.magnitude = float(mag)
        self.proper_name = name
        self.description = desc
        self.messier_cat = messier_cat
        self.right_ascension = self.degrees_to_decimal(ra_hour, ra_min, ra_sec)
        self.declination = self.degrees_to_decimal(dec_deg, dec_min, dec_sec)
        self.altitude = None

    # Same as Star
    def calculate_alt_az(self, dec, lat, ha_degrees, t, lon, mst):
        # ha_degrees = self.ha_time_to_degrees(ha_time)
        alt_rad = math.sin(math.radians(dec)) * math.sin(math.radians(lat)) + math.cos(math.radians(dec)) * \
                  math.cos(math.radians(lat)) * math.cos(math.radians(ha_degrees))
        alt_rad = math.asin(alt_rad)
        alt_degrees = math.degrees(alt_rad)
        self.altitude = alt_degrees

        # ha_degrees = self.ha_time_to_degrees(ha_time)
        az_rad = (math.sin(math.radians(dec)) - (math.sin(math.radians(alt_degrees)) * math.sin(math.radians(lat)))) / \
                 (math.cos(math.radians(alt_degrees)) * math.cos(math.radians(lat)))
        az_rad = math.acos(az_rad)
        az_degrees = math.degrees(az_rad)
        if math.sin(math.radians(ha_degrees)) < 0:
            az_degrees = az_degrees
        else:
            az_degrees = 360 - az_degrees

        return alt_degrees, az_degrees

    def degrees_to_decimal(self, ra_hour, ra_min, ra_sec):
        hours = int(ra_hour)
        minutes = int(ra_min)
        seconds = int(ra_sec)
        ra_time_decimal = hours + (minutes / 60) + (seconds / 3600)
        return ra_time_decimal
