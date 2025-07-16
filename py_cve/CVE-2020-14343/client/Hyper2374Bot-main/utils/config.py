import os
import yaml
from utils.file_management import FileManagement

class Config(object):
    def __init__(self, file_name, path="config"):
        self.__root = FileManagement.root()
        self.__path = path
        self.__file_name = file_name
        self.__file_path = os.path.join(
            self.__root,
            self.__path,
            self.__file_name
            )

        # Read the Yaml file
        self.__status, self.__data = self.__read()

    def get(self):
        return self.__status, self.__data

    def __read(self):
        stream = open(self.__file_path, 'r', encoding='utf8')
        data = yaml.load(stream, Loader=yaml.CLoader)
        return True, data
