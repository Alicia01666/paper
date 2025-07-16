import os

class FileManagement(object):
    def __init__(self):
        pass

    @staticmethod
    def root():
        """ To fetch the project root path.
        """
        return os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
