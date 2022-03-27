import database
from constant import *
from emojis import cats_emojis
from discord import Embed, Color
from discord.ext import commands
from utils import check_author, send_red_warning, get_time_info

def setup(bot):
    bot.add_command(top)

@commands.command()
async def top(ctx, date : str ='', num : str = "5"):

    author = ctx.author.name
    mention = f'{ctx.author.mention}'
    msg = await ctx.send(mention)
    embed = Embed(color=Color.from_rgb(255, 204, 153))

    if not check_author(author):
        await send_red_warning(msg, INVALID_AUTHOR)
        return

    try:
        num = int(num)
        error = False
    except:
        error = True

    if error or num > 10 or num <= 0:
        await send_red_warning(msg, f':no_entry: **{num} is invalid (0 < num <= 10)**')
        return

    try:
        time_info = get_time_info(author, date)
    except ValueError:
        return

    info = {"name": author, 'num': num, **time_info}
    print(info)
    records = database.top(**info)

    if not records:
        await send_red_warning(msg, f':warning: Sorry I do not find any records on **{info["month"]}{("/" + str(info["day"])) if info["day"] else ""}/{info["year"]}**')
        return

    embed.title = 'Here are the records!'
    embed.description = ''
    max_len = max([len(str(r[COLUMNS.index('price')])) for r in records])
    max_len = max_len if max_len <= 6 else 6

    for record in records:

        month = str(record[COLUMNS.index('month')])
        day = str(record[COLUMNS.index('day')])
        year = str(record[COLUMNS.index('year')])
        date = ('0' if len(month) == 1 else '') + month + '/' + ('0' if len(day) == 1 else '') + day + '/' + year

        price = str(record[COLUMNS.index('price')])
        price = ' ' * (max_len - len(price)) + price if len(price) < max_len else price

        category = record[COLUMNS.index('category')]
        detail = record[COLUMNS.index('detail')]

        embed.description += f'{cats_emojis[category]} `{date}` `{price}` `{detail}`\n\n'

    await msg.edit(embed=embed)
