from discord import Embed, Color
from discord.ext import commands

def setup(bot):
    bot.add_cog(Reload(bot))

class Reload(commands.Cog):
    def __init__ (self, bot):
        self.bot = bot

    @commands.command()
    async def reload(self, ctx, command=''):

        commands = [c.name for c in self.bot.commands]
        if not command:
            embed = Embed(description=':no_entry:  **Please Specify A Command!**', color=Color.red())

        elif command in commands:
            self.bot.reload_extension(f'commands.{command}')
            embed = Embed(description=f':white_check_mark:  **{command} reloaded!**', color=Color.green())

        else:
            embed = Embed(description=f':warning:  **{command} NOT FOUND!**', color=Color.orange())

        await ctx.send(embed=embed)
