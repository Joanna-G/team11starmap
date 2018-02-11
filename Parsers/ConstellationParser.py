import csv
import os.path

class ConstellationParser():
    def __init__(self):
        self.ConstellationList = []

    # Parses the input File
    def parse_file(self):
        path = os.path.join('resources', 'Constellation2.csv')
        file = csv.reader(open(path, newline=''), delimiter=',')

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
                self.ConstellationList.append(connectionList[:])
                connectionList.clear()
                connectionList.append(row[0])

        # Remove the first empty element of the list
        self.ConstellationList.pop(0)
        return self.ConstellationList