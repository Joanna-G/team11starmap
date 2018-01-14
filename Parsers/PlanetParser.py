import csv

class PlanetParser():
    def __init__(self):
        self.ElementsList = []

    # Parses the input File
    def parse_file(self):
        file = csv.reader(open('resources\Planets.csv', newline=''), delimiter=',')
        for row in file:
            element = []
            # Check if it is the header row, if it is, ignore it.
            if row[0] == "ï»¿PlanetName":
                continue
            else:
                for i in range (0, 12, 1):
                    element.append(row[i])

            self.ElementsList.append(element)

        return self.ElementsList

