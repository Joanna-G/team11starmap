from Parsers import Parser
import csv
import os.path

class ConstellationParser(Parser):
    def __init__(self):
        fileDir = os.path.dirname(os.path.realpath('__file__'))
        Parser.__init__(self, os.path.join(fileDir, 'resources', 'Constellations.csv'))

    # Parses the input File
    def parse_file(self):
        file = csv.reader(open(self.filepath, newline=''), delimiter=',')
        # Connection list stores 1st the constellation name, then all the asterisms
        connectionList = []
        for row in file:
            # Connection stores each asterism
            connection = []
            if row[0].isdigit():
                connection.append(row[0])
                connection.append(row[1])
                connectionList.append(connection)
            else:
                self.ElementsList.append(connectionList[:])
                connectionList.clear()
                connectionList.append(row[0])

        # Remove the first empty element of the list
        self.ElementsList.pop(0)
        print(self.ElementsList)
        return self.ElementsList

def main():
    const = ConstellationParser()
    stars = const.parse_file()
    print(stars)

if __name__ == "__main__":
    main()