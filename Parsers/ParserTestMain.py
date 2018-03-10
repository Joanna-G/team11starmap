from Parsers import *

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
    constellations.parse_file()
    print("\nConstellations: ")
    print(constellations.ElementsList)

    messier = MessierParser()
    messier.parse_file()
    print("\nMessier Deep Space Objects: ")
    print(messier.ElementsList)


if __name__ == "__main__":
    main()
