from Parsers import *
from Celestial_Objects import *
import TimeCalculations
import math


class Model():
    def __init__(self, year, month, day, hour, minute, utc_offset, lat, lon):
        # Create Parser objects, and parse files
        self.p_parse = PlanetParser().parse_file()
        self.c_parse = ConstellationParser().parse_file()
        self.m_parse = MessierParser().parse_file()
        self.s_parse = StarParser().parse_file()

        # Create TimeCalculations object, with default values (The Current day/time)
        self.time_calc = TimeCalculations.TimeCalculations(year, month, day, hour, minute, utc_offset, lat, lon)
        self.star_list = []
        self.constellation_list = []
        self.messier_list = []
        self.planet_list = []

        # Create all objects
        self.moon = Moon()
        self.Create_Celestial_Objects()

    # Create all Stars, Constellations, Planets, Messier Deep Space Objects, and Planets
    def Create_Celestial_Objects(self):
        self.Create_Stars()
        self.Create_Constellations()
        self.Create_Planets()
        self.Create_Messier_Obj()
        self.Create_Planets()

    # Create Stars based on information from Star Parser (s_parse) information and append to star_list
    def Create_Stars(self):
        for sp_star in self.s_parse:
            star = Star(sp_star[0], sp_star[1], sp_star[2], float(sp_star[3]), float(sp_star[4]), float(sp_star[5]))
            self.star_list.append(star)

    # Create all constellations based on infromation from Constellation Parser (c_parse) and append to constellation_list
    def Create_Constellations(self):
        for cp_constellation in self.c_parse:
            name = cp_constellation[0]
            star_list = []
            for index in cp_constellation[1:]:
                star_list.append(index)
            constellation = Constellation(name, star_list)

            # Working out a way to find the center of a constellation for labels.
            # Ignore this for now.
            # constellation.set_center()

            self.constellation_list.append(constellation)

    # Create all Messier Deep Space objects based on infromation from Messier Parser (m_parse) and append to messier_list
    def Create_Messier_Obj(self):
        print("To be implemented")

    # Create all Planets based on information from Planet Parser (p_parse) and append to planet_list
    def Create_Planets(self):
        for pp_planet in self.p_parse:
            planet = Planet(pp_planet[0], pp_planet[1], pp_planet[2], pp_planet[3], pp_planet[4], pp_planet[5],
                            pp_planet[6], pp_planet[7], pp_planet[8], pp_planet[9], pp_planet[10], pp_planet[11],
                            pp_planet[12])
            self.planet_list.append(planet)

    # Calculate all stars positions based on user inputted date, time, and location values
    def Calculate_Star_Positions(self):
        for star in self.star_list:
            star.ha_time = star.calculate_ha_time(self.time_calc.lst, star.right_ascension)
            star.ha_degrees = star.ha_time_to_degrees(star.ha_time)
            star.altitude, star.azimuth = star.calculate_alt_az(star.declination, self.time_calc.lat, star.ha_degrees,
                                                                None, None, None)
            star.get_xy_coords(star.altitude, star.azimuth, 4000)

    #
    def Calculate_Planet_Positions(self):
        for planet in self.planet_list:
            planet.semi_axis = planet.calculate_semi_axis(planet.ascal, planet.aprop, self.time_calc.cy)
            planet.eccentricity = planet.calculate_eccentricity(planet.escal, planet.eprop, self.time_calc.cy)
            planet.inclination = planet.calculate_inclination(planet.iscal, planet.iprop, self.time_calc.cy)
            planet.arg_perihelion = planet.calculate_arg_perihelion(planet.wscal, planet.wprop, self.time_calc.cy)
            planet.long_asc_node = planet.calculate_long_asc_node(planet.oscal, planet.oprop, self.time_calc.cy)
            planet.mean_long = planet.calculate_mean_longitude(planet.lscal, planet.lprop, self.time_calc.cy)
            planet.mean_anomaly = planet.calculate_mean_anomaly(planet.planet_name, self.time_calc.d)
            planet.true_anomaly = planet.calculate_true_anomaly(math.radians(planet.mean_anomaly),
                                                                math.radians(planet.eccentricity))
            planet.right_ascension, planet.declination, planet.distance = planet.calculate_ra_dec_planet(
                 planet.planet_name, planet.lscal, planet.lprop, planet.ascal, planet.aprop,
                 planet.escal, planet.eprop, planet.iscal, planet.iprop, planet.wscal,
                 planet.wprop, planet.oscal, planet.oprop, planet.lscal, planet.lprop,
                 self.planet_list[2].ascal, self.planet_list[2].aprop, self.planet_list[2].escal,
                 self.planet_list[2].eprop, self.planet_list[2].iscal,
                 self.planet_list[2].iprop, self.planet_list[2].wscal, self.planet_list[2].wprop,
                 self.planet_list[2].oscal, self.planet_list[2].oprop, self.time_calc.cy, self.time_calc.d)
            ha_time = planet.calculate_ha_time(self.time_calc.lst, planet.right_ascension)
            planet.ha = planet.ha_time_to_degrees(ha_time)
            planet.alt, planet.az = planet.calculate_alt_az(self, planet.declination, self.time_calc.lat,
                                                            planet.ha, self.time_calc.t, self.time_calc.lon,
                                                            self.time_calc.mst)

    #
    def Calculate_Moon_Position(self):
        print("Moons are stupid.")
        self.moon.right_ascension, self.moon.declination = self.moon.calculate_alt_az(self.time_calc.t,
                    self.time_calc.lat, self.time_calc.t, self.time_calc.t, self.time_calc.lon, self.time_calc.gmst)
        ha_time = self.moon.calculate_ha_time(self.time_calc.lst, self.moon.right_ascension)
        self.moon.alt = self.moon.testing_alt(self.moon.declination, self.time_calc.lat, ha_time)
        self.moon.az = self.moon.testing_az(self.moon.declination, self.time_calc.lat, ha_time, self.moon.alt)
        self.moon.phase = self.moon.lunar_phase(self.time_calc.jd_current, self.time_calc.new_moon_ref)
        print("Moon phase is " + str(self.moon.phase))
        self.moon.get_xy_coords(self.moon.alt, self.moon.az, 4000)

    #
    def Calculate_Messier_Positions(self):
        print("to be implemented")

