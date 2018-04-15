# from Celestial_Objects import BaseCelestialObject
# class Constellation(BaseCelestialObject):


# So, this questionably need to be a subclass of celestial Objects, so it currently isn't
class Constellation:
    def __init__(self, name, stars, star_list):
        # BaseCelestialObject.__init__(self, None, None)
        self.proper_name = name
        self.line_stars = stars
        self.main_star_list = star_list
        self.const_stars = []
        self.number_stars = 0
        # self.number_lines = None
        self.x = 0
        self.y = 0

    def set_const_stars(self):
        for element in self.line_stars:
            for star in self.main_star_list:
                if (element[0] or element[1]) == star.hd_id and star not in self.const_stars:
                        self.const_stars.append(star)

    def set_num_stars(self):
        self.number_stars = len(self.const_stars)

    # Finding the center of the constellation. There has to be a more python-esque way of accomplishing this,
    # but I'm not totally sure what it is at the moment. Ignore for now.
    def set_center(self):
        x_sum = 0
        y_sum = 0
        prev_canvas_x = 0
        prev_canvas_y = 0
        for star in self.const_stars:
            if star.canvas_x is None:
                star.canvas_x = prev_canvas_x
            if star.canvas_y is None:
                star.canvas_y = prev_canvas_y
            x_sum = x_sum + star.canvas_x
            y_sum = y_sum + star.canvas_y
        self.x = x_sum / self.number_stars
        self.y = y_sum / self.number_stars
