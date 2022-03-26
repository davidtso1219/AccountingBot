import pytz
from discord import Color, Embed
from datetime import datetime, timedelta

def get_args(info, columns):
    args = []
    for c in columns:
        args.append(info[c])
    return args

def check_author(author):
    return author == 'daaviid' or author == 'Jamie.lin'

async def send_red_warning(msg, description):
    await msg.edit(embed=Embed(description=description, color=Color.from_rgb(255, 0, 0)))
    return

def set_time_info(time_info, date, format):

    date = datetime.strptime(date, format)
    if format == '%m/%d/%Y' or format == '%m/%d/%y':
        time_info['month'] = date.month
        time_info['day'] = date.day
        time_info['year'] = date.year

    elif format == '%m/%Y':
        time_info['month'] = date.month
        time_info['day'] = None
        time_info['year'] = date.year

    elif format == '%m/%d':
        time_info['month'] = date.month
        time_info['day'] = date.day
        time_info['year'] = datetime.now().year

def get_time_info(author, date=''):
    '''
    check if the date from the user is valid
    '''
    time_info = {}
    formats = ["%m/%d/%Y", "%m/%d/%y", "%m/%Y", "%m/%d"]

    # if date is provided
    if date:
        for format in formats:
            try:
                set_time_info(time_info, date, format)
                return time_info
            except ValueError:
                pass

    # get the current date
    else:
        n = 0 if author == 'daaviid' else 15
        today = datetime.now(pytz.timezone('US/Pacific')) + + timedelta(hours=n)
        time_info = today.strftime("%m/%d/%Y").split('/')
        return time_info
