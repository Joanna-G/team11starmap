import math
import astropy.time
import dateutil.parser

year = 2018
month = 2
day = 5
hour = 18
minute = 30
second = 0

# Calculates the Altitude and Azimuth of a planet given Latitude (lat), Longitude (lon),
# Right Ascension (ra), and Declination (dec). ra and dec are in degrees
def calculate_alt_az(lat, lon, ra, dec):
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

def calculate_julian_day(year, month, day, hour, minute, second):
    julian_day = ((367 * year) - math.floor(7.0 * (year + math.floor((month + 9.0) / 12.0) / 4.0)) + math.floor(275.0 * month / 9.0) + day - 730531.5 + hour / 24.0)
    return julian_day

def calculate_julian_day_astropy(year, month, day):
    dt = dateutil.parser.parse(str(year) + '.' + str(month) + '.' + str(day))
    time = astropy.time.Time(dt)
    return time.jd

def calculate_julian_day_coleman(year, month, day, hour, minute):
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

def calculate_gmst(year, month, day, hour, minute):
    jd = calculate_julian_day_coleman(year, month, day, hour, minute)
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
    gmst_seconds = gmst_minutes_decimal * 60

    print(gmst_hours)
    print(gmst_minutes)
    print(gmst_seconds)




if __name__ == "__main__":
    print(calculate_julian_day_astropy(2019, 1, 1))
    print(calculate_julian_day_coleman(2019, 1, 1, 8, 0))
    calculate_gmst(2004, 1, 1, 0, 0)

