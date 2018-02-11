from Parsers.StarParser import StarParser
from Parsers.PlanetParser import PlanetParser
from Parsers.ConstellationParser import ConstellationParser


def main():
    stars = StarParser()
    starList = stars.parse_file()
    print("Stars: ")
    print(starList)

    planets = PlanetParser()
    planetList = planets.parse_file()
    print("\nPlanets: ")
    print(planetList)

    constellations = ConstellationParser()
    constellationsList = constellations.parse_file()
    print("\nConstellations: ")
    print(constellationsList)



if __name__ == "__main__":
    main()
