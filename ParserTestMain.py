from Parsers.StarParser import StarParser
from Parsers.PlanetParser import PlanetParser


def main():
    stars = StarParser()
    starList = stars.parse_file()
    print("Stars: ")
    print(starList)

    planets = PlanetParser()
    planetList = planets.parse_file()
    print("\nPlanets: ")
    print(planetList)


if __name__ == "__main__":
    main()
