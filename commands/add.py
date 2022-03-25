import pytz, server
from asyncio import TimeoutError
from discord import Embed, Color
from discord.ext import commands
from datetime import datetime, timedelta
from emojis import cats_emojis, num_emojis
from utils import get_time_info, validate_author

def setup(bot):
    bot.add_cog(Add(bot))

class Add(commands.Cog):

    def __init__ (self, bot):
        self.bot = bot

    @commands.command()
    async def add(self, ctx, price : str ='', date : str =''):

        # check if price is provided
        if not price:
            await ctx.send(f'`Usage: <price> (date: MM/DD/YYYY)`')
            return

        info = {'price': float(price)}
        author = ctx.author.name
        mention = f'{ctx.author.mention}'
        msg = await ctx.send(mention)
        embed = Embed(color=Color.from_rgb(255, 204, 153))

        # check the authors
        info['user'] = author
        if not (await validate_author(author, msg, embed)):
            return

        time_info = await get_time_info(date, author, msg, embed)
        if not time_info:
            return

        #
        types = ['month', 'day', 'year']
        embed.title = 'Enter details of this consumption'
        embed.add_field(name='Price', value=price)
        for i in range(3):
            embed.add_field(name=types[i].title(), value=time_info[i])
            info[types[i]] = int(time_info[i])
        await msg.edit(embed=embed)

        #
        def check(msg):
            return msg.author.name == author and msg.channel == ctx.channel and not msg.content.startswith('$')

        #
        try:
            details = await self.bot.wait_for("message", check=check, timeout=20.0)
            details = details.content
        except TimeoutError:
            await self.close_prompt(ctx, msg)
            return
        info['det'] = details

        # create a new embed to get the category
        embed.title = f'Choose one of the categories below'
        embed.description = f'**Detail**\n{details if len(details) < 50 else details[:50] + "..."}'
        await msg.delete()
        msg = await ctx.send(embed=embed)

        # get the category
        try:
            cat = await self.get_category(ctx)
        except TimeoutError:
            await self.close_prompt(ctx, msg)
            return
        except ValueError:
            await msg.delete()
            return
        info['cat'] = cat

        # add category to the embed
        embed.add_field(name='Category', value=cat)
        embed.title = 'Is the following information is all correct?'
        await msg.edit(embed=embed)

        try:
            correct = await self.emoji_confirm(ctx, msg)
        except TimeoutError:
            await self.close_prompt(ctx, msg)
            return

        await msg.delete()
        if correct:
            title = ':checkered_flag: Ok pushing to the database!'
            color = Color.from_rgb(0, 255, 0)

        else:
            title = 'Please try again...'
            color = Color.from_rgb(255, 0, 0)

        await ctx.send(embed=Embed(title=title, color=color))
        print(info)
        # server.push(**info)


    async def emoji_confirm(self, ctx, msg):
        emojis = ['✅', '❌']
        for emoji in emojis:
            await msg.add_reaction(emoji)

        def check(reaction, user):
            emoji = str(reaction.emoji)
            return (
                emoji in emojis
                and user == ctx.author
                and reaction.message.id == msg.id
                and user.id != self.bot.user.id
            )

        try:
            reaction, user = await ctx.bot.wait_for(
                "reaction_add", timeout=10.0, check=check
            )
        except TimeoutError:
            raise TimeoutError()

        return str(reaction.emoji) == emojis[0]

    async def get_category(self, ctx):
        title = 'Choose categories from the following options'
        color = Color.blue()
        description = ''
        cats = ['foods', 'transportation', 'entertainment', 'grocercy']
        n = len(cats)

        for i in range(n):
            description += f'`{i + 1}` {cats[i]} {cats_emojis[cats[i]]} \n\n'

        embed = Embed(title=title, description=description, color=color)
        msg = await ctx.send(embed=embed)
        for i in range(n):
            await msg.add_reaction(num_emojis[i])

        await msg.add_reaction('🗑️')

        def check(reaction, user):
            emoji = str(reaction.emoji)
            return (
                (emoji in num_emojis or emoji == '🗑️')
                and user == ctx.author
                and reaction.message.id == msg.id
                and user.id != self.bot.user.id
            )

        try:
            reaction, user = await ctx.bot.wait_for(
                "reaction_add", timeout=10.0, check=check
            )
        except TimeoutError:
            await msg.delete()
            raise TimeoutError()

        user_choice = str(reaction.emoji)
        await msg.delete()

        if user_choice == '🗑️':
            raise ValueError()

        return cats[num_emojis.index(str(reaction.emoji))]


    async def close_prompt(self, ctx, msg):
        await msg.delete()
        description = ":no_entry: **Prompt closed due to inactivity.**"
        color = Color.from_rgb(255, 0, 0)
        await ctx.send(embed=Embed(description=description, color=color))

