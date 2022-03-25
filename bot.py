import os
from app import keep_alive
from discord import Intents
from dotenv import load_dotenv
from discord.ext.commands import Bot

load_dotenv()
intents = Intents(messages=True, guilds=True, members=True, reactions=True)
bot = Bot(command_prefix='$', intents=intents)
extensions = [
    'commands.add',
    'commands.reload',
    'commands.create',
    'commands.total'
]


@bot.before_invoke
async def before_invoke(ctx):
    print(f'[cmd] "{ctx.command.name}" invoked with "{ctx.message.content}" by {ctx.message.author}')


# Ready
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

    for guild in bot.guilds:
        if guild.name == '嵐酉杉 & 藍友三':
            for channel in guild.channels:
                if channel.name == 'bot-spam':
                    await channel.send(f'{guild.owner.mention} I am restarted.')


if __name__ == '__main__':
    keep_alive()
    for extension in extensions:
        bot.load_extension(extension)
    bot.run(os.getenv('TOKEN'))
