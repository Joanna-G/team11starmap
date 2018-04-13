import os
import sys


class ProjectDirectory:
    def __init__(self):
        self.directory = ''
        if getattr(sys, 'frozen', False):
            self.directory = os.path.dirname(sys.executable)
        elif __file__:
            self.directory = os.path.dirname(__file__)
        self.dll_file = os.path.join(self.directory, 'gsdll64.dll')
        self.lib_file = os.path.join(self.directory, 'gsdll64.lib')
        self.so_file = os.path.join(self.directory, 'libgs.9.23.so')
        self.dylib_file = os.path.join(self.directory, 'libgs.9.23.dylib')
        print(self.dll_file)
