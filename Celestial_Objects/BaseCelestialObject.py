from abc import ABCMeta, abstractmethod
import math


class BaseCelestialObject:
    __metaclass__ = ABCMeta

    def __init__(self, ra, dec):
        self.right_ascension = ra
        self.declination = dec
        self.x = None
        self.y = None
        self.canvas_id = None
        self.canvas_x = None
        self.canvas_y = None
        self.offset_x = None
        self.offset_y = None

    def get_xy_coords(self, alt, az, r):
        # self.x = r * math.sin(math.radians(alt)) * math.cos(math.radians(az))
        # self.y = r * math.sin(math.radians(alt)) * math.sin(math.radians(az))

        self.x = self.canvas_x = -1*(1000 * math.cos(math.radians(az)) * math.tan(math.radians(90 - alt) / 2))
        self.y = self.canvas_y = 1000 * math.sin(math.radians(az)) * math.tan(math.radians(90 - alt) / 2)
        return self.x, self.y

    def calculate_ha_time(self, lst, ra):
        ha_time = lst - ra
        if ha_time < 0:
            while ha_time < 0:
                ha_time += 24
        elif ha_time > 24:
            while ha_time > 24:
                ha_time = ha_time - 24
        return ha_time

    def ra_degrees_to_time_decimal(self, ra):
        hours = int(ra / 15.0)
        minutes = int(((ra / 15.0) - hours) * 60)
        seconds = ((((ra / 15.0) - hours) * 60.0) - minutes) * 60
        # print('hh:mm:ss: ' + str(hours) + ' ' + str(minutes) + ' ' + str(seconds))
        ra_time_decimal = hours + (minutes / 60) + (seconds / 3600)
        return ra_time_decimal

    def ha_time_to_degrees(self, ha_time):
        ha_degrees_hours = int(ha_time * 15)
        ha_degrees_minutes = (((ha_time * 15) - ha_degrees_hours))
        ha_degrees_seconds = ((((ha_time * 15) - ha_degrees_hours)) - ha_degrees_minutes)
        ha_degrees = ha_degrees_hours + ha_degrees_minutes + ha_degrees_seconds
        return ha_degrees

    # Converts Right Ascension (ra) in degrees to Hours:Minutes:Seconds
    def convert_ra_mhs(self, ra):
        hours = int(ra / 15.0)
        minutes = int(((ra / 15.0) - hours) * 60.0)
        seconds = ((((ra / 15.0) - hours) * 60.0) - minutes) * 60.0
        return hours, minutes, seconds

    # Converts Declination (dec) in degress to Degrees:Minutes:Seconds
    def convert_dec_dms(self, dec):
        degrees = int(dec)
        minutes = int((dec - degrees) * 60.0)
        seconds = (((dec - degrees) * 60.0) - minutes) * 60.0
        return degrees, minutes, seconds

    def rev(self, x):
        return x - math.floor(x / 360.0) * 360.0

    # Convert an angle above 360 degrees to one less than 360
    def mod2pi(self, x):
        b = x / 2 * math.pi
        a = (math.pi * 2) * (b - self.abs_floor(b))
        if a < 0:
            a += (2 * math.pi)
        converted_angle = a
        return converted_angle

    def abs_floor(self, b):
        if b >= 0:
            floor = math.floor(b)
        else:
            floor = math.ceil(b)
        return floor


    @abstractmethod
    def calculate_alt_az(self, dec, lat, ha_degrees, t, lon, mst):
        pass


    # Functions for testing
    def testing_alt(self, dec, lat, ha_time):
        ha_degrees = self.ha_time_to_degrees(ha_time)
        alt_rad = math.sin(math.radians(dec)) * math.sin(math.radians(lat)) + math.cos(math.radians(dec)) * \
                  math.cos(math.radians(lat)) * math.cos(math.radians(ha_degrees))
        alt_rad = math.asin(alt_rad)
        alt_degrees = math.degrees(alt_rad)
        return alt_degrees

    def testing_az(self, dec, lat, ha_time, alt):
        ha_degrees = self.ha_time_to_degrees(ha_time)
        # print('ha degrees dd: ' + str(ha_degrees))
        az_rad = (math.sin(math.radians(dec)) - (math.sin(math.radians(alt)) * math.sin(math.radians(lat)))) / \
                 (math.cos(math.radians(alt)) * math.cos(math.radians(lat)))
        az_rad = math.acos(az_rad)
        az_degrees = math.degrees(az_rad)
        if math.sin(math.radians(ha_degrees)) < 0:
            az_degrees = az_degrees
        else:
            az_degrees = 360 - az_degrees
        return az_degrees

    # example of how to do make an abstract method
    # @abstractmethod
    # def example(self):
    #     pass