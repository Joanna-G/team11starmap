from Celestial_Objects import BaseCelestialObject
import math
import TimeCalculations


class Moon(BaseCelestialObject):
    def __init__(self):
        BaseCelestialObject.__init__(self, None, None)
        self.phase = None
        self.alt = None
        self.az = None
        self.proper_name = 'Moon'

    def lunar_phase(self, jd_current, new_moon_ref):

        # Calculate the current Julian Date and the Julian Date of the first
        # new moon of 1900. Use the JD of first moon as reference for current
        # moon phase.
        phase_jd = jd_current - new_moon_ref
        sc = 29.53059
        age_of_moon = phase_jd % sc

        # The age of the moon determines the phase, with the actual
        # date of the phase at the center of the range
        if 0 <= age_of_moon < 3.69:
            self.phase = 'New'
        elif 3.69 <= age_of_moon < 11.07:
            self.phase = 'First Quarter'
        elif 11.07 <= age_of_moon < 18.45:
            self.phase = 'Full'
        elif 18.45 <= age_of_moon < 25.84:
            self.phase = 'Last Quarter'
        elif 25.84 <= age_of_moon <= sc:
            self.phase = 'New'

        return self.phase

    # Calculate Lunar geocentric RA and Dec, which is close enough to the topocentric that it doesn't matter
    # So the abstract method says declination, but here we need this fun unknown value t, so go ahead and pass it t
    # instead of dec
    def calculate_alt_az(self, dec, lat, ha_degrees, t, lon, mst):

        # Get moon mean longitude, sun mean anomaly, moon mean anomaly,
        # moon mean elongation, moon mean distance, sun's mean longitude, e
        moon_mean_long = 270.434164 + 481267.8831 * t
        sun_mean_anom = 358.475833 + 35999.0498 * t
        moon_mean_anom = 296.104608 + 477198.8491 * t
        moon_mean_elong = 350.737486 + 445267.1142 * t
        moon_mean_dist = 11.250889 + 483202.0251 * t
        e = 1 - (0.002495 * t) - (0.00000752 * t * t)

        # Calculate Lunar geocentric latitude
        lunar_lat = (5.128189 * math.sin(math.radians(moon_mean_dist))) + \
                    (0.280606 * math.sin(math.radians(moon_mean_anom + moon_mean_dist))) + \
                    (0.277693 * math.sin(math.radians(moon_mean_anom - moon_mean_dist))) + \
                    (0.173238 * math.sin(math.radians(2 * moon_mean_elong - moon_mean_dist))) + \
                    (0.055413 * math.sin(math.radians(2 * moon_mean_elong + moon_mean_dist - moon_mean_anom))) + \
                    (0.046272 * math.sin(math.radians(2 * moon_mean_elong - moon_mean_dist - moon_mean_anom))) + \
                    (0.032573 * math.sin(math.radians(2 * moon_mean_elong + moon_mean_dist))) + \
                    (0.017198 * math.sin(math.radians(2 * moon_mean_anom + moon_mean_dist))) + \
                    (0.009267 * math.sin(math.radians(2 * moon_mean_elong + moon_mean_anom - moon_mean_dist))) + \
                    (0.008823 * math.sin(math.radians(2 * moon_mean_anom - moon_mean_dist)))

        # Calculate Lunar geocentric longitude
        lunar_long = moon_mean_long + (6.288750 * math.sin(math.radians(moon_mean_anom))) + \
                     (1.274018 * math.sin(math.radians(2 * moon_mean_elong - moon_mean_anom))) + \
                     (0.658309 * math.sin(math.radians(2 * moon_mean_elong))) + \
                     (0.213616 * math.sin(math.radians(2 * moon_mean_anom))) - \
                     (0.185596 * math.sin(math.radians(sun_mean_anom)) * e) - \
                     (0.114336 * math.sin(math.radians(2 * moon_mean_dist))) + \
                     (0.058793 * math.sin(math.radians(2 * moon_mean_elong - 2 * moon_mean_anom))) + \
                     (0.057212 * math.sin(math.radians(2 * moon_mean_elong - sun_mean_anom - moon_mean_anom)) * e) + \
                     (0.053320 * math.sin(math.radians(2 * moon_mean_elong + moon_mean_anom))) + \
                     (0.045874 * math.sin(math.radians(2 * moon_mean_elong - sun_mean_anom)) * e)

        # Convert from latitude and longitude to cartesian
        x, y, z = self.ra_dec_to_rect(lunar_long, lunar_lat, 1)

        # Convert from ecliptic to equatorial
        x2, y2, z2 = self.ecliptic_to_equatorial(x, y, z)

        # Convert back to spherical
        self.right_ascension, self.declination = self.rect_to_spherical(x2, y2, z2)

        # Normalize right ascension
        self.right_ascension = self.rev(self.right_ascension)
        self.right_ascension = self.ra_degrees_to_time_decimal(self.right_ascension)
        # self.calculate_ha_time(lst, self.right_ascension)
        # self.moon.alt = self.moon.testing_alt(self.moon.declination, lat, ha_time)
        # self.moon.az = self.moon.testing_az(self.moon.declination, lat, ha_time, self.moon.alt)
        return self.right_ascension, self.declination

    # Convert from ra, dec or long, lat or alt, az to x,y,z
    def ra_dec_to_rect(self, ra, dec, r):
        x = (r * math.cos(math.radians(dec)) * math.cos(math.radians(ra)))
        y = (r * math.cos(math.radians(dec)) * math.sin(math.radians(ra)))
        z = (r * math.sin(math.radians(dec)))

        return x, y, z

    def rect_to_spherical(self, x, y, z):
        r = math.sqrt(x * x + y * y + z * z)
        ra = math.atan2(y, x)

        if x == 0 and y == 0:
            dec = math.atan2(z, math.sqrt(x * x + y * y))
        else:
            dec = math.asin(z / r)

        return math.degrees(ra), math.degrees(dec)

    # Convert between ecliptic and equatorial coordinates.
    def ecliptic_to_equatorial(self, x_ecl, y_ecl, z_ecl):
        obl = math.radians(23.439281)
        x_eq = x_ecl
        y_eq = y_ecl * math.cos(obl) - z_ecl * math.sin(obl)
        z_eq = y_ecl * math.sin(obl) + z_ecl * math.cos(obl)
        return x_eq, y_eq, z_eq

    # Convert between equatorial and ecliptic
    def equatorial_to_ecliptic(self, x_eq, y_eq, z_eq):
        obl = math.radians(23.439281)
        x_ecl = x_eq
        y_ecl = y_eq * math.cos(obl) + z_eq * math.sin(obl)
        z_ecl = - y_eq * math.sin(obl) + z_eq * math.cos(obl)
        return x_ecl, y_ecl, z_ecl


if __name__ == "__main__":
    year = 2018
    month = 4
    day = 10
    hour = 19
    minute = 30
    lat = 34.73
    lon = 86.58
    offset = -6
    dst = 1

    moon = Moon()
    time = TimeCalculations.TimeCalculations(year, month, day, hour, minute, offset, lat, lon, dst)
    moon.phase = moon.lunar_phase(time.jd_current, time.new_moon_ref)
    gmst = time.calculate_gmst(time.jd_current, year)
    moon.right_ascension, moon.declination = moon.calculate_alt_az(time.t, 34, 0, time.t, lon, gmst)
    moon.right_ascension = time.ra_degrees_to_time_decimal(moon.right_ascension)
    lst = time.calculate_lst(lon, gmst)
    ha = moon.calculate_ha_time(lst, moon.right_ascension)
    alt = moon.testing_alt(moon.declination, lat, ha)
    az = moon.testing_az(moon.declination, lat, ha, alt)
    print("Altitude: " + str(alt) + " Azimuth: " + str(az) + " Phase: " + str(moon.phase))
