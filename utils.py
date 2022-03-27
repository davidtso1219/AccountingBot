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

def get_details_field(details):
    return f'**Detail**\n{details if len(details) < 50 else details[:50] + "..."}'

def set_time_info(time_info, date, format):

    date = datetime.strptime(date, format)
    if format == '%m/%d/%Y' or format == '%m/%d/%y':
        time_info['month'] = date.month
        time_info['day'] = date.day
        time_info['year'] = date.year

    elif format == '%m/%Y' or format == '%m/%y':
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
    formats = ["%m/%d/%Y", "%m/%d/%y", "%m/%Y", "%m/%y", "%m/%d"]

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
        today = (datetime.now(pytz.timezone('US/Pacific')) + + timedelta(hours=n)).strftime("%m/%d/%Y")
        set_time_info(time_info, today, "%m/%d/%Y")
        return time_info


async def confirm_emoji(ctx, msg):
    emojis = ['✅', '❌']
    for emoji in emojis:
        await msg.add_reaction(emoji)

    def check(reaction, user):
        emoji = str(reaction.emoji)
        return (
            emoji in emojis
            and user == ctx.author
            and reaction.message.id == msg.id
        )

    try:
        reaction, user = await ctx.bot.wait_for(
            "reaction_add", timeout=10.0, check=check
        )
    except TimeoutError:
        raise TimeoutError()

    return str(reaction.emoji) == emojis[0]