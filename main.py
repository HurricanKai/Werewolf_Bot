'''

888       888                                                  888  .d888       888888b.            888    
888   o   888                                                  888 d88P"        888  "88b           888    
888  d8b  888                                                  888 888          888  .88P           888    
888 d888b 888  .d88b.  888d888  .d88b.  888  888  888  .d88b.  888 888888       8888888K.   .d88b.  888888 
888d88888b888 d8P  Y8b 888P"   d8P  Y8b 888  888  888 d88""88b 888 888          888  "Y88b d88""88b 888    
88888P Y88888 88888888 888     88888888 888  888  888 888  888 888 888          888    888 888  888 888    
8888P   Y8888 Y8b.     888     Y8b.     Y88b 888 d88P Y88..88P 888 888          888   d88P Y88..88P Y88b.  
888P     Y888  "Y8888  888      "Y8888   "Y8888888P"   "Y88P"  888 888          8888888P"   "Y88P"   "Y888 
                                                                                                           
                         - = https://github.com/werewolves-devs/werewolf_bot = -
                                                                                                           
'''

import discord
import random
import asyncio

# Import config data
from config import prefix, welcome_channel
from management.db import db_set
from interpretation.ww_head import process
import config


client = discord.Client()


# Whenever a message is sent.
@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    # Check if the message author has the Game Master role
    isGameMaster = False
    if False: # somebody fix this
        isGameMaster = True

    result = process(message,isGameMaster)

    temp_msg = []

    gamelog_channel = client.get_channel(int(config.game_log))
    botspam_channel = client.get_channel(int(config.bot_spam))
    storytime_channel = client.get_channel(int(config.story_time))

    for mailbox in result:

        for element in mailbox.gamelog:
            msg = await gamelog_channel.send(element.content)
            if element.temporary == True:
                temp_msg.append(msg)

        for element in mailbox.botspam:
            msg = await botspam_channel.send(element.content)
            if element.temporary == True:
                temp_msg.append(msg)

        for element in mailbox.storytime:
            msg = await storytime_channel.send(element.content)
            if element.temporary == True:
                temp_msg.append(msg)

        for element in mailbox.channel:
            msg = await client.get_channel(element.destination).send(element.content)
            if element.temporary == True:
                temp_msg.append(msg)

        for element in mailbox.player:
            msg = await client.get_channel('''How did we do this again?''').send(element.content)
            if element.temporary == True:
                temp_msg.append(msg)

        for element in mailbox.oldchannels:
            # element.channel - channel to be edited;
            # element.victim - person's permission to be changed;
            # element.number - type of setting to set to:
                # 0 - no access     (no view, no type)
                # 1 - access        (view + type)
                # 2 - frozen        (view, no type)
                # 3 - abducted      (no view, no type)
                # 4 - dead          (dead role?)

            # TODO
            pass

        for element in mailbox.newchannels:
            # element.name - name of the channel;
            # element.owner - owner of the channel;
            # element.members - members of the channel
            # element.settlers - members for whom this shall become their home channel
            #
            # @Participant      - no view + type
            # @dead Participant - view + no type
            # @everyone         - no view + no type

            # All you need to do is create a channel where only the channel owner has access.
            # The other members are given access through another Mailbox.
            # You could make the work easier if you also posted a cc channel message already over here.

            if element.owner not in element.members:
                element.members.append(element.owner)
            for buddy in element.settlers:
                if buddy not in element.members:
                    print("Warning: I'm adding settlers to a channel!")

            for buddy in element.settlers:
                db_set(buddy,"channel",'''id of the channel you just created''')

    # Delete all temporary messages after "five" seconds.
    await asyncio.sleep(5)
    for msg in temp_msg:
        await client.delete_message(msg)


# Whenever the bot regains his connection with the Discord API.
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

    await client.send_message(client.get_channel(welcome_channel),'Beep boop! I just went online!')

client.run(config.TOKEN)
