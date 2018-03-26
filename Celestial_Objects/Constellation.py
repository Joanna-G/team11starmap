# from Celestial_Objects import BaseCelestialObject

# class Constellation(BaseCelestialObject):


# So, this questionably need to be a subclass of celestial Objects, so it currently isn't
class Constellation:
    def __init__(self, name, star_list):
        # BaseCelestialObject.__init__(self, None, None)
        self.proper_name = name
        self.star_list = star_list
        self.number_stars = None
        self.number_lines = None
        self.x = 0
        self.y = 0

    # Finding the center of the constellation. There has to be a more python-esque way of accomplishing this,
    # but I'm not totally sure what it is at the moment. Ignore for now.
    def set_center(self):
        x_sum = 0
        y_sum = 0
        for star in self.star_list:
            x_sum += star.x
            y_sum += star.y
        self.x = x_sum / len(self.star_list)
        self.y = y_sum / len(self.star_list)
