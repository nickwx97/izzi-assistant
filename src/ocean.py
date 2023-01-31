# This file is part of Izzi Assistant.

# Izzi Assistant is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.

# Izzi Assistant is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Izzi Assistant; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

from datetime import datetime
from dateutil.relativedelta import relativedelta
import discord
import os
import re
import asyncio
from sqlite3 import IntegrityError

from db import DB
import occmd

from dotenv import load_dotenv

# prepare static data and objects
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
database = DB()
client = discord.Client()
dungeon_open = False
izzi_id = 784851074472345633
admin_list = [
    # insert admin discord ids here
]
channel_blacklist=[
    # insert discord channel ids here
]

async def reminder_loop(client, database):

    # loop every second to check for reminders
    asyncio.ensure_future(reminder_loop_task(client, database))
    now = int(datetime.now().timestamp())

    # check if monday GMT 00:00:00
    if datetime.now().weekday() == 0 and datetime.now().hour == 0 and datetime.now().minute == 0 and datetime.now().second == 0:
        await occmd.monday_guild_bonk(client.get_channel(971698533507948575), database)


    for mana in database.get_expired_mana(now):
        channel = client.get_channel(database.get_last_channel(mana[0]))
        if channel is None:
            continue
        
        # check ping reminder
        if database.get_ping_reminder(mana[0]) == 1:
            await channel.send(f"<@{mana[0]}> **Your __mana__ is full! To battle!!**")
        else:
            user = await client.fetch_user(mana[0])
            username = user.name
            await channel.send(f"**{username} Your __mana__ is full! To battle!!**")
        database.clear_mana_reminded(mana[0])

    if dungeon_open:
        for dungeon_mana in database.get_expired_dungeon_mana(now):
            channel = client.get_channel(database.get_last_channel(dungeon_mana[0]))
            if channel is None:
                continue
            
            if database.get_ping_reminder(dungeon_mana[0]) == 1:
                await channel.send(f"<@{dungeon_mana[0]}> **Your __dungeon mana__ is full! To the dungeons!!**")
            else:
                user = await client.fetch_user(dungeon_mana[0])
                username = user.name
                await channel.send(f"**{username} Your __dungeon mana__ is full! To the dungeons!!**")
            database.clear_dungeon_mana_reminded(dungeon_mana[0])

    for raid in database.get_expired_raid(now):
        channel = client.get_channel(database.get_last_channel(raid[0]))
        if channel is None:
            continue

        if database.get_ping_reminder(raid[0]) == 1:
            await channel.send(f"<@{raid[0]}> **Your __raid battle__ is ready!**")
        else:
            user = await client.fetch_user(raid[0])
            username = user.name
            await channel.send(f"**{username} Your __raid battle__ is ready!**")
        database.clear_raid_reminded(raid[0])

    for lotto in database.get_expired_lotto(now):
        channel = client.get_channel(database.get_last_channel(lotto[0]))
        if channel is None:
            continue
        
        if database.get_ping_reminder(lotto[0]) == 1:
            await channel.send(f"<@{lotto[0]}> **Your __lotto__ is ready! Time to gamble!!**")
        else:
            user = await client.fetch_user(lotto[0])
            username = user.name
            await channel.send(f"**{username} Your __lotto__ is ready! Time to gamble!!**")
        database.clear_lotto_reminded(lotto[0])
    
    for hr in database.get_expired_hr(now):
        channel = client.get_channel(database.get_last_channel(hr[0]))
        if channel is None:
            continue
        
        if database.get_ping_reminder(hr[0]) == 1:
            await channel.send(f"<@{hr[0]}> **Your __hr__ is ready! Free mana!!1!**")
        else:
            user = await client.fetch_user(hr[0])
            username = user.name
            await channel.send(f"**{username} Your __hr__ is ready! Free mana!!1!**")

        database.clear_hr_reminded(hr[0])

    for spawn in database.get_expired_spawn(now):
        channel = client.get_channel(database.get_last_channel(spawn[0]))
        if channel is None:
            continue
        
        if database.get_ping_reminder(spawn[0]) == 1:
            await channel.send(f"<@{spawn[0]}> **Your __raid spawn__ is ready!**")
        else:
            user = await client.fetch_user(spawn[0])
            username = user.name
            await channel.send(f"**{username} Your __raid spawn__ is ready!**")
        database.clear_spawn_reminded(spawn[0])

    for vote in database.get_expired_vote(now):
        channel = client.get_channel(database.get_last_channel(vote[0]))
        if channel is None:
            continue
        
        if database.get_ping_reminder(vote[0]) == 1:
            await channel.send(f"<@{vote[0]}> **Your __vote__ is ready!**")
        else:
            user = await client.fetch_user(vote[0])
            username = user.name
            await channel.send(f"**{username} Your __vote__ is ready!**")
        database.clear_vote_reminded(vote[0])

    for dono in database.get_expired_guild_remind(now):
        channel = client.get_channel(database.get_last_channel(dono[0]))
        if channel is None:
            continue
        
        if database.get_ping_reminder(dono[0]) == 1:
            await channel.send(f"<@{dono[0]}> **Donate now in <#971698533507948575> or Jei will bonk you**")
        else:
            user = await client.fetch_user(dono[0])
            username = user.name
            await channel.send(f"**{username} Donate now in <#971698533507948575> or Jei will bonk you**")
        database.clear_guild_reminded(dono[0])

async def reminder_loop_task(client, database):
    # loop once a second to check for reminders
    await asyncio.sleep(1)
    await reminder_loop(client, database)
    

# On ready, create log
@client.event
async def on_ready():
    print(f"{client.user.id} {client.user} Connected to Discord!")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="the fishies in the ocean..."))
    set_dungeon_status_on_startup()

def set_dungeon_status_on_startup():
    global dungeon_open
    status = database.get_dungeon_status()
    if status == 1:
        dungeon_open = True
    else:
        dungeon_open = False

@client.event
async def on_message_edit(before, after):
    # Ignore messages from self
    if before.author == client.user:
        return
    
    # Only checks messages from izzi
    if before.author.id != izzi_id:
        return
    
    # Ignore non-embeds
    if before.embeds == []:
        return

    await occmd.parse_event_lobbies(after)
                    

# On message, check if the message mentions a specific user
@client.event
async def on_message(message):
    global dungeon_open
    # ignore self
    if message.author == client.user:
        return

    if message.content.lower().startswith('ocadmin'):
        if message.author.id not in admin_list:
            return
        try:
            if message.content.split(" ", 1)[1].lower().startswith('dungeon'):
                try:
                    if message.content.split(" ", 2)[2].lower().startswith('off'):
                        dungeon_open = False
                        database.set_dungeon_status(0)
                        await message.channel.send('Dungeon is now closed.')
                    elif message.content.split(" ", 2)[2].lower().startswith('on'):
                        dungeon_open = True
                        database.set_dungeon_status(1)
                        await message.channel.send('Dungeon is now open.')
                except:
                    await message.channel.send('Dungeon is currently ' + ('open' if dungeon_open else 'closed') + '.')
            elif message.content.split(" ", 1)[1].lower().startswith('guild'):
                add = re.match(r'ocadmin guild add ([0-9]+)', message.content.lower())
                remove = re.match(r'ocadmin guild remove ([0-9]+)', message.content.lower())
                guild_list = re.match(r'ocadmin guild list', message.content.lower())
                guild_dono = re.match(r'ocadmin guild dono', message.content.lower())
                override = re.match(r'ocadmin guild override ([0-9]+)', message.content.lower())
                if add:
                    userid = int(add.group(1))
                    # get user name
                    user = await client.fetch_user(userid)
                    username = user.name
                    # add user to guild
                    try:
                        database.add_guild_user(userid)
                        await message.channel.send(f'{username} has been added to the guild.')
                    except IntegrityError:
                        await message.channel.send(f'{username} is already in the guild.')
                elif remove:
                    userid = int(remove.group(1))
                    # get user name
                    user = await client.fetch_user(userid)
                    username = user.name
                    # remove user from guild
                    database.remove_guild_user(userid)
                    await message.channel.send(f'{username} has been removed from the guild.')
                elif guild_list:
                    users = database.get_guild_users()
                    counter = 0
                    return_msg = ""
                    # get user names
                    for user in users:
                        counter += 1
                        userid = user[0]
                        user = await client.fetch_user(userid)
                        return_msg += f'{userid} : {user}\n'

                    await message.channel.send(f"List of Guild Members [{counter}]\n```{return_msg}```")
                
                elif guild_dono:
                    table = database.get_guild_dono()
                    
                    return_msg = ""
                    return_counter = 0
                    more_than_7_days = ""
                    more_than_counter = 0
                    # get user names
                    for user,last_dono in table:
                        return_counter += 1
                        userid = user
                        user = await client.fetch_user(user)
                        # convert time to readable format time ago
                        now = datetime.now()
                        last_dono = datetime.fromtimestamp(last_dono)
                        rd = relativedelta(now, last_dono)
                        return_msg += "%s : %d years, %d months, %d days, %d hours, %d minutes and %d seconds\n" % (user, rd.years, rd.months, rd.days, rd.hours, rd.minutes, rd.seconds)
                        if rd.years > 0 or rd.months > 0 or rd.days > 7:
                            more_than_counter += 1
                            more_than_7_days += f'{userid} : {user}\n'

                    await message.channel.send(f"List of users and relative last donation [{return_counter}]\n```{return_msg}```")
                    await message.channel.send(f"List of users who haven't donated in 7 days [{more_than_counter}]\n```{more_than_7_days}```")
                
                elif override:
                    database.set_last_donation(int(override.group(1)), int(datetime.now().timestamp()))
                    user = await client.fetch_user(int(override.group(1)))
                    username = user.name
                    await message.channel.send(f'{username} has been overridden. Datetime set to now.')

                else:
                    await message.channel.send('Invalid command. List of guild commands:\n```guild add/remove <userid>\nguild list\nguild dono\nguild override <userid>\n```')
            else:
                await message.channel.send('Invalid command. Did you mean `ocadmin dungeon` or `ocadmin guild`?')
        except:
            await message.channel.send('Invalid command. Did you mean `ocadmin dungeon` or `ocadmin guild`?')
        return
    
    if message.content.lower().startswith('oc') or message.content.lower().startswith('ooo'):
        if message.channel.id not in channel_blacklist:    
            # update user last seen channel
            database.set_last_channel(message.author.id, message.channel.id)
        else:
            return
        # Help message
        if message.content.split(" ", 1)[1].lower().startswith('help') or message.content.split(" ", 1)[1].startswith('?'):
            await occmd.help(message)
        elif message.content.split(" ", 1)[1].lower().startswith('ping'):
            await occmd.ping(client, message)
        elif message.content.split(" ", 1)[1].lower().startswith('register'):
            await occmd.register(database, message)
        elif re.match(r'^(:?oc|ooo) ?premium (yes|no)$', message.content, re.IGNORECASE): 
            await occmd.premium(database, message)
        elif message.content.split(" ", 1)[1].lower().startswith('rmping'):
            await occmd.rmping(database, message)
        elif message.content.split(" ", 1)[1].lower().startswith('rm'):
            await occmd.rm(database, message, dungeon_open)
        elif message.content.split(" ", 1)[1].lower().startswith('rd clear'):
            await occmd.rd_clear(database, message)
        elif message.content.split(" ", 1)[1].lower().startswith('snipelist'):
            await occmd.snipelist(client, database, message)
        elif message.content.split(" ", 1)[1].lower().startswith('addcard'):
            await occmd.addcard(database, message)
        elif message.content.split(" ", 1)[1].lower().startswith('removecard'):
            await occmd.removecard(database, message)
        elif message.content.split(" ", 1)[1].lower().startswith('deleteaccount'):
            await occmd.delete(database, message)
        elif message.content.split(" ", 1)[1].lower().startswith('fav'):
            await occmd.fav(database, message)
        elif message.content.split(" ", 1)[1].lower().startswith('mobile'):
            await occmd.mobile(database, message)
        else:
            await message.channel.send('Unknown command! Use `oc help` to see a list of commands.')
        return

    # tracking from izzi
    if message.content.lower().startswith('<@784851074472345633>'):
        # guild dono update
        if message.content.split(" ", 1)[1].lower().startswith('guild donate'):
            if message.channel == client.get_channel(971698533507948575):
                if database.check_if_guild_user(message.author.id):
                    await occmd.guild_donate(database, message)
                else:
                    await message.channel.send('You are not in the guild, ask an admin to add you.')

        if message.channel.id not in channel_blacklist:    
            # update user last seen channel
            database.set_last_channel(message.author.id, message.channel.id)
        else:
            return
        # track mana from embed
        if message.content.split(" ", 1)[1].lower().startswith('mana'):
            await occmd.update_mana(client, database, message)
        # update mana from bt
        elif message.content.split(" ", 1)[1].lower().startswith('bt'):
            if "all" in message.content.split(" ", 1)[1].lower():
                await occmd.battle_all(client, database, message)
            else:
                await occmd.battle(client, database, message)
        # update dg mana from bt
        elif message.content.split(" ", 1)[1].lower().startswith('dg'):
            await occmd.dungeon(client, database, message)
        elif message.content.split(" ", 1)[1].lower().startswith('rd bt') or message.content.split(" ", 1)[1].lower().startswith('ev bt'):
            await occmd.raid(client, database, message)
        elif message.content.split(" ", 1)[1].lower().startswith('rd spawn') or message.content.split(" ", 1)[1].lower().startswith('ev spawn'):
            await occmd.raid_spawn(client, database, message)
        elif message.content.split(" ", 1)[1].lower().startswith('lotto') or message.content.split(" ", 1)[1].lower().startswith('lottery'):
            await occmd.lotto(client, database, message)
        elif message.content.split(" ", 1)[1].lower().startswith('hr') or message.content.split(" ", 1)[1].lower().startswith('hourly'):
            await occmd.hr(client, database, message)
        elif message.content.split(" ", 1)[1].lower().startswith('vote') or message.content.split(" ", 1)[1].lower().startswith('daily'):
            await occmd.vote(client, database, message)
        elif message.content.split(" ", 1)[1].lower().startswith('ev lobbies') or message.content.lower().startswith('event lobbies'):
            # wait for izzi to send the embed
            msg = await client.wait_for('message', check=lambda m: m.author.id == izzi_id and m.channel.id == message.channel.id, timeout=10)
            await occmd.parse_event_lobbies(msg)
        elif message.content.split(" ", 1)[1].lower().startswith('rd lobbies') or message.content.lower().startswith('raid lobbies'):
            if not database.is_registered(message.author.id):
                return
            # wait for izzi to send the embed
            msg = await client.wait_for('message', check=lambda m: m.author.id == izzi_id and m.channel.id == message.channel.id, timeout=10)
            await occmd.raid_lobby_wrapper(client, database, msg, message.author.id)
        elif message.content.split(" ", 1)[1].lower().startswith('rd view') or message.content.split(" ", 1)[1].lower().startswith('raid view'):
            if not database.is_registered(message.author.id):
                return
            # wait for izzi to send the embed
            msg = await client.wait_for('message', check=lambda m: m.author.id == izzi_id and m.channel.id == message.channel.id, timeout=10)
            await occmd.raid_view(msg)

if __name__ == '__main__':
    # start reminder loop
    asyncio.ensure_future(reminder_loop(client, database))
    # run client
    client.run(TOKEN)