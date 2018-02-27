import math

# http://spaceupdate.com/activities/ST05_plotting_the_moon.pdf

# May need to convert the alt/az to theta/phi used in polar coordinates?
# theta = longitude
# phi = 90 - latitude
# cos(theta) = cos(alt) * cos(az)
# tan(phi) = tan(alt) / sin(az)

# I think that the "latitude" is the azimuth in this case. It would go from 0 at "North" working
# counterclockwise like a normal circle.
# I think the "longitude" is the altitude. It'd go from 90 in the center to 0 at the edge of the graph.
# The following call for some sort of "center" and I'm not entirely sure what that would be. I think we
# would say the center is 0 latitude, 90 longitude?


# Convert from alt, az to x,y,z
# Stole this from the other file.
def alt_az_to_rect(alt, az, r):
    x = (r * math.cos(math.radians(az)) * math.cos(math.radians(alt)))
    y = (r * math.cos(math.radians(az)) * math.sin(math.radians(alt)))
    z = (r * math.sin(math.radians(az)))

    return x, y, z


# Returns r and theta where r is distance from center (latitude or azimuth) and theta is angle in radians
def rect_to_polar(x, y):
    r = math.sqrt(x * x + y * y)
    theta = math.atan(y / x)

    return r, theta


def azimuthal_equidistant(az, alt):
    # phi1 = latitude of the center of the projection
    # lambda0 = longitude of the center of the projection
    # c is the angular distance from the center
    # cos(c) = sin(phi1) * sin(phi) + cos(phi1) * cos(phi) * cos(lambda - lambda0)
    # kp = c / sin(c)
    # x = kp * cos(phi) * sin(lambda-lambda0)
    # y = kp * (cos(phi1) * sin(phi) - sin(phi1) * cos(phi) * cos(lambda - lambda0))
    return 0


def lambert_az_equidistant(az, alt):
    # phi1 = standard parallel
    # lambda0 = central longitude
    # kp = square_root(2 / (1 + sin(phi1) * sin(phi) + cos(phi1) * cos(phi) * cos(lambda - lambda0)))
    # x = kp * cos(phi) * sin(lambda - lambda0)
    # y = kp * (cos(phi1) * sin(phi) - sin(phi1) * cos(phi) * cos(lambda - lambda0))
    return 0


def stereographic(az, alt, R):
    # R is the radius of the sphere
    # phi1 = the central latitude
    # lambda0 = the central longitude
    # k = (2 * R) / (1 + sin(phi1) * sin(phi) + cos(phi1) * cos(phi) * cos(lambda - lambda0))
    # x = k * cos(phi) * sin(lambda - lambda0)
    # y = k * (cos(phi1) * sin(phi) - sin(phi1) * cos(phi) * cos(lambda - lambda0))
    return 0

