import database
from constant import *
from discord import Embed, Color
from discord.ext import commands
from utils import check_author, send_red_warning, confirm_emoji, get_embed_from_record

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
    title = 'Is this the one you want to delete?'
    embed = get_embed_from_record(title, last_record)
    await msg.edit(embed=embed)

    #
    try:
        await confirm_emoji(ctx, msg)
    except TimeoutError:
        await send_red_warning(msg, INACTIVITY_DESCRIPTION)
        return

    id = last_record[0]
    database.delete(id)
    await msg.clear_reactions()
    embed = Embed(description=':white_check_mark:  **That Record Is Deleted!**', color=Color.green())
    await msg.edit(embed=embed)