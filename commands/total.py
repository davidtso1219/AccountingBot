from multiprocessing.sharedctypes import Value
import database
from constant import *
from discord import Embed, Color
from discord.ext import commands
from utils import get_time_info, check_author, send_red_warning

def setup(bot):
    bot.add_command(total)

@commands.command()
async def total(ctx, date : str =''):

    author = ctx.author.name
    mention = f'{ctx.author.mention}'
    msg = await ctx.send(mention)
    embed = Embed(color=Color.from_rgb(255, 204, 153))

    if not check_author(author):
        await send_red_warning(msg, embed, INVALID_AUTHOR)
        return

    try:
        time_info = get_time_info(author, date)
    except ValueError:
        return

    info = {"name": author, **time_info}
    sum_price = database.total(**info)
    embed.description = f':money_with_wings: You have spent **{sum_price}** '
    embed.description += f'{ "TWD" if author != "daaviid" else "dollars"} '
    embed.description += f'on **{info["month"]}{("/" + str(info["day"])) if info["day"] else ""}/{info["year"]}**'
    await ctx.send(embed=embed)
