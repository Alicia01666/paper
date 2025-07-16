from os import name
from twitchio.ext import commands

def add_single_command(cls, single_commands_list):

    for cmd in single_commands_list:
        @commands.command(name='%s' % cmd.name, aliases=cmd.alias)
        async def single_command(
            self, ctx, name=cmd.name,
            text=cmd.text
            ):
            await ctx.send(f'' + '%s' % text)

        setattr(cls, cmd.name, single_command)
