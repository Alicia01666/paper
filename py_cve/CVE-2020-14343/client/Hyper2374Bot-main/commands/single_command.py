
class SingleCommand(object):
    def __init__(self, GUID, name, alias, sleep, text, level):
        self.__GUID = GUID
        self.__name = name
        self.__alias = alias
        self.__sleep = sleep
        self.__text = text
        self.__level = level

    @property
    def name(self):
        return self.__name

    @property
    def alias(self):
        return self.__alias

    @property
    def text(self):
        return self.__text
