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
        self.time_calc = TimeCalculations.TimeCalculations(year, month, day, hour, minute, utc_offset, lat, lon, 0)
        self.star_list = []
        self.constellation_list = []
        self.messier_list = []
        self.planet_list = []

        # Create all objects
        self.moon = Moon()
        self.Create_Celestial_Objects()

        self.boundary_x = None
        self.boundary_y = None

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

    # Create all constellations based on information from
    # Constellation Parser (c_parse) and append to constellation_list
    def Create_Constellations(self):

        for cp_constellation in self.c_parse:
            name = cp_constellation[0]
            stars = []
            for index in cp_constellation[1:]:
                stars.append(index)

            constellation = Constellation(name, stars, self.star_list)
            constellation.set_const_stars()
            constellation.set_num_stars()
            self.constellation_list.append(constellation)

    # Create all Messier Deep Space objects based on infromation from
    # Messier Parser (m_parse) and append to messier_list
    def Create_Messier_Obj(self):
        for mm_messier in self.m_parse:
            messier = MessierObject(mm_messier[0], mm_messier[1], mm_messier[2], mm_messier[3], mm_messier[4],
                                    mm_messier[5], mm_messier[6], mm_messier[7], mm_messier[8], mm_messier[9])
            self.messier_list.append(messier)

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

    # Calculate the position of each planet
    def Calculate_Planet_Positions(self):
        self.planet_list[2].semi_axis = self.planet_list[2].calculate_semi_axis(self.planet_list[2].ascal, self.planet_list[2].aprop, self.time_calc.cy)
        self.planet_list[2].eccentricity = self.planet_list[2].calculate_eccentricity(self.planet_list[2].escal, self.planet_list[2].eprop, self.time_calc.cy)
        self.planet_list[2].inclination = self.planet_list[2].calculate_inclination(self.planet_list[2].iscal, self.planet_list[2].iprop, self.time_calc.cy)
        self.planet_list[2].arg_perihelion = self.planet_list[2].calculate_arg_perihelion(self.planet_list[2].wscal, self.planet_list[2].wprop, self.time_calc.cy)
        self.planet_list[2].long_asc_node = self.planet_list[2].calculate_long_asc_node(self.planet_list[2].oscal, self.planet_list[2].oprop, self.time_calc.cy)
        self.planet_list[2].mean_long = self.planet_list[2].calculate_mean_longitude(self.planet_list[2].lscal, self.planet_list[2].lprop, self.time_calc.cy)
        # self.planet_list[2].mean_anomaly = self.planet_list[2].calculate_mean_anomaly(self.planet_list[2].proper_name, self.time_calc.d)
        # self.planet_list[2].true_anomaly = self.planet_list[2].calculate_true_anomaly(
        #     math.radians(self.planet_list[2].mean_anomaly), math.radians(self.planet_list[2].eccentricity))
        #self.planet_list[2].true_anomaly = self.planet_list[2].calculate_true_anomaly(math.radians(self.planet_list[2].mean_anomaly), math.radians(self.planet_list[2].eccentricity))
        self.planet_list[2].right_ascension, self.planet_list[2].declination, self.planet_list[2].distance = \
            self.planet_list[2].calculate_ra_dec_planet(self.planet_list[2].proper_name, self.planet_list[2].semi_axis,
                                                        math.radians(self.planet_list[2].eccentricity),
                                                        self.planet_list[2].inclination,
                                                        self.planet_list[2].arg_perihelion,
                                                        self.planet_list[2].long_asc_node,
                                                        self.planet_list[2].mean_long,
                                                        self.planet_list[2].semi_axis,
                                                        math.radians(self.planet_list[2].eccentricity),
                                                        self.planet_list[2].inclination,
                                                        self.planet_list[2].arg_perihelion,
                                                        self.planet_list[2].long_asc_node,
                                                        self.planet_list[2].mean_long)
        print(self.planet_list[2].proper_name)
        print("Right Ascension: ", self.planet_list[2].right_ascension)
        print("Declination: ", self.planet_list[2].declination)
        print()

        for planet in self.planet_list:
            if planet.proper_name != "Earth/Sun":
                planet.semi_axis = planet.calculate_semi_axis(planet.ascal, planet.aprop, self.time_calc.cy)
                planet.eccentricity = planet.calculate_eccentricity(planet.escal, planet.eprop, self.time_calc.cy)
                planet.inclination = planet.calculate_inclination(planet.iscal, planet.iprop, self.time_calc.cy)
                planet.arg_perihelion = planet.calculate_arg_perihelion(planet.wscal, planet.wprop, self.time_calc.cy)
                planet.long_asc_node = planet.calculate_long_asc_node(planet.oscal, planet.oprop, self.time_calc.cy)
                planet.mean_long = planet.calculate_mean_longitude(planet.lscal, planet.lprop, self.time_calc.cy)
                #planet.mean_anomaly = planet.calculate_mean_anomaly(planet.proper_name, self.time_calc.d)
                #planet.true_anomaly = planet.calculate_true_anomaly(planet.mean_anomaly,
                                                                   # math.radians(planet.eccentricity))
                #planet.true_anomaly = planet.calculate_true_anomaly(math.radians(planet.mean_anomaly),
                                                                    #math.radians(planet.eccentricity))
                planet.right_ascension, planet.declination, planet.distance = planet.calculate_ra_dec_planet(
                    planet.proper_name, planet.semi_axis, math.radians(planet.eccentricity), planet.inclination,
                    planet.arg_perihelion, planet.long_asc_node, planet.mean_long, self.planet_list[2].semi_axis,
                    math.radians(self.planet_list[2].eccentricity), self.planet_list[2].inclination,
                    self.planet_list[2].arg_perihelion, self.planet_list[2].long_asc_node,
                    self.planet_list[2].mean_long)
                ha_time = planet.calculate_ha_time(self.time_calc.lst, planet.right_ascension)
                planet.ha = planet.ha_time_to_degrees(ha_time)
                planet.alt, planet.az = planet.calculate_alt_az(planet.right_ascension, planet.declination,
                                                                self.time_calc.lat, self.time_calc.lon,
                                                                self.time_calc.mst)
                planet.get_xy_coords(planet.alt, planet.az, 4000)
                print("Altitude: ", planet.alt)
                print("Azimuth: ", planet.az)
                print()

    # Calculate the position of the Moon
    def Calculate_Moon_Position(self):
        self.moon.right_ascension, self.moon.declination = self.moon.calculate_alt_az(self.time_calc.t,
                                                                                      self.time_calc.lat, self.time_calc.t, self.time_calc.t, self.time_calc.lon, self.time_calc.gmst)
        ha_time = self.moon.calculate_ha_time(self.time_calc.lst, self.moon.right_ascension)
        self.moon.alt = self.moon.testing_alt(self.moon.declination, self.time_calc.lat, ha_time)
        self.moon.az = self.moon.testing_az(self.moon.declination, self.time_calc.lat, ha_time, self.moon.alt)
        self.moon.phase = self.moon.lunar_phase(self.time_calc.jd_current, self.time_calc.new_moon_ref)
        self.moon.get_xy_coords(self.moon.alt, self.moon.az, 4000)

    # Calculate the position of each messier object
    def Calculate_Messier_Positions(self):
        for messier in self.messier_list:
            messier.ha_time = messier.calculate_ha_time(self.time_calc.lst, messier.right_ascension)
            messier.ha_degrees = messier.ha_time_to_degrees(messier.ha_time)
            messier.altitude, messier.azimuth = messier.calculate_alt_az(messier.declination, self.time_calc.lat,
                                                                         messier.ha_degrees, None, None, None)
            messier.get_xy_coords(messier.altitude, messier.azimuth, 4000)

    def reset_values(self):
        for star in self.star_list:
            star.canvas_y = None
            star.canvas_x = None
            star.canvas_id = None

        for planet in self.planet_list:
            planet.canvas_x = None
            planet.canvas_y = None
            planet.canvas_id = None

        for messier in self.messier_list:
            messier.canvas_x = None
            messier.canvas_y = None
            messier.canvas_id = None

        self.moon.canvas_id = None
        self.moon.canvas_x = None
        self.moon.canvas_y = None

        for constellation in self.constellation_list:
            constellation.x = 0
            constellation.y = 0
