PREFIX = "$"
SEND_DELAY = 0.5

import discord
from discord.ext import commands
import sys
import os
from dotenv import load_dotenv
import shlex
import asyncio 

load_dotenv('.env')
client = commands.Bot(command_prefix=PREFIX, intents=discord.Intents.all())

@client.event
async def on_ready():
    print('Ready')
    
    target_guild = None
    message = 'Glory to the GCS!'
    
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
            if len(arguments) < 2:
                try:
                    print(message)
                except:
                    print('No set message')
                continue

            if arguments[1] == 'none':
                message = 'Glory to the GCS!'
                print('Set message to default')
            else:
                message = arguments[1]
                print('Set message to {}'.format(arguments[1]))
        elif arguments[0] == 'run':
            if not target_guild:
                print('No target guild')
                continue

            webhooks = []
            for channel in target_guild.text_channels:
                try:
                    webhook = await channel.create_webhook(name='RAT')
                    webhooks.append(webhook)
                except Exception as error_message:
                    print(f'Could not create webhook in {channel.name}')
                    print(error_message)
                else:
                    print(f'Created webhook in {channel.name}')

            while True:
                for webhook in webhooks:
                    await webhook.send(message)
                    print(f'Fired webhook {webhook.url}')
                await asyncio.sleep(SEND_DELAY)

        else:
            print('Invalid command')

@client.command()
async def ping(context):
    ping = round(client.latency * 1000)
    await context.send(f'{ping} ms')

client.run(os.getenv('TOKEN'))

