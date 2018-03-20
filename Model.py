from Parsers import *
from Celestial_Objects import *
import TimeCalculations

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
            self.constellation_list.append(constellation)

    # Create all Messier Deep Space objects based on infromation from Messier Parser (m_parse) and append to messier_list
    def Create_Messier_Obj(self):
        print("To be implemented")

    # Create all Planets based on information from Planet Parser (p_parse) and append to planet_list
    def Create_Planets(self):
        print("To Be implemented")

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
        print("To Be implemented")

    #
    def Calculate_Moon_Position(self):
        print("to be implemented")

    #
    def Calculate_Messier_Positions(self):
        print("to be implemented")

