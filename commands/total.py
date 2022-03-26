import server
from utils import get_time_info, validate_author
from discord import Embed, Color
from discord.ext import commands

def setup(bot):
    bot.add_command(total)

@commands.command()
async def total(ctx, date : str =''):

    author = ctx.author.name
    mention = f'{ctx.author.mention}'
    msg = await ctx.send(mention)
    embed = Embed(color=Color.from_rgb(255, 204, 153))

    if not (await validate_author(author, msg, embed)):
        return

    time_info = await get_time_info(date, author, msg, embed)
    if not time_info:
        return

    info = {"name": author}
    types = ['month', 'day', 'year']
    for i in range(3):
        info[types[i]] = int(time_info[i])

    # sum_price = server.total(**info)
    sum_price = 0
    embed.description = f':money_with_wings: You have spent **{sum_price}** { "TWD" if author != "daaviid" else "dollars"} on **{info["month"]}/{info["day"]}/{info["year"]}**'
    await ctx.send(embed=embed)
