from abc import ABCMeta, abstractmethod
import math


class BaseCelestialObject:
    __metaclass__ = ABCMeta

    def __init__(self):
        self.right_ascension = None
        self.declination = None
        self.x = None
        self.y = None

    def get_xy_coords(self, alt, az, r):
        self.x = r * math.sin(math.radians(alt)) * math.cos(math.radians(az))
        self.y = r * math.sin(math.radians(alt)) * math.sin(math.radians(az))
        return self.x, self.y

    def calculate_alt(self, dec, lat, ha_degrees):
        # ha_degrees = self.ha_time_to_degrees(ha_time)
        alt_rad = math.sin(math.radians(dec)) * math.sin(math.radians(lat)) + math.cos(math.radians(dec)) * \
                  math.cos(math.radians(lat)) * math.cos(math.radians(ha_degrees))
        alt_rad = math.asin(alt_rad)
        alt_degrees = math.degrees(alt_rad)
        return alt_degrees

    def calculate_az(self, dec, lat, ha_degrees, alt):
        # ha_degrees = self.ha_time_to_degrees(ha_time)
        az_rad = (math.sin(math.radians(dec)) - (math.sin(math.radians(alt)) * math.sin(math.radians(lat)))) / \
                 (math.cos(math.radians(alt)) * math.cos(math.radians(lat)))
        az_rad = math.acos(az_rad)
        az_degrees = math.degrees(az_rad)
        if math.sin(math.radians(ha_degrees)) < 0:
            az_degrees = az_degrees
        else:
            az_degrees = 360 - az_degrees
        return az_degrees

    def calculate_ha_time(self, lst, ra):
        ha_time = lst - ra
        if ha_time < 0:
            while ha_time < 0:
                ha_time += 24
        elif ha_time > 24:
            while ha_time > 24:
                ha_time = ha_time - 24
        return ha_time

    def ha_time_to_degrees(self, ha_time):
        ha_degrees_hours = int(ha_time * 15)
        ha_degrees_minutes = (((ha_time * 15) - ha_degrees_hours))
        ha_degrees_seconds = ((((ha_time * 15) - ha_degrees_hours)) - ha_degrees_minutes)
        ha_degrees = ha_degrees_hours + ha_degrees_minutes + ha_degrees_seconds
        return ha_degrees

    # example of how to do make an abstract method
    # @abstractmethod
    # def example(self):
    #     pass


class Planet(BaseCelestialObject):
    def __init__(self):
        BaseCelestialObject.__init__(self)
        self.planet_name = None
        self.ascal = None
        self.aprop = None
        self.escal = None
        self.eprop = None
        self.iscal = None
        self.iprop = None
        self.wscal = None
        self.wprop = None
        self.oscal = None
        self.oprop = None
        self.lscal = None
        self.lprop = None
        self.semi_axis = None
        self.eccentricity = None
        self.inclination = None
        self.arg_perihelion = None
        self.long_asc_node = None
        self.mean_long = None
        self.mean_anomaly = None
        self.true_anomaly = None


class Star(BaseCelestialObject):
    def __init__(self, star_id, hd_id, proper_name, ra, dec, mag):
        BaseCelestialObject.__init__(self)
        self.star_id = star_id
        self.hd_id = hd_id
        self.proper_name = proper_name
        self.right_ascension = ra
        self.declination = dec
        self.magnitude = mag
        self.ha_time = None
        self.ha_degrees = None
        self.altitude = None
        self.azimuth = None



class Moon(BaseCelestialObject):
    def __init__(self):
        BaseCelestialObject.__init__(self)
        self.phase = None


class Constellation(BaseCelestialObject):
    def __init__(self, name, star_list):
        BaseCelestialObject.__init__(self)
        self.name = name
        self.star_list = star_list
        self.number_stars = None
        self.number_lines = None


class Messier_Objects(BaseCelestialObject):
    def __init__(self):
        BaseCelestialObject.__init__(self)
        # A type so that the GUI knows the correct "sprite" to display?
        self.type = None
