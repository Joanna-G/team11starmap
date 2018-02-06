from abc import ABCMeta, abstractmethod


class BaseCelestialObject:
    __metaclass__ = ABCMeta
    def __init__(self):
        self.right_ascension = None
        self.declination = None

    # example of how to do make an abstract method
    # @abstractmethod
    # def example(self):
    #     pass

class Planet(BaseCelestialObject):
    def __init__(self):
        BaseCelestialObject.__init__(self)
        self.planet_name = None

class Star(BaseCelestialObject):
    def __init__(self):
        BaseCelestialObject.__init__(self)
        self.proper_name = None
        self.star_id = None
        self.magnitude = None
        self.hd_number = None

class Moon(BaseCelestialObject):
    def __init__(self):
        BaseCelestialObject.__init__(self)
        self.phase = None

class Constellation(BaseCelestialObject):
    def __init__(self):
        BaseCelestialObject.__init__(self)
        self.name = None
        self.number_stars = None
        self.number_lines = None
        self.stars = []

class Messier_Objects(BaseCelestialObject)
    def __init__(self):
        BaseCelestialObject.__init__(self)




