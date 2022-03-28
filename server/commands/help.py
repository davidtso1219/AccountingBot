from discord import Embed, Color
from discord.ext import commands

def setup(bot):
    bot.add_command(help)

@commands.command()
async def help(ctx):

    commands = {
        'add': {
            'usage': '$add <price> (date)',
            'description': 'Add an expense at give price on the given date',
            'examples': [
                '`$add 12`: Add an expense of 12 dollars today',
                '`$add 12 3/22`: Add an expense of 12 dollars on 3/22/2022',
                '`$add 12 3/22/22`: Add an expense of 12 dollars on 3/22/2022'
            ]
        },
        'delete': {
            'usage': '$delete',
            'description': 'Delete your last expense',
            'examples': []
        },
        'top': {
            'usage': '$top (date) (num)',
            'description': 'Show the most costly expenses',
            'examples': [
                '`$top`: Show the most 5 costly expenses today',
                '`$top 3/22`: Show the most 5 costly expenses on 3/22/2022',
                '`$top 8 3/22/22`: Show the most 8 costly expenses on 3/22/2022'
            ]
        },
        'total': {
            'usage': '$total (date)',
            'description': 'Show the total expenses on the given date',
            'examples': [
                '`$total`: Show the total expenses today',
                '`$top 3/22`: Show the total expenses on 3/22/2022'
            ]
        },
        'help': {
            'usage': '$help',
            'description': 'Show this message',
            'examples': []
        }
    }

    embed = Embed(title='Accounting Bot', description='**Available commands:**\n', color=Color.from_rgb(255, 204, 153))
    for data in commands.values():
        embed.description += '\n**' + data['usage'] + '**\n'
        embed.description += data['description'] + '\n'

        for example in data['examples']:
            embed.description += example + '\n'

    await ctx.send(embed=embed)
