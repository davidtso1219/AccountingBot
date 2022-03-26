import server
from discord import Embed, Color
from discord.ext import commands

def setup(bot):
    bot.add_command(create)

@commands.command()
async def create(ctx):
    server.create()
    embed = Embed(description=':white_check_mark:  **New Table Created!**', color=Color.green())
    await ctx.send(embed=embed)