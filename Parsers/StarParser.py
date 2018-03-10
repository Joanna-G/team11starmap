from Parsers import Parser
import csv
import os.path

class StarParser(Parser):
    def __init__(self):
        fileDir = os.path.dirname(os.path.realpath('__file__'))
        Parser.__init__(self, os.path.join(fileDir, 'resources', 'Stars.csv'))


    # Parses the input File
    def parse_file(self):
        file = csv.reader(open(self.filepath, newline=''), delimiter=',')
        for row in file:
            element = []
            # Check if it is the header row, if it is, ignore it.
            if row[3] == "HR":
                continue
            # Check the Magnitude, if its greater than 6, ignore it
            elif abs(float(row[10])) > 6:
                continue
            else:
                # Store HD, ProperName ("" if it doesn't have one), Right Ascension, Declination, and Magnitude
                element.append(row[0])  # StarID -- Numbering system, not used for drawing charts
                element.append(row[2])  # Henry Draper ID
                element.append(row[6])  # Proper Name ("" if it doesn't have one)
                element.append(row[7])  # Right Ascension (RA)
                element.append(row[8])  # Declination
                element.append(row[10]) # Magnitude

            self.ElementsList.append(element)

        return self.ElementsList
