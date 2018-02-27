import math
from datetime import datetime as dt
import time
import astropy.time
from astropy.time import Time
from astropy.coordinates import SkyCoord, EarthLocation, AltAz, Angle, Latitude, Longitude, ICRS, Galactic, FK4, FK5
import astropy.units as u
# import dateutil.parser

# placeholder
cy = 0


# Calculates the Altitude and Azimuth of a planet given Latitude (lat), Longitude (lon),
# Right Ascension (ra), and Declination (dec). ra and dec are in degrees
def calculate_planet_alt_az(lat, lon, ra, dec):
    if lat < 0:
        lat *= -1.0
    if lon < 0:
        lon *= -1.0

    hour_angle = calculate_mst(year, month, day, hour, minute, 0, lat, lon)
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


# Conversions added by Joanna for moon, but may be applicable elsewhere.
# Reduces an angle to between 0 and 360 degrees
def rev(x):
    return x - math.floor(x / 360.0) * 360.0


# Convert from ra, dec or long, lat or alt, az to x,y,z
def ra_dec_to_rect(ra, dec, r):
    x = (r * math.cos(math.radians(dec)) * math.cos(math.radians(ra)))
    y = (r * math.cos(math.radians(dec)) * math.sin(math.radians(ra)))
    z = (r * math.sin(math.radians(dec)))

    return x, y, z


def rect_to_spherical(x, y, z):
    r = math.sqrt(x * x + y * y + z * z)
    ra = math.atan2(y, x)

    if x == 0 and y == 0:
       dec = math.atan2(z, math.sqrt(x * x + y * y))
    else:
       dec = math.asin(z/r)

    return math.degrees(ra), math.degrees(dec)


# Convert between ecliptic and equatorial coordinates.
def ecliptic_to_equatorial(x_ecl, y_ecl, z_ecl):
    obl = math.radians(23.439281)
    x_eq = x_ecl
    y_eq = y_ecl * math.cos(obl) - z_ecl * math.sin(obl)
    z_eq = y_ecl * math.sin(obl) + z_ecl * math.cos(obl)
    return x_eq, y_eq, z_eq


# Convert between equatorial and ecliptic
def equatorial_to_ecliptic(x_eq, y_eq, z_eq):
    obl = math.radians(23.439281)
    x_ecl = x_eq
    y_ecl = y_eq * math.cos(obl) + z_eq * math.sin(obl)
    z_ecl = - y_eq * math.sin(obl) + z_eq * math.cos(obl)
    return x_ecl, y_ecl, z_ecl


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
    return float(ascal) + float(aprop) * cy


# calculate eccentricity of the orbit
def calculate_eccentricity(escal, eprop, cy):
    return float(escal) + float(eprop) * cy


# calculate inclination on the plane of the ecliptic
def calculate_inclination(iscal, iprop, cy):
    # return math.radians(float(iscal) - float(iprop) * cy / 3600)
    return math.radians(float(iscal) - float(iprop) * cy / 3600)


# calculate argument of perihelion
def calculate_arg_perihelion(wscal, wprop, cy):
    return math.radians(float(wscal) + float(wprop) * cy / 3600)


# calculate longitude of ascending node
def calculate_long_asc_node(oscal, oprop, cy):
    return math.radians(float(oscal) - float(oprop) * cy / 3600)


# calculate mean longitude of a planet
def calculate_mean_longitude(lscal, lprop, cy):
    # return mod2pi(math.radians(float(lscal) + float(lprop) * cy / 3600))
    mean_long_rads = math.radians(float(lscal) + float(lprop) * cy / 3600)
    # mean_long = float(lscal) + float(lprop) * cy / 3600
    mean_long_rads = mean_long_rads % (math.pi*2)
    mean_long = math.degrees(mean_long_rads)
    return mean_long


# calculate mean anomaly of a planet
def calculate_mean_anomaly(planet_name, d):
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
def calculate_eccentric_anomaly():
    pass
# need to figure this out


# calculate true anomaly of a planet
def calculate_true_anomaly(mean_anomaly, eccentricity):
    E = mean_anomaly + eccentricity * math.sin(mean_anomaly) * (1.0 + eccentricity * math.cos(mean_anomaly))
    E1 = 0
    while(abs(E - E1) > (1.0 * eccentricity - 12)):
        E1 = E
        E = E1 - (E1 - eccentricity * math.sin(E1) - mean_anomaly) / (1 - eccentricity * math.cos(E1))
        if(abs(E - E1) > (1.0 * eccentricity - 12)):
            break
    V = 2 * math.atan(math.sqrt(1 + eccentricity) / (1 - eccentricity)) * math.tan(0.5 * E)
    if(V < 0):
        V = V + (math.pi * 2)
        V = math.degrees(V)
        V = V % 360
    return V

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
def calculate_ra_dec_planet(pl_name, pl_lscal, pl_lprop, pl_ascal, pl_aprop, pl_escal, pl_eprop, pl_iscal, pl_iprop, pl_wscal,
                            pl_wprop, pl_oscal, pl_oprop, e_lscal, e_lprop, e_ascal, e_aprop, e_escal, e_eprop,
                            e_iscal, e_iprop, e_wscal, e_wprop, e_oscal, e_oprop, cy, d):

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
    e_mean_anomaly = calculate_mean_anomaly("Earth/Sun", d)
    e_v = calculate_true_anomaly(e_mean_anomaly, math.radians(e_eccentricity))
    e_r = e_axis * (1 - math.pow(e_eccentricity, 2)) / (1 + e_eccentricity * math.cos(e_v))

    # calculate the heliocentric rectangular coordinates of Earth
    e_x = e_r * math.cos(e_v + e_arg_perihelion)
    e_y = e_r * math.sin(e_v + e_arg_perihelion)
    e_z = 0.0

    # calculate the position of the planet in its' orbit
    pl_m = mod2pi(pl_mean_long - pl_arg_perihelion)
    pl_mean_anomaly = calculate_mean_anomaly(pl_name, d)
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
    ra = math.atan2(yeq, xeq)
    ra = math.degrees(ra) % 360
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

    # Added by Ben - I need this for planet calculations. Can move if needed, but is time related
    def calculate_julian_century(self, jd):
        return math.radians(jd / 36525)

    # Added by Ben - also needed this
    # Joanna also needs this
    def calculate_T(self, jd):
        return (jd - 2415020.0) / 36525

    # added by Ben - not sure what this exactly does, but works for mean anomaly
    def calculate_day(self, year, month, day, UT):
        d = 367 * year - 7 * (year + (month + 9) / 12) / 4 + 275 * month / 9 + day - 730530
        d = d + UT / 24.0
        return d

    # Added by Jo - May need this later
    def calculate_day_number(self, year, month, day, hour, minute):
        jd = self.calculate_julian_day(year, month, day, hour, minute)
        day_num = jd - 2451543.5
        return day_num

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

    # Jo is testing something
    def calculate_gst(self, jd):
        T = self.calculate_T(jd)
        theta0 = 280.46061837 + 360.98564736629 * (jd - 2451545.0) + 0.000387933 * T * T - T * T * T / 38710000.0
        return theta0

    def calc_lst_jo(self, theta0, lon):
        return theta0 + lon

    def calc_ha_jo(self, lst, ra):
        return lst - ra

    def calc_alt_jo(self, dec, lat, ha):
        dec = math.radians(dec)
        lat = math.radians(lat)
        ha = math.radians(ha)

        alt = math.sin(dec) * math.sin(lat) + math.cos(dec) * math.cos(lat) * math.cos(ha)
        alt = math.degrees(math.asin(alt))
        return alt

    def calc_az_jo(self, dec, lat, alt):
        dec = math.radians(dec)
        lat = math.radians(lat)
        alt = math.radians(alt)

        az = (math.sin(dec) - math.sin(lat) * math.sin(alt)) / math.cos(lat) * math.cos(alt)
        az = math.degrees((math.acos(az)))
        return az
    # Jo is done testing something

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
        alt_rad = math.sin(math.radians(dec)) * math.sin(math.radians(lat)) + math.cos(math.radians(dec)) * \
                  math.cos(math.radians(lat)) * math.cos(math.radians(ha_degrees))
        alt_rad = math.asin(alt_rad)
        alt_degrees = math.degrees(alt_rad)
        return alt_degrees

    def testing_az(self, dec, lat, ha_time, alt):
        ha_degrees = self.ha_time_to_degrees(ha_time)
        print('ha degrees dd: ' + str(ha_degrees))
        az_rad = (math.sin(math.radians(dec)) - (math.sin(math.radians(alt)) * math.sin(math.radians(lat)))) / \
                 (math.cos(math.radians(alt)) * math.cos(math.radians(lat)))
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


# Start of Moon Calculations

# Calculates the current phase of the moon.
# Returns an integer representation with 0 being new,
# 1 being first quarter, 2 being full, and 3 being last quarter
def lunar_phase(year, month, day, hour, minute, lat, lon):

    # Moon Phases
    NEW = 0
    FIRST = 1
    FULL = 2
    LAST = 3

    # Calculate the current Julian Date and the Julian Date of the first
    # new moon of 1900. Use the JD of first moon as reference for current
    # moon phase.
    jd_calc = TimeCalculations(year, month, day, hour, minute, lat, lon)
    jd_current = jd_calc.calculate_julian_day(year, month, day, hour, minute)
    new_moon_ref = jd_calc.calculate_julian_day(1900, 1, 1, 0, 0)
    phase_jd = jd_current - new_moon_ref
    sc = 29.53059
    age_of_moon = phase_jd % sc

    # Testing age of moon
    print("Age of moon: " + str(age_of_moon))

    # The age of the moon determines the phase, with the actual
    # date of the phase at the center of the range
    if 0 <= age_of_moon < 3.69:
        current_phase = NEW
    elif 3.69 <= age_of_moon < 11.07:
        current_phase = FIRST
    elif 11.07 <= age_of_moon < 18.45:
        current_phase = FULL
    elif 18.45 <= age_of_moon < 25.84:
        current_phase = LAST
    elif 25.84 <= age_of_moon <= sc:
        current_phase = NEW

    return current_phase


# Calculate Lunar geocentric RA and Dec, which is close enough to the topocentric that it doesn't matter
def lunar_location(year, month, day, hour, minute, lat, lon):

    # Get current Julian Date
    jd_calc = TimeCalculations(year, month, day, hour, minute, lat, lon)
    jd = jd_calc.calculate_julian_day(year, month, day, hour, minute)

    # No idea what this is, but I need it.
    t = jd_calc.calculate_T(jd)

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
    x, y, z = ra_dec_to_rect(lunar_long, lunar_lat, 1)

    # Convert from ecliptic to equatorial
    x2, y2, z2 = ecliptic_to_equatorial(x, y, z)

    # Convert back to spherical
    ra, dec = rect_to_spherical(x2, y2, z2)

    # Normalize right ascension
    ra = rev(ra)

    theta0 = rev(jd_calc.calculate_gst(jd))
    print("Theta0: " + str(theta0))
    lst = rev(jd_calc.calc_lst_jo(theta0, lon))
    print("lst: " + str(lst))
    ha = rev(jd_calc.calc_ha_jo(lst, ra))
    print("hr: " + str(ha))

    alt = jd_calc.calc_alt_jo(dec, lat, ha)
    az = jd_calc.calc_az_jo(dec, lat, alt)

    return dec, ra, alt, az


if __name__ == "__main__":
    year = 2018
    month = 2
    day = 25
    hour = 9
    minute = 0
    lat = 34.73
    lon = 86.58

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
    jd = time_calc.calculate_julian_day(year, month, day, hour, minute)
    phase = lunar_phase(year, month, day, hour, minute, lat, lon)
    lun_dec, lun_ra, lun_alt, lun_az = lunar_location(year, month, day, hour, minute, lat, lon)

    # Testing for print
    if phase == 0:
        phase = "new"
    elif phase == 1:
        phase = "first"
    elif phase == 2:
        phase = "full"
    else:
        phase = "last"

    print('gmst decimal: ' + str(gmst_decimal))
    print('lst decimal: ' + str(lst_decimal))
    print('ha decimal: ' + str(ha_time))
    print('az degrees: ' + str(az_degrees))
    print('alt degrees: ' + str(alt_degrees))
    print('tesing az: ' + str(testing_az_degrees))
    print('tesing alt: ' + str(testing_alt_degrees))
    print('testing jd: ' + str(jd))
    print('testing moon phase: ' + str(phase))
    print('testing lunar ra: ' + str(lun_ra))
    print('testing lunar dec: ' + str(lun_dec))
    print('testing lunar alt: ' + str(lun_alt))
    print('testing lunar az: ' + str(lun_az))
    print(str(convert_ra_mhs(lun_ra)))
    print(str(convert_dec_dms(lun_dec)))

