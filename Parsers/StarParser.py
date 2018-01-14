import csv
import os.path

class StarParser():
    def __init__(self):
        self.ElementsList = []

    # Parses the input File
    def parse_file(self):
        path = os.path.join('resources', "hyg.csv")
        file = csv.reader(open(path, newline=''), delimiter=',')
        #file = csv.reader(open('resources\hyg.csv', newline=''), delimiter=',')
        for row in file:
            element = []
            # Check if it is the header row, if it is, ignore it.
            if row[3] == "HR":
                continue
            # Check the Magnitude, if its greater than 6, ignore it
            elif abs(float(row[10])) > 6:
                continue
            else:
                # Store StarID, ProperName ("" if it doesn't have one), Right Ascension, Declination, and Magnitude
                element.append(row[0])
                element.append(row[6])
                element.append(row[7])
                element.append(row[8])
                element.append(row[10])

            self.ElementsList.append(element)

        return self.ElementsList
