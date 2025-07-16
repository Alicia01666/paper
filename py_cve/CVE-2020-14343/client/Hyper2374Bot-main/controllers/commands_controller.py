"""
@File

@Copyright
    Copyright (C) 2021 Jason Lin <jason40418@gmail.com>

    Permission is hereby granted, free of charge, to any person obtaining a
    copy of this software and associated documentation files (the "Software"),
    to deal in the Software without restriction, including without limitation
    the rights to use, copy, modify, merge, publish, distribute, sublicense,
    and/or sell copies of the Software, and to permit persons to whom the
    Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
    DEALINGS IN THE SOFTWARE.

@Comment

@Reference
"""
from commands.timer_command import TimerCommand
from commands.single_command import SingleCommand
from utils.config import Config

class CommandsController(object):
    def __init__(self):
        self.__config = Config("commands.yaml")
        self.__status, self.__config_data = self.__config.get()
        self.__single_command_list = self.__get_single_command()
        self.__timer_command_list = self.__get_timer_command()

    def get(self):
        return self.__single_command_list, self.__timer_command_list

    def __get_single_command(self):
        result = list()

        for cmd in self.__config_data['single']:
            result.append(SingleCommand(
                cmd['GUID'], cmd['name'], cmd['alias'], cmd['sleep'],
                cmd['text'], cmd['level']
            ))

        return result

    def __get_timer_command(self):
        result = list()

        for cmd in self.__config_data['timer']:
            result.append(TimerCommand(
                cmd['GUID'], cmd['name'], cmd['alias'], cmd['time'],
                cmd['text'], cmd['lines']
            ))

        return result
