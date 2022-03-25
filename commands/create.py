from server import cursor
from discord import Embed, Color
from discord.ext import commands

def setup(bot):
    bot.add_command(create)

@commands.command()
async def create(ctx):
    # cursor.execute("DROP TABLE IF EXISTS records")
    # cursor.execute('''
    #     CREATE TABLE records (
    #         _id integer PRIMARY KEY AUTOINCREMENT,
    #         price float,
    #         month int,
    #         day int,
    #         year int,
    #         user varchar(10),
    #         category varchar(20),
    #         detail varchar(100)
    #     )
    # ''')
    embed = Embed(description=':white_check_mark:  **New Table Created!**', color=Color.green())
    await ctx.send(embed=embed)