from Celestial_Objects import BaseCelestialObject
import math


class Planet(BaseCelestialObject):
    def __init__(self, planet_name, lscal, lprop, ascal, aprop, escal, eprop, iscal, iprop, wscal, wprop, oscal, oprop):
        BaseCelestialObject.__init__(self, None, None)
        self.proper_name = planet_name
        self.ascal = ascal
        self.aprop = aprop
        self.escal = escal
        self.eprop = eprop
        self.iscal = iscal
        self.iprop = iprop
        self.wscal = wscal
        self.wprop = wprop
        self.oscal = oscal
        self.oprop = oprop
        self.lscal = lscal
        self.lprop = lprop
        self.semi_axis = None
        self.eccentricity = None
        self.inclination = None
        self.arg_perihelion = None
        self.long_asc_node = None
        self.mean_long = None
        self.mean_anomaly = None
        self.true_anomaly = None
        self.alt = None
        self.az = None
        self.distance = None
        self.ha = None

    def calculate_alt_az(self, ra, lat, dec, lon, mst):
        if lat < 0:
            lat *= -1.0
        if lon < 0:
            lon *= -1.0

        # hour_angle = calculate_mst(year, month, day, hour, minute, 0, lat, lon)
        hour_angle = mst - ra
        if hour_angle < 0:
            hour_angle += 360

        # Convert degrees to radians
        dec_rad = math.radians(dec)
        lat_rad = math.radians(lat)
        ha_rad = math.radians(hour_angle)

        # Calculate altitude in radians
        sin_alt = (math.sin(dec_rad) * math.sin(lat_rad)) + (math.cos(dec_rad) * math.cos(lat_rad) * math.cos(ha_rad))
        alt = math.asin(sin_alt)

        # Calculate azimuth in radians
        try:
            cos_az = (math.sin(dec_rad) - math.sin(lat_rad)) / (math.cos(alt) * math.cos(lat_rad))
            az = math.acos(cos_az)
        except:
            az = 0

        # Convert alt and az to degrees
        alt = math.degrees(alt)
        az = math.degrees(az)
        if math.sin(ha_rad) > 0.0:
            az = 360.0 - az

        return (alt, az)

    # calculate semimajor axis of the orbit
    def calculate_semi_axis(self, pl_name, ascal, aprop, cy):
        if pl_name == "Mercury" or pl_name == "Venus" or pl_name == "Jupiter" or pl_name == "Uranus":
            return float(ascal) + float(aprop) * cy
        else:
            return float(ascal) - float(aprop) * cy

    # calculate eccentricity of the orbit
    def calculate_eccentricity(self, pl_name, escal, eprop, cy):
        if pl_name == "Mercury" or pl_name == "Mars" or pl_name == "Neptune" or pl_name == "Pluto":
            return float(escal) + float(eprop) * cy
        else:
            return float(escal) - float(eprop) * cy

    # calculate inclination on the plane of the ecliptic
    def calculate_inclination(self, pl_name, iscal, iprop, cy):
        if pl_name == "Jupiter" or pl_name == "Saturn" or pl_name == "Pluto":
            return math.radians(float(iscal) + float(iprop) * cy / 3600)
        else:
            return math.radians(float(iscal) - float(iprop) * cy / 3600)

    # calculate argument of perihelion
    def calculate_arg_perihelion(self, pl_name, wscal, wprop, cy):
        if pl_name == "Venus" or pl_name == "Saturn" or pl_name == "Neptune" or pl_name == "Pluto":
            return math.radians(float(wscal) - float(wprop) * cy / 3600)
        else:
            return math.radians(float(wscal) + float(wprop) * cy / 3600)

    # calculate longitude of ascending node
    def calculate_long_asc_node(self, pl_name, oscal, oprop, cy):
        if pl_name == "Jupiter":
            return math.radians(float(oscal) + float(oprop) * cy / 3600)
        else:
            return math.radians(float(oscal) - float(oprop) * cy / 3600)

    # calculate mean longitude of a planet
    def calculate_mean_longitude(self, lscal, lprop, cy):
        return self.mod2pi(math.radians(float(lscal) + float(lprop) * cy / 3600))


    # calculate eccentric anomaly of a planet
    def calculate_eccentric_anomaly(self):
        pass

    # calculate true anomaly of a planet
    def calculate_true_anomaly(self, mean_anomaly, eccentricity):
        E = mean_anomaly + eccentricity * math.sin(mean_anomaly) * (1.0 + eccentricity * math.cos(mean_anomaly))
        E1 = 0
        while (abs(E - E1) > (1.0 * eccentricity - 12)):
            E1 = E
            E = E1 - (E1 - eccentricity * math.sin(E1) - mean_anomaly) / (1 - eccentricity * math.cos(E1))
            if (abs(E - E1) > (1.0 * eccentricity - 12)):
                break
        V = 2 * math.atan(math.sqrt(1 + eccentricity) / (1 - eccentricity)) * math.tan(0.5 * E)
        while (V < 0):
            V = V + (math.pi * 2)
        return V

    # calculate right ascension and declination of a planet
    def calculate_ra_dec_planet(self, pl_name, pl_axis, pl_eccentricity, pl_inclination,
                                pl_arg_perihelion, pl_long_asc_node, pl_mean_long, e_axis,
                                e_eccentricity, e_inclination, e_arg_perihelion, e_long_asc_node, e_mean_long):

        # calculate the position of the Earth in its orbit
        e_mean_anomaly = self.mod2pi(e_mean_long - e_arg_perihelion)
        e_v = self.calculate_true_anomaly(e_mean_anomaly, math.radians(e_eccentricity))
        e_r = math.radians(e_axis * (1 - math.pow(e_eccentricity, 2)) / (1 + e_eccentricity * math.cos(e_v)))

        # calculate the heliocentric rectangular coordinates of Earth
        e_x = e_r * math.cos(e_v + e_arg_perihelion)
        e_y = e_r * math.sin(e_v + e_arg_perihelion)
        e_z = 0.0

        # calculate the position of the planet in its' orbit
        pl_mean_anomaly = self.mod2pi(pl_mean_long - pl_arg_perihelion)
        pl_v = self.calculate_true_anomaly(pl_mean_anomaly, math.radians(pl_eccentricity))
        pl_r = math.radians(pl_axis * (1 - math.pow(pl_eccentricity, 2)) / (1 + pl_eccentricity * math.cos(pl_v)))

        # calculate the heliocentric rectangular coordinates of the planet
        pl_xh = pl_r * (math.cos(pl_long_asc_node) * math.cos(pl_v + pl_arg_perihelion - pl_long_asc_node)
                        - math.sin(pl_long_asc_node) * math.sin(pl_v + pl_arg_perihelion - pl_long_asc_node)
                        * math.cos(pl_inclination))
        pl_yh = pl_r * (math.sin(pl_long_asc_node) * math.cos(pl_v + pl_arg_perihelion - pl_long_asc_node)
                        + math.cos(pl_long_asc_node) * math.sin(pl_v + pl_arg_perihelion - pl_long_asc_node)
                        * math.cos(pl_inclination))
        pl_zh = pl_r * (math.sin(pl_v + pl_arg_perihelion - pl_long_asc_node) * math.sin(pl_inclination))

        if pl_name == "Earth/Sun":
            pl_xh = pl_yh = pl_zh = 0
        # if Earth/Sun set all to 0.0

        # convert to geocentric rectangular coordinates
        xg = pl_xh - e_x
        yg = pl_yh - e_y
        zg = pl_zh - e_z

        # rotate around X axis from ecliptic to equatorial coordinates
        ecl = math.radians(23.439281)
        xeq = xg
        yeq = yg * math.cos(ecl) - zg * math.sin(ecl)
        zeq = yg * math.sin(ecl) + zg * math.cos(ecl)

        # calculate right ascension and declination from the rectangular equatorial coordinates
        # also calculates distance in AUs
        ra = math.degrees(self.mod2pi(math.atan2(yeq, xeq)))
        dec = math.degrees(math.atan(zeq / math.sqrt(math.pow(xeq, 2) + math.pow(yeq, 2))))
        dist = math.sqrt(math.pow(xeq, 2) + math.pow(yeq, 2) + math.pow(zeq, 2))

        return (ra, dec, dist)
