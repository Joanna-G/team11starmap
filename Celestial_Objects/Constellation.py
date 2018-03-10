from Celestial_Objects import BaseCelestialObject

#class Constellation(BaseCelestialObject):

# So, this questionably need to be a subclass of celestial Objects, so it currently isn't
class Constellation:
    def __init__(self, name, star_list):
        #BaseCelestialObject.__init__(self, None, None)
        self.name = name
        self.star_list = star_list
        self.number_stars = None
        self.number_lines = None