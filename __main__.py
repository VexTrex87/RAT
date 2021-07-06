PREFIX = "$"

import discord
from discord.ext import commands
import sys
import os
from dotenv import load_dotenv
import shlex

load_dotenv('.env')
client = commands.Bot(command_prefix=PREFIX, intents=discord.Intents.all())
target_guild = None

@client.event
async def on_ready():
    print('Ready')
    
    while True:
        input_text = input('$ ')
        arguments = shlex.split(input_text)
    
        if arguments[0] == 'help':
            print('help     Shows this list')
            print('exit     Stops the program')
            print('target   Sets a target guild')
            print('setmsg   Sets the RAT message')
            print('run      Runs RAT on the target guild')
        elif arguments[0] == 'exit':
            sys.exit()
        elif arguments[0] == 'target':
            if len(arguments) < 2:
                try:
                    print(target_guild.name)
                except:
                    print('No target guild')
                continue

            if arguments[1] == 'none':
                target_guild = None
                print('Removed target guild')
                continue

            try:
                arguments[1] = int(arguments[1])
            except ValueError:
                print('Could not convert guild id {} into an integer'.format(arguments[1]))
                continue

            guild = client.get_guild(arguments[1])
            if not guild:
                print('Could not find guild {}'.format(arguments[1]))
                continue

            target_guild = guild
            print(f'Set target guild to {guild.name}')
        elif arguments[0] == 'setmsg':
            pass
        elif arguments[0] == 'run':
            pass
        else:
            print('Invalid command')

@client.command()
async def ping(context):
    ping = round(client.latency * 1000)
    await context.send(f'{ping} ms')

client.run(os.getenv('TOKEN'))

