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

    def calculate_alt_az(self, ra, dec, lat, ha_degrees, t, lon, mst):
        if lat < 0:
            lat *= -1.0
        if lon < 0:
            lon *= -1.0

        #hour_angle = calculate_mst(year, month, day, hour, minute, 0, lat, lon)
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

        # Convert altitude and azimuth to degrees
        alt = math.degrees(alt)
        az = math.degrees(az)

        if math.sin(ha_rad) > 0.0:
            az = 360.0 - az

        return (alt, az)

    # calculate semimajor axis of the orbit
    def calculate_semi_axis(self, ascal, aprop, cy):
        return float(ascal) + float(aprop) * cy

    # calculate eccentricity of the orbit
    def calculate_eccentricity(self, escal, eprop, cy):
        return float(escal) + float(eprop) * cy

    # calculate inclination on the plane of the ecliptic
    def calculate_inclination(self, iscal, iprop, cy):
        # return math.radians(float(iscal) - float(iprop) * cy / 3600)
        return math.radians(float(iscal) - float(iprop) * cy / 3600)

    # calculate argument of perihelion
    def calculate_arg_perihelion(self, wscal, wprop, cy):
        return math.radians(float(wscal) + float(wprop) * cy / 3600)

    # calculate longitude of ascending node
    def calculate_long_asc_node(self, oscal, oprop, cy):
        return math.radians(float(oscal) - float(oprop) * cy / 3600)

    # calculate mean longitude of a planet
    def calculate_mean_longitude(self, lscal, lprop, cy):
         # return mod2pi(math.radians(float(lscal) + float(lprop) * cy / 3600))
        mean_long = math.radians(float(lscal) + float(lprop) * cy / 3600)
         # mean_long = float(lscal) + float(lprop) * cy / 3600
        # mean_long_rads = mean_long_rads % (math.pi*2)
        mean_long = mean_long % (2 * math.pi)
        return mean_long

    # calculate mean anomaly of a planet
    def calculate_mean_anomaly(self, planet_name, d):
        if planet_name == "Mercury":
            return (168.6562 + 4.0923344368 * d) % 360
             # return 102.27938 + 149472.51529 * T + 0.000007 * math.pow(cy, 2)
        elif planet_name == "Venus":
            return (48.0052 + 1.6021302244 * d) % 360
             # return 212.60322 + 58517.80387 * T + 0.001286 * math.pow(cy, 2)
        elif planet_name == "Mars":
            return (18.6021 + 0.5240207766 * d) % 360
             # return 319.51913 + 19139.85475 * T + 0.000181 * math.pow(cy, 2)
        elif planet_name == "Earth/Sun":
            return (356.0470 + 0.9856002585 * d) % 360
        elif planet_name == "Jupiter":
            return (19.8950 + 0.0830853001 * d) % 360
             # return 225.32833 + 3034.69202 * T - 0.000722 * math.pow(cy, 2)
        elif planet_name == "Saturn":
            return (316.9670 + 0.0334442282 * d) % 360
             # return 175.46622 + 1221.55147 * cy - 0.000502 * math.pow(cy, 2)
        elif planet_name == "Uranus":
            return (142.5905 + 0.011725806 * d) % 360
        elif planet_name == "Neptune":
            return (260.2471 + 0.005995147 * d) % 360
        else:
            return 1

    # need to figure this out

    # calculate eccentric anomaly of a planet
    def calculate_eccentric_anomaly(self):
        pass

    # need to figure this out

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
            # V = math.degrees(V)
            # V = V % 360
        return V

    # calculate right ascension and declination of a planet
    def calculate_ra_dec_planet(self, pl_name, pl_lscal, pl_lprop, pl_ascal, pl_aprop, pl_escal, pl_eprop, pl_iscal, pl_iprop,
                                pl_wscal,
                                pl_wprop, pl_oscal, pl_oprop, e_lscal, e_lprop, e_ascal, e_aprop, e_escal, e_eprop,
                                e_iscal, e_iprop, e_wscal, e_wprop, e_oscal, e_oprop, cy, d):

        # calculate elements of planetary orbit of the planet
        #pl_mean_long = self.calculate_mean_longitude(pl_lscal, pl_lprop, cy)
        pl_axis = self.calculate_semi_axis(pl_ascal, pl_aprop, cy)
        pl_eccentricity = self.calculate_eccentricity(pl_escal, pl_eprop, cy)
        pl_inclination = self.calculate_inclination(pl_iscal, pl_iprop, cy)
        pl_arg_perihelion = self.calculate_arg_perihelion(pl_wscal, pl_wprop, cy)
        pl_long_asc_node = self.calculate_long_asc_node(pl_oscal, pl_oprop, cy)

        # calculate elements of the planetary orbit of the Earth
        #e_mean_long = self.calculate_mean_longitude(e_lscal, e_lprop, cy)
        e_axis = self.calculate_semi_axis(e_ascal, e_aprop, cy)
        e_eccentricity = self.calculate_eccentricity(e_escal, e_eprop, cy)
        # e_inclination = calculate_inclination(e_iscal, e_iprop, cy)
        e_arg_perihelion = self.calculate_arg_perihelion(e_wscal, e_wprop, cy)
        # e_long_asc_node = calculate_long_asc_node(e_oscal, e_oprop, cy)

        # calculate the position of the Earth in its orbit
        #e_mean_anomaly = self.mod2pi(e_mean_long - e_arg_perihelion)
        e_mean_anomaly = self.calculate_mean_anomaly("Earth/Sun", d)
        e_v = self.calculate_true_anomaly(math.radians(e_mean_anomaly), math.radians(e_eccentricity))
        e_r = e_axis * (1 - math.pow(e_eccentricity, 2)) / (1 + e_eccentricity * math.cos(e_v))

        # calculate the heliocentric rectangular coordinates of Earth
        e_x = e_r * math.cos(e_v + e_arg_perihelion)
        e_y = e_r * math.sin(e_v + e_arg_perihelion)
        e_z = 0.0

        # calculate the position of the planet in its' orbit
        #pl_mean_anomaly = self.mod2pi(pl_mean_long - pl_arg_perihelion)
        pl_mean_anomaly = self.calculate_mean_anomaly(pl_name, d)
        pl_v = self.calculate_true_anomaly(math.radians(pl_mean_anomaly), math.radians(pl_eccentricity))
        pl_r = pl_axis * (1 - math.pow(pl_eccentricity, 2)) / (1 + pl_eccentricity * math.cos(pl_v))

        # calculate the heliocentric rectangular coordinates of the planet
        pl_xh = pl_r * (math.cos(pl_long_asc_node) * math.cos(pl_v + pl_arg_perihelion - pl_long_asc_node)
                        - math.sin(pl_long_asc_node) * math.sin(pl_v + pl_arg_perihelion - pl_long_asc_node)
                        * math.cos(pl_inclination))
        pl_yh = pl_r * (math.sin(pl_long_asc_node) * math.cos(pl_v + pl_arg_perihelion - pl_long_asc_node)
                        + math.cos(pl_long_asc_node) * math.sin(pl_v + pl_arg_perihelion - pl_long_asc_node)
                        * math.cos(pl_inclination))
        pl_zh = pl_r * (math.sin(pl_v + pl_arg_perihelion - pl_long_asc_node) * math.sin(pl_inclination))
        # come back to this
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
        ra = math.atan2(yeq, xeq)
        ra = math.degrees(ra) % 360
        dec = math.degrees(math.atan(zeq / math.sqrt(math.pow(xeq, 2) + math.pow(yeq, 2))))
        dist = math.sqrt(math.pow(xeq, 2) + math.pow(yeq, 2) + math.pow(zeq, 2))

        return (ra, dec, dist)


