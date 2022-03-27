import os
from discord import Intents
from server import keep_alive
from dotenv import load_dotenv
from discord.ext.commands import Bot

load_dotenv()
intents = Intents(messages=True, guilds=True, members=True, reactions=True)
bot = Bot(command_prefix='$', intents=intents)
extensions = [
    'commands.add',
    'commands.reload',
    'commands.clear',
    'commands.total',
    'commands.delete',
    'commands.top',
    'commands.help'
]


@bot.before_invoke
async def before_invoke(ctx):
    print(f'[cmd] "{ctx.command.name}" invoked with "{ctx.message.content}" by {ctx.message.author}')


# Ready
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    guild_name = 'my own server' if 'Test' in str(bot.user) else '嵐酉杉 & 藍友三'

    for guild in bot.guilds:
        if guild.name == guild_name:
            for channel in guild.channels:
                if channel.name == 'bot-spam':
                    await channel.send(f'{guild.owner.mention} I am restarted.')


if __name__ == '__main__':
    keep_alive()
    bot.remove_command('help')
    for extension in extensions:
        bot.load_extension(extension)
    bot.run(os.getenv('TOKEN'))
