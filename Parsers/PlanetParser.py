from Parsers import Parser
import csv
import os.path


class PlanetParser(Parser):
    def __init__(self):
        fileDir = os.path.dirname(os.path.realpath('__file__'))
        Parser.__init__(self, os.path.join(fileDir, 'resources', "Planets.csv"))

    # Parses the input File
    def parse_file(self):
        file = csv.reader(open(self.filepath, newline=''), delimiter=',')
        for row in file:
            element = []

            # Check if it is the header row, if it is, ignore it.
            if row[1] == "Lscal":
                continue
            elif row[0] in (None, ""):
                break
            else:
                for i in range(0, 13, 1):
                    element.append(row[i])
            self.ElementsList.append(element)

        # print(self.ElementsList)
        return self.ElementsList


# def main():
#     planet = PlanetParser()
#     element = planet.parse_file()
#     print(element)
