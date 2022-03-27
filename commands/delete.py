import database
from constant import *
from discord import Embed, Color
from discord.ext import commands
from utils import check_author, send_red_warning, get_details_field, confirm_emoji

def setup(bot):
    bot.add_command(delete)

@commands.command()
async def delete(ctx):
    author = ctx.author.name
    mention = f'{ctx.author.mention}'
    msg = await ctx.send(mention)
    embed = Embed(color=Color.from_rgb(255, 204, 153))

    #
    if not check_author(author):
        await send_red_warning(msg, embed, INVALID_AUTHOR)
        return

    #
    last_record = database.get_last_record(author)
    if not last_record:
        await send_red_warning(msg, embed, INVALID_RECORD)
        return

    #
    last_record = last_record[0]
    embed.title = 'Is this the one you want to delete?'
    embed.description = get_details_field(last_record[COLUMNS.index('details')])
    columns = ['price', 'month', 'day', 'year']
    for c in columns:
        embed.add_field(name=c.title(), value=last_record[COLUMNS.index(c)])

    id = last_record[0]
    embed.add_field(name='ID', value=id)
    await msg.edit(embed=embed)

    #
    try:
        await confirm_emoji(ctx, msg)
    except TimeoutError:
        await send_red_warning(msg, INACTIVITY_DESCRIPTION)
        return

    database.delete(id)
    await msg.clear_reactions()
    embed = Embed(description=':white_check_mark:  **That Record Is Deleted!**', color=Color.green())
    await msg.edit(embed=embed)