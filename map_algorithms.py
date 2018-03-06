import math

# http://spaceupdate.com/activities/ST05_plotting_the_moon.pdf

# May need to convert the alt/az to theta/phi used in polar coordinates?
# theta = longitude?
# phi = 90 - latitude?
# cos(theta) = cos(alt) * cos(az)
# tan(phi) = tan(alt) / sin(az)

# I think that the "longitude" is the azimuth in this case. It would go from 0 at "North" (East?) working
# counterclockwise like a normal circle.
# I think the "latitude" is the altitude. It'd go from 90 in the center (zenith) to 0 at the edge (horizon).
# The following call for some sort of "center" and I'm not entirely sure what that would be. I think we
# would say the center is 90 latitude, 0 longitude?


# Convert from alt, az to x,y,z
# Stole this from the other file.
def alt_az_to_rect(alt, az, r):
    x = (r * math.cos(math.radians(az)) * math.cos(math.radians(alt)))
    y = (r * math.cos(math.radians(az)) * math.sin(math.radians(alt)))
    z = (r * math.sin(math.radians(az)))

    # Print for testing
    print("x = " + str(x) + " y = " + str(y) + " z = " + str(z))
    return x, y, z


# Returns r and theta where r is distance from center (latitude or azimuth) and theta is angle in radians
def rect_to_polar(x, y):
    r = math.sqrt(x * x + y * y)
    theta = math.atan(y / x)

    # Print for testing
    print("r = " + str(r) + " theta = " + str(theta))
    return r, theta


def azimuthal_equidistant(az, alt):
    # phi1 = latitude of the center of the projection
    phi1 = math.radians(90)
    # lambda0 = longitude of the center of the projection
    lamb0 = math.radians(0)

    phi = math.radians(90 - alt)
    lamb = math.radians(az)

    # c is the angular distance from the center
    # cos(c) = sin(phi1) * sin(phi) + cos(phi1) * cos(phi) * cos(lambda - lambda0)
    c = math.acos(math.sin(phi1) * math.sin(phi) + math.cos(phi1) * math.cos(phi) * math.cos(lamb - lamb0))
    # kp = c / sin(c)
    kp = c / math.sin(c)
    # x = kp * cos(phi) * sin(lambda-lambda0)
    x = kp * math.cos(phi) * math.sin(lamb - lamb0)
    # y = kp * (cos(phi1) * sin(phi) - sin(phi1) * cos(phi) * cos(lambda - lambda0))
    y = kp * (math.cos(phi1) * math.sin(phi) - math.sin(phi1) * math.cos(phi) * math.cos(lamb - lamb0))

    # Print for testing
    print("x = " + str(x) + " y = " + str(y))

    return x, y


def lambert_az_equidistant(az, alt):
    # phi1 = standard parallel
    phi1 = math.radians(90)
    # lambda0 = central longitude
    lamb0 = math.radians(0)

    phi = math.radians(90 - alt)
    lamb = math.radians(az)

    # kp = square_root(2 / (1 + sin(phi1) * sin(phi) + cos(phi1) * cos(phi) * cos(lambda - lambda0)))
    kp = math.sqrt(2 / (1 + math.sin(phi1) * math.sin(phi) + math.cos(phi1) * math.cos(phi) * math.cos(lamb - lamb0)))
    # x = kp * cos(phi) * sin(lambda - lambda0)
    x = kp * math.cos(phi) * math.sin(lamb - lamb0)
    # y = kp * (cos(phi1) * sin(phi) - sin(phi1) * cos(phi) * cos(lambda - lambda0))
    y = kp * (math.cos(phi1) * math.sin(phi) - math.sin(phi1) * math.cos(phi) * math.cos(lamb - lamb0))

    # Print for testing
    print("x = " + str(x) + " y = " + str(y))

    return x, y


def stereographic(az, alt):
    # r is the radius of the sphere (1? Radius of the earth? No idea.)
    r = 6371
    # phi1 = the central latitude
    phi1 = math.radians(90)
    # lambda0 = the central longitude
    lamb0 = math.radians(0)

    phi = math.radians(90 - alt)
    lamb = math.radians(az)

    # k = (2 * r) / (1 + sin(phi1) * sin(phi) + cos(phi1) * cos(phi) * cos(lambda - lambda0))
    k = (2 * r) / (1 + math.sin(phi1) * math.sin(phi) + math.cos(phi1) * math.cos(phi) * math.cos(lamb - lamb0))
    # x = k * cos(phi) * sin(lambda - lambda0)
    x = k * math.cos(phi) * math.sin(lamb - lamb0)
    # y = k * (cos(phi1) * sin(phi) - sin(phi1) * cos(phi) * cos(lambda - lambda0))
    y = k * (math.cos(phi1) * math.sin(phi) - math.sin(phi1) * math.cos(phi) * math.cos(lamb - lamb0))

    # Print for testing
    print("x = " + str(x) + " y = " + str(y))

    return x, y


# Local variables for testing
alt = 20
az = 270
r = 1

x, y, z = alt_az_to_rect(alt, az, r)
r, theta = rect_to_polar(x, y)
x, y = azimuthal_equidistant(az, alt)
x, y = lambert_az_equidistant(az, alt)
x, y = stereographic(az, alt)
