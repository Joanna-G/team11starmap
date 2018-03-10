from Parsers import Parser
import csv
import os

class MessierParser(Parser):
    def __init__(self):
        fileDir = os.path.dirname(os.path.realpath('__file__'))
        Parser.__init__(self, os.path.join(fileDir, 'resources', 'Messier_Deep_Space_Objects.csv'))

    def parse_file(self):
        file = csv.reader(open(self.filepath, newline=''), delimiter=',')

        for row in file:
            element = []
            element.append(row[1]) # MessierCatOrder
            element.append(row[2]) # RA Hours
            element.append(row[3]) # RA Minutes
            element.append(row[4]) # RA Sec
            element.append(row[5]) # Dec Degrees
            element.append(row[6]) # Dec Min
            element.append(row[7]) # Dec Sec
            element.append(row[8]) # Magnitude
            element.append(row[9]) # Common Name
            element.append(row[10])# Desc

            self.ElementsList.append(element)

        return self.ElementsList

def main():
    messier = MessierParser()
    elements = messier.parse_file()
    print(elements)