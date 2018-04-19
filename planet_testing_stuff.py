import math


class my_class:
    N = 0  # Long of asc node
    i = 0  # incl of ecliptic
    w = 0.0  # argument of perihelion
    a = 0  # semi-major axis
    e = 0.0  # eccentricity
    M = 0.0  # mean anomaly
    r = 0.0  # distance
    ecl = 0.0
    RA = 0.0
    Dec = 0.0
    az = 0.0
    alt = 0.0


def time_scale(y, m, D, UT):
    d = 367 * y - 7 * (y + (m + 9) / 12) / 4 + 275 * m / 9 + D - 730530
    d = d + UT / 24.0
    return d


def normalize(M):
    if M > 360:
        while M > 360:
            M = M - 360
    elif M < 0:
        while M < 0:
            M = M + 360
    else:
        M = M
    return M


def sun_pos(sun, UT, lat, long):
    e = sun.e
    E = sun.M + sun.e * math.sin(sun.M) * (1.0 + sun.e * math.cos(sun.M))
    xv = math.cos(E) - e
    yv = math.sqrt(1.0 - e * e) * math.sin(E)
    v = math.atan2(yv, xv)
    sun.r = math.sqrt(xv * xv + yv * yv)

    sun.lonsun = math.radians(math.degrees(v) + math.degrees(sun.w))

    xs = sun.r * math.cos(sun.lonsun)
    ys = sun.r * math.sin(sun.lonsun)
    xe = xs
    ye = ys * math.cos(math.radians(sun.ecl))
    ze = ys * math.sin(math.radians(sun.ecl))

    sun.RA = math.degrees(math.atan2(ye, xe))
    sun.Dec = math.degrees(math.atan2(ze, math.sqrt(xe * xe + ye * ye)))

    while sun.RA > 360:
        sun.RA = sun.RA - 360
    while sun.RA < 0:
        sun.RA = sun.RA + 360

    rg = math.sqrt(xe * xe + ye * ye + ze * ze)

    GMST0 = sun.lonsun / 15 + 12
    GMST = GMST0 + UT
    LST = GMST + long / 15

    HA = LST - sun.RA

    x = math.cos(HA) * math.cos(sun.Dec)
    y = math.sin(HA) * math.cos(sun.Dec)
    z = math.sin(sun.Dec)

    xhor = x * math.sin(lat) - z * math.cos(lat)
    yhor = y
    zhor = x * math.cos(lat) + z * math.sin(lat)

    sun.az = math.radians(math.degrees(math.atan2(yhor, xhor)) + 180)
    sun.alt = math.atan2(zhor, math.sqrt(xhor * xhor + yhor * yhor))

    return LST


def planet_pos(planet, sun, LST, lat):
    M = math.radians(planet.M)
    e = planet.e
    E = M + e * math.sin(M) * (1.0 + e * math.cos(M))
    a = planet.a
    w = planet.w
    N = planet.N
    i = planet.i

    if 0.05 < e < 0.06:
        E0 = E
        isGreater = True
        while isGreater:
            E1 = E0 - (E0 - e * math.sin(E0) - M) / (1 - e * math.cos(E0))
            if E0 - E1 < math.radians(0.001):
                isGreater = False
            E0 = E1

    xv = a * (math.cos(E) - e)
    yv = a * (math.sqrt(1.0 - e * e) * math.sin(E))

    v = math.atan2(yv, xv)
    r = math.sqrt(xv * xv + yv * yv)

    xh = r * (math.cos(N) * math.cos(v + w) - math.sin(N) * math.sin(v + w) * math.cos(i))
    yh = r * (math.sin(N) * math.cos(v + w) + math.cos(N) * math.sin(v + w) * math.cos(i))
    zh = r * (math.sin(v + w) * math.sin(i))

    lonecl = math.atan2(yh, xh)
    latecl = math.atan2(zh, math.sqrt(xh * xh + yh * yh))

    xh = r * math.cos(lonecl) * math.cos(latecl)
    yh = r * math.sin(lonecl) * math.cos(latecl)
    zh = r * math.sin(latecl)

    xs = sun.r * math.cos(sun.lonsun)
    ys = sun.r * math.sin(sun.lonsun)

    xg = xh + xs
    yg = yh + ys
    zg = zh

    xe = xg
    ye = yg * math.cos(planet.ecl) - zg * math.sin(planet.ecl)
    ze = yg * math.sin(planet.ecl) + zg * math.cos(planet.ecl)

    planet.RA = math.degrees(math.atan2(ye, xe))
    planet.Dec = math.degrees(math.atan2(ze, math.sqrt(xe * xe + ye * ye)))

    while planet.RA < 0:
        planet.RA = planet.RA + 360
    while planet.RA > 360:
        planet.RA = planet.RA - 360

    rg = math.sqrt(xe * xe + ye * ye + ze * ze)

    HA = LST - planet.RA

    x = math.cos(HA) * math.cos(planet.Dec)
    y = math.sin(HA) * math.cos(planet.Dec)
    z = math.sin(planet.Dec)

    xhor = x * math.sin(lat) - z * math.cos(lat)
    yhor = y
    zhor = x * math.cos(lat) + z * math.sin(lat)

    az = math.radians(math.degrees(math.atan2(yhor, xhor)) + 180)
    alt = math.atan2(zhor, math.sqrt(xhor * xhor + yhor * yhor))

    return az, alt


if __name__ == '__main__':
    y = 2018
    m = 4
    D = 22
    UT = 21.5
    lat = 34.7
    long = -86.6

    d = time_scale(y, m, D, UT)

    sun = my_class()
    sun.N = 0
    sun.i = 0
    sun.w = 282.9404 + 4.70935E-5 * d
    sun.a = 1.0
    sun.e = 0.016709 - 1.151E-9 * d
    sun.M = 356.0470 + 0.9856002585 * d
    sun.M = normalize(sun.M)
    sun.M = math.radians(sun.M)
    sun.ecl = 23.4393 - 3.563E-7 * d
    LST = sun_pos(sun, UT, lat, long)

    moon = my_class()
    moon.N = 125.1228 - 0.0529538083 * d
    moon.i = 5.1454
    moon.w = 318.0634 + 0.1643573223 * d
    moon.a = 60.2666
    moon.e = 0.054900
    moon.M = 115.3654 + 13.0649929509 * d

    mercury = my_class()
    mercury.N = 48.3313 + 3.24587E-5 * d
    mercury.i = 7.0047 + 5.00E-8 * d
    mercury.w = 29.1241 + 1.01444E-5 * d
    mercury.a = 0.387098
    mercury.e = 0.205635 + 5.59E-10 * d
    mercury.M = 168.6562 + 4.0923344368 * d
    mercury.ecl = 23.4393 - 3.563E-7 * d
    mercury.az, mercury.alt = planet_pos(mercury, sun, LST, lat)
    print('{} : {} : {} {}'.format(sun.az, sun.alt, mercury.az, mercury.alt))
