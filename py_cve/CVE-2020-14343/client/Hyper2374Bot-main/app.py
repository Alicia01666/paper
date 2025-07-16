from controllers.commands_controller import CommandsController
from generals.add_commands import *
from bot.twitch_bot import TwitchBot

# pip install pipenv
# pipenv --python 3.7
# pipenv install twitchio
# pipenv install pyyaml
# pipenv run python app.py

if __name__ == "__main__":
    single_command_list, timer_command_list = CommandsController().get()
    add_single_command(TwitchBot, single_command_list)
    bot = TwitchBot(timer_command_list)
    bot.run()
