from abc import abstractmethod

class Parser():
    def __init__(self, filepath):
        self.filepath = filepath
        self.ElementsList = []

    @abstractmethod
    def parse_file(self):
        pass
