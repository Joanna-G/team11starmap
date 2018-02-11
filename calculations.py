import math
import astropy.time
from astropy.time import Time
from astropy.coordinates import SkyCoord, EarthLocation, AltAz, Angle, Latitude, Longitude, ICRS, Galactic, FK4, FK5
import astropy.units as u
import dateutil.parser



# placeholder
cy = 0


# Calculates the Altitude and Azimuth of a planet given Latitude (lat), Longitude (lon),
# Right Ascension (ra), and Declination (dec). ra and dec are in degrees
def calculate_planet_alt_az(lat, lon, ra, dec):
    if lat < 0:
        lat *= -1.0
    if lon < 0:
        lon *= -1.0

    hour_angle = calculate_mst(year, month, day, hour, minute, second, lat, lon)
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


# Calculates the Mean Sidereal Time. Given Year (year), Month (month), Day (day), Hour (hour) on a
# 24 hour clock, Minute (minute), Second (second), Latitude (lat) and Longitude (lon).
# All times must be measured from Greenwich mean time (TimeZone = 0).
def calculate_mst(year, month, day, hour, min, sec, lat, lon):
    if month <= 2:
        year -= 1
        month += 12

    a = math.floor(year / 100.0)
    b = 2 - a + math.floor(a / 4)
    c = math.floor(365.25 * year)
    d = math.floor(30.6001 * (month + 1))

    # Get days since J2000
    jd = b + c + d - 730550.5 + day + (hour + min / 60 + sec / 3600) / 24
    # Get Julian centuries since J2000
    jt = jd / 36525.0
    # Calculate initial Mean Sidereal Time (mst)
    mst = 280.46061837 + (360.98564736629 * jd) + (0.000387933 * math.pow(jt, 2)) - (math.pow(jt, 3) / 38710000) + lon
    # Clip mst to range 0.0 to 360.0
    if mst > 0.0:
        while mst > 360.0:
            mst -= 360.0
    else:
        while mst < 0.0:
            mst += 360.0
    return mst


# Converts Right Ascension (ra) in degrees to Hours:Minutes:Seconds
def convert_ra_mhs(ra):
    hours = int(ra / 15.0)
    minutes = int(((ra / 15.0) - hours) * 60.0)
    seconds = ((((ra / 15.0) - hours) * 60.0) - minutes) * 60.0
    return (hours, minutes, seconds)


# Converts Declination (dec) in degress to Degrees:Minutes:Seconds
def convert_dec_dms(dec):
    degrees = int(dec)
    minutes = int((dec - degrees) * 60.0)
    seconds = (((dec - degrees) * 60.0) - minutes) * 60.0
    return (degrees, minutes, seconds)


# calculate semimajor axis of the orbit
def calculate_semi_axis(ascal, aprop, cy):
    return ascal + aprop * cy


# calculate eccentricity of the orbit
def calculate_eccentricity(escal, eprop, cy):
    return escal + eprop * cy


# calculate inclination on the plane of the ecliptic
def calculate_inclination(iscal, iprop, cy):
    return math.radians(iscal - iprop * cy / 3600)


# calculate argument of perihelion
def calculate_arg_perihelion(wscal, wprop, cy):
    return math.radians(wscal + wprop * cy / 3600)


# calculate longitude of ascending node
def calculate_long_asc_node(oscal, oprop, cy):
    return math.radians(oscal - oprop * cy / 3600)


# calculate mean longitude of a planet
def calculate_mean_longitude(lscal, lprop, cy):
    return mod2pi(math.radians(lscal + lprop * cy / 3600))


# calculate true anomaly of a planet
def calculate_true_anomaly(mean_anomaly, eccentricity):
    pass
# need to figure this out


# Convert an angle above 360 degrees to one less than 360
def mod2pi(x):
    b = x / 2 * math.pi
    a = (math.pi * 2) * (b - abs_floor(b))
    if a < 0:
        a += (2 * math.pi)
    converted_angle = a
    return converted_angle


def abs_floor(b):
    if b >= 0:
        floor = math.floor(b)
    else:
        floor = math.ceil(b)
    return floor


# calculate right ascension and declination of a planet
def calculate_ra_dec_planet(pl_lscal, pl_lprop, pl_ascal, pl_aprop, pl_escal, pl_eprop, pl_iscal, pl_iprop, pl_wscal,
                            pl_wprop, pl_oscal, pl_oprop, e_lscal, e_lprop, e_ascal, e_aprop, e_escal, e_eprop,
                            e_iscal, e_iprop, e_wscal, e_wprop, e_oscal, e_oprop, cy):

    # calculate elements of planetary orbit of the planet
    pl_mean_long = calculate_mean_longitude(pl_lscal, pl_lprop, cy)
    pl_axis = calculate_semi_axis(pl_ascal, pl_aprop, cy)
    pl_eccentricity = calculate_eccentricity(pl_escal, pl_eprop, cy)
    pl_inclination = calculate_inclination(pl_iscal, pl_iprop, cy)
    pl_arg_perihelion = calculate_arg_perihelion(pl_wscal, pl_wprop, cy)
    pl_long_asc_node = calculate_long_asc_node(pl_oscal, pl_oprop, cy)

    # calculate elements of the planetary orbit of the Earth
    e_mean_long = calculate_mean_longitude(e_lscal, e_lprop, cy)
    e_axis = calculate_semi_axis(e_ascal, e_aprop, cy)
    e_eccentricity = calculate_eccentricity(e_escal, e_eprop, cy)
    e_inclination = calculate_inclination(e_iscal, e_iprop, cy)
    e_arg_perihelion = calculate_arg_perihelion(e_wscal, e_wprop, cy)
    e_long_asc_node = calculate_long_asc_node(e_oscal, e_oprop, cy)

    # calculate the position of the Earth in its orbit
    e_m = mod2pi(e_mean_long - e_arg_perihelion)
    # need to calculate mean anomaly
    e_v = calculate_true_anomaly(e_mean_anomaly, math.radians(e_eccentricity))
    e_r = e_axis * (1 - math.pow(e_eccentricity, 2)) / (1 + e_eccentricity * math.cos(e_v))

    # calculate the heliocentric rectangular coordinates of Earth
    e_x = e_r * math.cos(e_v + e_arg_perihelion)
    e_y = e_r * math.sin(e_v + e_arg_perihelion)
    e_z = 0.0

    # calculate the position of the planet in its' orbit
    pl_m = mod2pi(pl_mean_long - pl_arg_perihelion)
    # need to calculate mean anomaly
    pl_v = calculate_true_anomaly(pl_mean_anomaly, math.radians(pl_eccentricity))
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
    ra = math.radians(mod2pi(math.atan2(yeq, xeq)))
    dec = math.degrees(math.atan(zeq / math.sqrt(math.pow(xeq, 2) + math.pow(yeq, 2))))
    dist = math.sqrt(math.pow(xeq, 2) + math.pow(yeq, 2) + math.pow(zeq, 2))

    return (ra, dec, dist)


# start of calculations for the stars

class TimeCalculations:
    def __init__(self, year, month, day, hour, minute, lat, lon):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.lat = lat
        self.lon = lon

    def calculate_julian_day(self, year, month, day, hour, minute):
        converted_time = hour + (minute / 60)
        converted_day = day + (converted_time / 24)
        if month > 2:
            year = year
            month = month
        else:
            year -= 1
            month += 12
        b = -13
        jd = int(365.25 * year) + int(30.6001 * (month + 1)) + converted_day + 1720994.5 + b
        return jd

    def calculate_gmst(self, year, month, day, hour, minute):
        jd = self.calculate_julian_day(year, month, day, hour, minute)
        midnight = math.floor(jd) + 0.5
        days_since_midnight = jd - midnight
        hours_since_midnight = days_since_midnight * 24
        days_since_epoch = jd - 2451545.0
        centuries_since_epoch = days_since_epoch / 35625
        whole_days_since_epoch = midnight - 2451545

        gmst = 6.697374558 + 0.06570982441908 * whole_days_since_epoch + 1.00273790935 * hours_since_midnight + 0.000026 * math.pow(centuries_since_epoch, 2)
        gmst_remainder = gmst % int(gmst)
        gmst_hours = math.floor(gmst) % 24
        gmst_minutes = math.floor(gmst_remainder * 60)
        gmst_minutes_decimal = gmst_remainder * 60
        gmst_minutes_decimal = gmst_minutes_decimal % int(gmst_minutes_decimal)
        gmst_seconds = math.floor(gmst_minutes_decimal * 60)

        if year < 2000:
            gmst_minutes += 60
            gmst_seconds += 60

        gmst_decimal = gmst_hours + (gmst_minutes / 60) + (gmst_seconds / 3600)

        return gmst_decimal

    def calculate_lst(self, lon_decimal, gmst_decimal):
        offset_decimal = lon_decimal / 15
        lst_decimal = gmst_decimal + offset_decimal
        if lst_decimal < 0:
            lst_decimal += 24
        elif lst_decimal > 24:
            lst_decimal = lst_decimal - 24

        return lst_decimal

    def calculate_ha_time(self, lst, ra):
        ha_time = lst - ra
        print('ha time before correction: ' + str(ha_time))
        if ha_time < 0:
            while ha_time < 0:
                ha_time += 24
        elif ha_time > 24:
            while ha_time > 24:
                ha_time = ha_time - 24
        return ha_time

    def calculate_az(self, dec, lat, ha_time):
        ha_degrees = self.ha_time_to_degrees(ha_time)

        az_rad = math.atan((-1 * math.sin(math.radians(ha_degrees)) * math.cos(math.radians(dec))) / (
                (math.cos(math.radians(lat)) * math.sin(math.radians(dec))) - (
                math.sin(math.radians(lat)) * math.cos(math.radians(dec)) * math.cos(math.radians(ha_degrees)))))
        az_degrees = math.degrees(az_rad)

        if az_degrees < 0:
            while az_degrees < 0:
                az_degrees += 360
        elif az_degrees > 360:
            while az_degrees > 360:
                az_degrees = 360 - az_degrees

        return az_degrees

    def calculate_alt(self, dec, lat, ha_time):
        ha_degrees = self.ha_time_to_degrees(ha_time)
        print('ha degrees: ' + str(ha_degrees))
        alt_rad = math.asin(math.sin(math.radians(lat)) * math.sin(math.radians(dec))) + (
                math.cos(math.radians(lat)) * math.cos(math.radians(dec)) * math.cos(math.radians(ha_degrees)))
        alt_degrees = math.degrees(alt_rad)
        return alt_degrees

    def testing_alt(self, dec, lat, ha_time):
        ha_degrees = self.ha_time_to_degrees(ha_time)
        alt_rad = math.sin(math.radians(dec)) * math.sin(math.radians(lat)) + math.cos(math.radians(dec)) * math.cos(math.radians(lat)) * math.cos(math.radians(ha_degrees))
        alt_rad = math.asin(alt_rad)
        alt_degrees = math.degrees(alt_rad)
        return alt_degrees

    def testing_az(self, dec, lat, ha_time, alt):
        ha_degrees = self.ha_time_to_degrees(ha_time)
        print('ha degrees dd: ' + str(ha_degrees))
        az_rad = (math.sin(math.radians(dec)) - (math.sin(math.radians(alt)) * math.sin(math.radians(lat)))) / (math.cos(math.radians(alt)) * math.cos(math.radians(lat)))
        az_rad = math.acos(az_rad)
        az_degrees = math.degrees(az_rad)
        if math.sin(math.radians(ha_degrees)) < 0:
            az_degrees = az_degrees
        else:
            az_degrees = 360 - az_degrees
        return az_degrees


    def ha_time_to_degrees(self, ha_time):
        ha_degrees_hours = int(ha_time * 15)
        ha_degrees_minutes = (((ha_time * 15) - ha_degrees_hours))
        ha_degrees_seconds = ((((ha_time * 15) - ha_degrees_hours)) - ha_degrees_minutes)
        ha_degrees = ha_degrees_hours + ha_degrees_minutes + ha_degrees_seconds
        return ha_degrees


    def ra_degrees_to_time_decimal(self, ra):
        hours = int(ra / 15.0)
        minutes = int(((ra / 15.0) - hours) * 60)
        seconds = ((((ra / 15.0) - hours) * 60.0) - minutes) * 60
        print('hh:mm:ss: ' + str(hours) + ' ' + str(minutes) + ' ' + str(seconds))
        ra_time_decimal = hours + (minutes / 60) + (seconds / 3600)
        return ra_time_decimal


if __name__ == "__main__":
    year = 1905
    month = 2
    day = 16
    hour = 12
    minute = 0
    lat = 34.71
    lon = 86.6

    ra = 1.28435588
    dec = -66.39789075

    time_calc = TimeCalculations(year, month, day, hour, minute, lat, lon)
    gmst_decimal = time_calc.calculate_gmst(year, month, day, hour, minute)
    lst_decimal = time_calc.calculate_lst(lon, gmst_decimal)
    ha_time = time_calc.calculate_ha_time(lst_decimal, ra)
    az_degrees = time_calc.calculate_az(dec, lat, ha_time)
    alt_degrees = time_calc.calculate_alt(dec, lat, ha_time)
    testing_alt_degrees = time_calc.testing_alt(dec, lat, ha_time)
    testing_az_degrees = time_calc.testing_az(dec, lat, ha_time, testing_alt_degrees)

    print('gmst decimal: ' + str(gmst_decimal))
    print('lst decimal: ' + str(lst_decimal))
    print('ha decimal: ' + str(ha_time))
    print('az degrees: ' + str(az_degrees))
    print('alt degrees: ' + str(alt_degrees))
    print('tesing az: ' + str(testing_az_degrees))
    print('tesing alt: ' + str(testing_alt_degrees))