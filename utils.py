import pytz
from discord import Color
from datetime import datetime, timedelta

def get_args(info, columns):
    args = []
    for c in columns:
        args.append(info[c])
    return args

async def validate_author(author, msg, embed):
    '''
    '''
    if author != 'daaviid' and author != 'Jamie.lin':
        embed.description = f':warning: You are **NOT** supposed to add!'
        embed.color = Color.from_rgb(255, 0, 0)
        await msg.edit(embed=embed)
        return False

    return True

async def get_time_info(date, author, msg, embed):
    '''
    '''
    # see if the date from the user is valid
    if date:
        try:
            datetime.strptime(date, "%m/%d/%Y")
            time_info = date.split('/')
        except ValueError:
            embed.description = f':warning: `{date}` is **invalid**'
            embed.color = Color.from_rgb(255, 0, 0)
            await msg.edit(embed=embed)
            return

    # get the current date
    else:
        n = 0 if author == 'daaviid' else 15
        today = datetime.now(pytz.timezone('US/Pacific')) + + timedelta(hours=n)
        time_info = today.strftime("%m/%d/%Y").split('/')

    return time_info