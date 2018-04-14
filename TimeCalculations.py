import math
from datetime import datetime, timedelta


class TimeCalculations:
    def __init__(self, year, month, day, hour, minute, utc_offset, lat, lon, dst):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = 0
        self.utc_offset = utc_offset
        self.lat = lat
        self.lon = lon
        self.dst = dst

        self.julian_day = self.calculate_julian_day(self.year, self.month, self.day, self.hour, self.minute)
        self.gmst = self.calculate_gmst(self.julian_day, self.year)
        self.lst = self.calculate_lst(self.lon, self.gmst)
        self.mst = self.calculate_mst(self.year, self.month, self.day, self.hour, self.minute, self.second, self.lon)
        self.cy = self.calculate_cy()

        self.jd_current = self.calculate_julian_day(year, month, day, hour, minute)
        self.new_moon_ref = self.calculate_julian_day(1900, 1, 1, 0, 0)
        self.t = self.calculate_T(self.jd_current)
        self.d = self.calculate_day(self.year, self.month, self.day, self.utc_offset)

    # def convert_to_ut(self, year, month, day, hour, minute, utc_offset):
    #     hour = hour + utc_offset
    #     if hour > 24:
    #         day += 1
    #         hour -= 24
    #     elif hour < 0:
    #         day -= 1
    #         hour += 24

    def update_times(self, year, month, day, hour, minute, utc_offset, lat, lon, dst):
        self.utc_offset = utc_offset
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = 0
        self.lat = lat
        self.lon = lon
        self.dst = dst

        # Convert to UTC
        date = datetime.now()
        date.replace(self.year, self.month, self.day, self.hour, self.minute, 0, 0)

        if self.dst == 1:
            future_date = date + timedelta(hours=(self.utc_offset + 1))
        else:
            future_date = date + timedelta(hours=self.utc_offset)

        self.year = future_date.year
        self.month = future_date.month
        self.day = future_date.day
        self.hour = future_date.hour
        self.minute = future_date.minute

        self.julian_day = self.calculate_julian_day(self.year, self.month, self.day, self.hour, self.minute)
        self.gmst = self.calculate_gmst(self.julian_day, self.year)
        self.lst = self.calculate_lst(self.lon, self.gmst)
        self.mst = self.calculate_mst(self.year, self.month, self.day, self.hour, self.minute, self.second, self.lon)
        self.cy = self.calculate_cy()

        self.jd_current = self.calculate_julian_day(self.year, self.month, self.day, self.hour, self.minute)
        self.new_moon_ref = self.calculate_julian_day(1900, 1, 1, 0, 0)
        self.t = self.calculate_T(self.jd_current)
        self.d = self.calculate_day(self.year, self.month, self.day, self.utc_offset)

    def calculate_cy(self):
        return self.julian_day/36525

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
    #def calculate_julian_century(self):
     #   return math.radians(self.julian_day / 36525)

    # Added by Ben - also needed this
    # Joanna also needs this
    def calculate_T(self, jd):
        return (jd - 2415020.0) / 36525

    # added by Ben - not sure what this exactly does, but works in mean anomaly calculation
    def calculate_day(self, year, month, day, UT):
        d = 367 * year - 7 * (year + (month + 9) / 12) / 4 + 275 * month / 9 + day - 730530
        d = d + UT / 24.0
        return d

    def calculate_gmst(self, jd, year):
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
        # division by zero
        try:
            gmst_minutes_decimal = gmst_minutes_decimal % int(gmst_minutes_decimal)
        except:
            gmst_minutes_decimal = 0
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

    # Calculates the Mean Sidereal Time. Given Year (year), Month (month), Day (day), Hour (hour) on a
    # 24 hour clock, Minute (minute), Second (second), Latitude (lat) and Longitude (lon).
    # All times must be measured from Greenwich mean time (TimeZone = 0).
    def calculate_mst(self, year, month, day, hour, min, sec, lon):
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
        mst = 280.46061837 + (360.98564736629 * jd) + (0.000387933 * math.pow(jt, 2)) - (
                    math.pow(jt, 3) / 38710000) + lon
        # Clip mst to range 0.0 to 360.0
        if mst > 0.0:
            while mst > 360.0:
                mst -= 360.0
        else:
            while mst < 0.0:
                mst += 360.0
        return mst

    # Exists in Base Celestial Object class
    # def calculate_ha_time(self, lst, ra):
    #     ha_time = lst - ra
    #     if ha_time < 0:
    #         while ha_time < 0:
    #             ha_time += 24
    #     elif ha_time > 24:
    #         while ha_time > 24:
    #             ha_time = ha_time - 24
    #     return ha_time


    # Exists in base celestial object class
    # def ha_time_to_degrees(self, ha_time):
    #     ha_degrees_hours = int(ha_time * 15)
    #     ha_degrees_minutes = (((ha_time * 15) - ha_degrees_hours))
    #     ha_degrees_seconds = ((((ha_time * 15) - ha_degrees_hours)) - ha_degrees_minutes)
    #     ha_degrees = ha_degrees_hours + ha_degrees_minutes + ha_degrees_seconds
    #     return ha_degrees

    def ra_degrees_to_time_decimal(self, ra):
        hours = int(ra / 15.0)
        minutes = int(((ra / 15.0) - hours) * 60)
        seconds = ((((ra / 15.0) - hours) * 60.0) - minutes) * 60
        # print('hh:mm:ss: ' + str(hours) + ' ' + str(minutes) + ' ' + str(seconds))
        ra_time_decimal = hours + (minutes / 60) + (seconds / 3600)
        return ra_time_decimal

