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
def calculate_semi_axis(planet):
    return planet.ascal + planet.aprop * cy


# calculate eccentricity of the orbit
def calculate_eccentricity(planet):
    return planet.escal + planet.eprop * cy


# calculate inclination on the plane of the ecliptic
def calculate_inclination(planet):
    return math.radians(planet.iscal - planet.iprop * cy / 3600)


# calculate argument of perihelion
def calculate_arg_perihelion(planet):
    return math.radians(planet.wscal + planet.wprop * cy / 3600)


# calculate longitude of ascending node
def calculate_long_asc_node(planet):
    return math.radians(planet.oscal - planet.oprop * cy / 3600)


# calculate longitude of a planet
def calculate_longitude(planet):
    return mod2pi(math.radians(planet.iscal + planet.lprop * cy / 3600))


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


# start of calculations for the stars

# uses astropy library to calculate julian date. can also get gsmt time
def calculate_julian_day_astropy(year, month, day, hour, minute, lat, lon):
    # location = (str(lat) + 'd', str(lon) + 'd')
    location = (lat,lon)
    dt = dateutil.parser.parse(str(year) + '.' + str(month) + '.' + str(day) + ' ' + str(hour) + ':' + str(minute) + ':' + '0')
    time = astropy.time.Time(dt, location=('114.5d', '40d'))
    gsmt = time.sidereal_time('mean', 'greenwich')
    lst = time.sidereal_time('mean')
    print('gmst: ' + str(gsmt))
    print('lst ?: ' + str(lst))
    return time.jd


# pretty confident that this is right
def calculate_julian_day(year, month, day, hour, minute):
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

def gmst_testing(year, month, day, hour, minute):
    jd = calculate_julian_day(year, month, day, hour, minute)
    jd = math.floor(jd) + 0.5
    ut = hour + (minute / 60)
    t = (jd - 2451545.0) / 36525.0
    t_0 = 6.697374558+(2400.051336*t)+(0.000025862*math.pow(t,2))+(ut*1.0027379093)
    if t_0 > 24:
        while t_0 > 24.0:
            t_0 -= 24.0
    elif t_0 < 0.0:
        while t_0 < 0.0:
            t_0 += 24.0
    print(t_0)


# pretty confident that this is right
def calculate_gmst(year, month, day, hour, minute):
    jd = calculate_julian_day(year, month, day, hour, minute)
    midnight = math.floor(jd) + 0.5
    days_since_midnight = jd - midnight
    hours_since_midnight = days_since_midnight * 24
    days_since_epoch = jd - 2451545.0
    centuries_since_epoch = days_since_epoch / 35625
    whole_days_since_epoch = midnight - 2451545.0

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

    return (gmst_hours, gmst_minutes, gmst_seconds)


# this needs to be checked
def calculate_local_sidereal_time(lon_degrees, lon_minutes, lon_direction, gmst):
    lon_decimal = lon_degrees + (lon_minutes / 60.0)
    # if lon_direction == 'W':
    #     lon_decimal *= -1



    offset_decimal = lon_decimal / 15.0
    print('offset_decimal: ' + str(offset_decimal))
    hour_offset = int(offset_decimal)
    minute_offset = (offset_decimal % hour_offset) * 60
    second_offset = (minute_offset % int(minute_offset)) * 60

    minute_offset = int(minute_offset)
    second_offset = int(second_offset)

    gmst_decimal = gmst[0] + (gmst[1] / 60) + (gmst[2] / 3600)
    print('gmst_decimal: ' + str(gmst_decimal))
    lst = gmst_decimal + offset_decimal
    print('lst_decimal: ' + str(lst))

    print('offset time: ' + str(hour_offset) + ' ' + str(minute_offset) + ' ' + str(second_offset))

    lst_hour = gmst[0] + hour_offset
    lst_minute = gmst[1] + minute_offset
    lst_second = gmst[2] + second_offset

    if lst_second < 0:
        lst_second = 60 + lst_second
        lst_minute -= 1
    elif lst_second > 59:
        lst_second = 0
        lst_minute += 1

    if lst_minute < 0:
        lst_minute = 60 + lst_minute
        lst_hour -= 1
    elif lst_minute > 59:
        lst_minute = 0
        lst_hour += 1

    return (lst_hour, lst_minute, lst_second)


# pretty sure this is not right
def calculate_alt_az(ra, dec, lat, lon, lst):
    lst_decimal = lst[0] + (lst[1] / 60)
    hour_angle = lst_decimal - ra
    az = math.atan((math.sin(hour_angle) * math.cos(dec) * -1) / (math.cos(lat) * math.sin(dec) - math.sin(lat) * math.cos(dec) * math.cos(hour_angle)))
    alt = math.asin(math.sin(lat) * math.sin(dec) + math.cos(lat) * math.cos(dec) * math.cos(hour_angle))
    print(az)
    print(alt)

# uses astropy library to calculate altitude and azimuth
def calculate_alt_az_astropy():
    m33 = SkyCoord.from_name('M33')
    bear_mountain = EarthLocation(lat=41.3*u.deg, lon=-74*u.deg, height=390*u.m)
    utcoffset = -4*u.hour
    time = Time('2012-7-12 23:00:00') - utcoffset

    m33altaz = m33.transform_to(AltAz(obstime=time, location=bear_mountain))
    print("M33's Altitude = {0.alt:.4}".format(m33altaz))
    print("M33's Azimuth = {0.az:.4}".format(m33altaz))

    print(m33altaz.alt)


if __name__ == "__main__":
    year = 2018
    month = 2
    day = 8
    hour = 0
    minute = 27
    lat = 60
    # lon = -86.59
    lon = -86

    print('astropy jd: ' + str(calculate_julian_day_astropy(year, month, day, hour, minute, lat, lon)))
    print('jd: ' + str(calculate_julian_day(year, month, day, hour, minute)))
    gmst = calculate_gmst(year, month, day, hour, minute)
    # gmst_testing(year, month, day, hour, minute)
    print('gmst: ' + str(gmst))
    # print(calculate_mst(1900, 7, 31, 0, 0, 0, 0, 0))
    # print('gmst time: ' + str(gmst))
    lst = calculate_local_sidereal_time(lon, 30, 'W', gmst)
    print('lst time: ' + str(lst))
    #
    # calculate_alt_az(2.01372424, -19.49883745, 41.3, -74.0, lst)
    # calculate_alt_az_astropy()