import os
from twitchio.ext import commands
from utils.timer import Timer

class TwitchBot(commands.Bot):

    def __init__(self, timers_commands=None):
        self.__channels = os.environ['CHANNEL'].split(',')
        super().__init__(
            irc_token        = os.environ['TMI_TOKEN'],
            client_id        = os.environ['CLIENT_ID'],
            nick             = os.environ['BOT_NICK'],
            prefix           = os.environ['BOT_PREFIX'],
            initial_channels = self.__channels
        )
        self.__timers_commands = timers_commands
        self.__timers_list = list()
        self.__chatter_count = {
            channel.lower(): 0 for channel in self.__channels
        }

    async def event_ready(self):
        """ The event when the bot is online!

        This function would only call once.
        """
        print(f"{os.environ['BOT_NICK']} is online!")
        ws = self._ws  # this is only needed to send messages within event_ready
        self.setup_timer()

        for channel in self.__channels:
            await ws.send_privmsg(channel, f"/me has landed!")

    async def event_message(self, ctx):
        """ This function would execute each time once the message send to chat.
        """
        # make sure the bot ignores itself and the streamer
        chatroom = ctx.author.name.lower()
        if ctx.author.name.lower() == os.environ['BOT_NICK'].lower():
            return

        self.__chatter_count[chatroom] = self.__chatter_count[chatroom] + 1

        await self.handle_commands(ctx)

        if 'hello' in ctx.content.lower():
            await ctx.channel.send(f"Hi, @{ctx.author.name}!")

    def setup_timer(self):
        for timer in self.__timers_commands:
            async def timer_message(time=timer.time, msg=timer.text, lines=timer.lines):
                curr_lines = self.__chatter_count
                print(self.__chatter_count)
                for channel in self.__channels:
                    if curr_lines[channel.lower()] >= lines:
                        curr_lines[channel.lower()] = 0
                        await self._ws.send_privmsg(channel, msg)

            self.__timers_list.append(
                Timer(timer.time, timer_message)
            )
