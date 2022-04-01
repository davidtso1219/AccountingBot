import database
from constant import *
from discord import Embed, Color
from discord.ext import commands
from utils import send_red_warning

def setup(bot):
    bot.add_command(clear)

@commands.command()
async def clear(ctx):

    author = ctx.author.name
    mention = f'{ctx.author.mention}'
    msg = await ctx.send(mention)
    embed = Embed(color=Color.from_rgb(255, 204, 153))

    if author != 'daaviid':
        await send_red_warning(msg, INVALID_AUTHOR)
        return

    database.create()
    embed = Embed(description=':white_check_mark:  **New Table Created!**', color=Color.green())
    await ctx.send(embed=embed)
