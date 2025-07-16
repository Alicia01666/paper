class TimerCommand(object):
    def __init__(self, GUID, name, alias, time, text, lines):
        self.__GUID = GUID
        self.__name = name
        self.__alias = alias
        self.__time = time
        self.__text = text
        self.__lines = lines

    @property
    def name(self):
        return self.__name

    @property
    def alias(self):
        return self.__alias

    @property
    def time(self):
        return self.__time

    @property
    def text(self):
        return self.__text

    @property
    def lines(self):
        return self.__lines
