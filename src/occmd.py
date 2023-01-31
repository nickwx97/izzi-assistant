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

# functions to reply to bot commands

import discord
import re
import asyncio
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


izzi_id = 784851074472345633
global_event_list = []
global_raid_list = []

ability_emote_mapping = {
    "predator": "<:co_Predator:990284640705191977>",
    "dragonrage": "<:DragonRage:990284621784678490>",
    "dominator1": "<:Dominator:990284620392190012>",
    "spellbook": "<:SpellBook:990284648418537522>",
    "sleep": "<:Sleep:990284647223148544>",
    "stun": "<:Stun:990284649865572402>",
    "presenceofmind": "<:co_PresenceofMind:990284641955098644>",
    "evasion": "<:co_Evade:990284626218078239>",
    "misdirection": "<:Misdirection:990284637307805716>",
    "guardian": "<:Guardian:990284632358535199>",
    "restriction": "<:Restrict:990284644740137031>",
    "eclipse": "<:co_Eclipse:990284623680507969>",
    "heal": "<:Revitalize:990284646136836176>",
    "killerinstincts": "<:KillerInstincts:990284634090782841>",
    "futuresight": "<:FutureSight:990284631138000956>",
    "boneplatting": "<:BonePlatting:990284616483086366>",
    "pointblank": "<:PointBlank:990284638465441843>",
    "frost": "<:Frost:990284629619642460>",
    "shard": "<:Blizzard:990284615367409745>",
    "chronobreak": "<:Chronobreak:990284618412466176>",
    "dreameater": "<:co_DreamEater:990284623013642270>",
    "shatteredsword": "<:Crusher:990284619393945670>",
    "berserk": "<:Berserk:990284614335598622>",
    "balancingstrike": "<:BalancingStrike:990284613064740934>",
    "fightingspirit": "<:FightingSpirit:990284628751446047>",
    "exhaust": "<:co_Exhaust:990284627602178088>",
    "burningmeteor": "<:ElementalStrike:990284625324679199>",
    "timebomb": "<:TimeBomb:990284652096942130>",
    "harbinger": "<:HarbingerofDeath:990284633453232138>",
    "lifesteal": "<:Lifesteal:990284636284420116>",
    "rapidfire": "<:co_Rapidfire:990284643188228126>",
    "wrecker": "<:Wrecker:990284655251030136>",
    "surge": "<:Surge:990284650897367051>",
    "precision": "<:Precision:990284639543394324>",
    "toxic": "<:ToxicScreen:990284654269575248>",
    "tornado": "<:Tornado:990284653116149790>"
}

element_weakness = [
    [2, 8], # water 0
    [0], # fire 1
    [1, 6], # grass 2
    [1, 7], # crystal 3
    [3], # light 4
    [4], # dark 5
    [5, 9], # poison 6
    [6], # wind 7
    [9], # electric 8
    [2, 3],  # ground 9
    [] # neutral 10
]

element_to_eid = {
    ":droplet:": 0,
    ":fire:": 1,
    ":leaves:": 2,
    ":snowflake:": 3,
    ":sunny:": 4,
    ":crescent_moon:": 5,
    ":biohazard:": 6,
    ":cloud_tornado:": 7,
    ":zap:": 8,
    ":mountain:": 9,
    ":sparkles:": 10
}

eid_to_element = {
    0: ":droplet:",
    1: ":fire:",
    2: ":leaves:",
    3: ":snowflake:",
    4: ":sunny:",
    5: ":crescent_moon:",
    6: ":biohazard:",
    7: ":cloud_tornado:",
    8: ":zap:",
    9: ":mountain:",
    10: ":sparkles:"
}

def check_premium(database, id):
    if database.get_premium(id) == 0:
        return False
    else:
        return True

def get_sec(time_str):
    """Get seconds from time."""
    h, m, s = time_str.split(' : ')
    return int(h) * 3600 + int(m) * 60 + int(s)

async def help(message):
    # send an embed with a list of commands
    embed = discord.Embed(title="Ocean Commands", description="List of commands for the Celestial Ocean server", color=0x00ff00)
    embed.add_field(name="oc help", value="Shows this message", inline=False)
    embed.add_field(name="oc ping", value="Pong!", inline=False)

    # izzi related commands
    embed.add_field(name="oc register", value="Register for tracking", inline=False)
    embed.add_field(name="oc premium [yes|no]", value="Configure donator status", inline=False)
    embed.add_field(name="oc mobile [on|off]", value="Configure raid ping type", inline=False)
    embed.add_field(name="oc rd clear", value="Clear your raid battle reminder", inline=False)
    embed.add_field(name="oc rm", value="Reminder list", inline=False)
    embed.add_field(name="oc rmping", value="Show reminder ping status", inline=False)
    embed.add_field(name="oc rmping [on|off]", value="Enable/Disable reminder ping status", inline=False)
    embed.add_field(name="oc snipelist [ID/mention]", value="View your raid snipe list, or provide option for another's snipelist", inline=False)
    embed.add_field(name="oc snipelist reset", value="Reset your raid snipelist", inline=False)
    embed.add_field(name="oc addcard", value="Adds a card to your snipelist", inline=False)
    embed.add_field(name="oc removecard", value="Removes a card from your snipelist", inline=False)
    embed.add_field(name="oc fav", value="Shows your favorite list", inline=False)
    embed.add_field(name="oc fav <add/remove> <channel ID/mention>", value="Adds/Removes a channel from your favorites", inline=False)
    embed.add_field(name="oc deleteaccount", value="Deletes your Ocean Helper account", inline=False)
    # Add footer
    embed.set_footer(text="This bot was originally created by @Tiensi#0001. Contact through DMs for enquiry.")
    # Send the embed to the channel
    await message.channel.send(embed=embed)

async def addcard(database, message):
    if not database.is_registered(message.author.id):
        return
    
    cards_message = re.split("oc addcard ", message.content, flags=re.IGNORECASE)[1]
    cards = cards_message.split(",")
    count = 0
    for card in cards:
        ret = database.insert_card(message.author.id, card)
        if ret is not None:
            count += ret
    await message.channel.send(f"Added {count} card(s) to your snipelist.")

async def removecard(database, message):
    if not database.is_registered(message.author.id):
        return
    
    cards_message = re.split("oc removecard ", message.content, flags=re.IGNORECASE)[1]
    cards = cards_message.split(",")
    count = 0
    for card in cards:
        ret = database.delete_card(message.author.id, card)
        if ret is not None:
            count += ret
    await message.channel.send(f"Removed {count} card(s) from your snipelist.")

async def ping(client, message):
    latency = round(client.latency * 1000)
    # send embed with latency
    embed = discord.Embed(title="Ocean Ping", description="Pong!", color=0x00ff00)
    embed.add_field(name="Latency 🏓", value=f"{latency} ms", inline=False)
    # Send the embed to the channel
    await message.channel.send(embed=embed)

async def register(database, message):
    if not database.insert_user(message.author.id, message.channel.id):
        await message.channel.send('You are already registered!')
    else:
        # send embed with registration message
        embed = discord.Embed(title="Ocean Registration", color=0x00ff00)
        embed.add_field(name="Registration 📝", value="You have been registered for tracking! Remember to set premium status if you are!", inline=False)
        # add footer
        embed.set_footer(text="You are strongly encouraged to run *iz mana* to start mana tracking!")
        # Send the embed to the channel
        await message.channel.send(embed=embed)

async def premium(database, message):

    if not database.is_registered(message.author.id):
        await message.channel.send('You are not registered for tracking!')
        return

    if "yes" in message.content:
        database.set_premium(message.author.id, 1)
        await message.channel.send('You are now a premium donator!')
    elif "no" in message.content:
        database.set_premium(message.author.id, 0)
        await message.channel.send('You are no longer a premium donator!')

async def snipelist(client, database, message):
    global meta_list
    if not database.is_registered(message.author.id):
        return
    
    # default id is the user's id
    id = message.author.id

    # get arguments if any, replace id with argument
    args = message.content.split(" ")
    if len(args) > 2:
        if args[2] == "reset":
            num_rows = database.delete_all_cards(id)
            await message.channel.send(f"Your snipelist has been reset! {num_rows} card(s) was/were removed.")
            return
        id = re.sub(r"[<@>]", "", args[2])
        if re.match("\d+", id):
            id = int(id)

    # get name from id using discord api
    name = await client.fetch_user(id)
    name = name.name.rsplit(',', 1)[0]

    # get user meta list from database
    meta_list = database.get_cards(id)
    if len(meta_list) == 0:
        await message.channel.send('You have no cards in your raid snipe list!')
        return
    
    # unpack meta list
    card_list = []
    for meta in meta_list:
        card_list.append(meta[0])
    meta_list = card_list

    # send snipe list in normal message
    embed = discord.Embed(title=f"{name}'s Snipe List", color=0x00ff00)
    embed.add_field(name="Snipe List 📝", value=f"{', '.join(sorted(meta_list))}", inline=False)
    # add footer
    embed.add_field(name="Donations are appreciated to @Tiensi#0001 😋.", value="Edit your cards with oc addcard / removecard", inline=False)
    # Send the embed to the channel
    await message.channel.send(embed=embed)

async def delete(database, message):
    if not database.is_registered(message.author.id):
        return
    database.delete_user(message.author.id)
    await message.channel.send('Your account has been unregistered <:co_tearyeye:1001421420779286558>')

async def fav(database, message):
    if not database.is_registered(message.author.id):
        return
    if "add" in message.content:
        channel_id = re.split("oc fav add ", message.content, flags=re.IGNORECASE)[1]
        if re.match("<#\d+>", channel_id):
            channel_id = int(re.sub(r"[<#>]", "", channel_id))
        elif re.match("\d+", channel_id):
            channel_id = int(channel_id)
        else:
            await message.channel.send("Invalid channel id format!")
            return
        database.insert_fav(message.author.id, channel_id)
        await message.channel.send(f"Added <#{channel_id}> to your favorite list!")
    elif "remove" in message.content:
        channel_id = re.split("oc fav remove ", message.content, flags=re.IGNORECASE)[1]
        if re.match("<#\d+>", channel_id):
            channel_id = int(re.sub(r"[<#>]", "", channel_id))
        elif re.match("\d+", channel_id):
            channel_id = int(channel_id)
        else:
            await message.channel.send("Invalid channel id format!")
            return
        database.delete_fav(message.author.id, channel_id)
        await message.channel.send(f"Removed <#{channel_id}> from your favorite list!")
    else:
        fav_list = database.get_favs(message.author.id)
        if len(fav_list) == 0:
            await message.channel.send('You have no favorite channels!')
            return
        fav_list = [f"> <#{fav[0]}>\n" for fav in fav_list]
        await message.channel.send(f"> **{message.author.name}'s favorite list:**\n{''.join(fav_list)}")

async def mobile(database, message):
    if not database.is_registered(message.author.id):
        return
    if "on" in message.content:
        database.set_mobile(message.author.id, 1)
        await message.channel.send('Mobile raid ping is now __enabled__! (unquoted)')
    elif "off" in message.content:
        database.set_mobile(message.author.id, 0)
        await message.channel.send('Mobile raid ping is now __disabled__! (quoted)')
    else:
        mobile = database.get_mobile(message.author.id)
        if mobile == 1:
            await message.channel.send('Mobile raid ping is __enabled__! (unquoted)')
        else:
            await message.channel.send('Mobile raid ping is __disabled__! (quoted)')

async def update_mana(client, database, message):

    if not database.is_registered(message.author.id):
        return

    # wait for izzi to reply with the mana
    msg = await client.wait_for('message', check=lambda m: m.author.id == izzi_id and m.channel.id == message.channel.id, timeout=10)
    mana_text, dungeon_mana_text = msg.embeds[0].to_dict()["description"].split("\n")
    mana_regex = re.match(r'.*? __(.*?)__.*?__ .*', mana_text, re.DOTALL)
    dungeon_mana_regex = re.match(r'.*? __(.*?)__.*?__ .*', dungeon_mana_text, re.DOTALL)

    max_mana = int(mana_regex.group(1).split("/")[1])
    current_mana = int(mana_regex.group(1).split("/")[0])
    dungeon_mana = int(dungeon_mana_regex.group(1).split("/")[0])
    
    mana_mins = (max_mana - current_mana) * 2
    dungeon_mana_mins = (100 - dungeon_mana) / 5 * 4
    database.set_mana(message.author.id, max_mana, mana_mins*60 + int(datetime.now().timestamp()))
    database.set_dungeon_mana(message.author.id, dungeon_mana_mins*60 + int(datetime.now().timestamp()))
    await msg.add_reaction('<:co_okbear:986644165146345472>')

async def battle(client, database, message):

    if not database.is_registered(message.author.id):
        return

    # wait for izzi to reply with the mana
    msg = await client.wait_for('message', check=lambda m: m.author.id == izzi_id and m.channel.id == message.channel.id, timeout=10)
    title = msg.embeds[0].to_dict()["title"].split(" ")[0]
    if title == "Error":
        await msg.add_reaction('<a:co_pikasus:990206893005881345>')
        return
    else:
        # set new time
        new_time = database.get_mana_time(message.author.id) + 60*5*2
        max_mana = database.get_max_mana(message.author.id)
        if max_mana is None:
            await msg.channel.send("I don't know your max mana yet, unable to set new time for reminder <:co_confused:995485865725927437>")
        else:
            database.set_mana(message.author.id, max_mana, new_time)
            await msg.add_reaction('<:co_okbear:986644165146345472>')

async def battle_all(client, database, message):

    if not database.is_registered(message.author.id):
        return

    # wait for izzi to reply with the mana
    msg = await client.wait_for('message', check=lambda m: m.author.id == izzi_id and m.channel.id == message.channel.id, timeout=10)
    title = msg.embeds[0].to_dict()["title"].split(" ")[0]
    if title == "Error":
        await msg.add_reaction('<a:co_pikasus:990206893005881345>')
        return
    else:
        # reduce mana by mod 5, set new time
        max_mana = database.get_max_mana(message.author.id)
        if max_mana is None:
            await msg.channel.send("I don't know your max mana yet, unable to set new time for reminder <:co_confused:995485865725927437>")
        else:
            new_time = max_mana * 2 * 60 + int(datetime.now().timestamp())
            database.set_mana(message.author.id, max_mana, new_time)
            await msg.add_reaction('<:co_okbear:986644165146345472>')

async def dungeon(client, database, message):
    
    if not database.is_registered(message.author.id):
        return

    # wait for izzi to reply with the mana
    msg = await client.wait_for('message', check=lambda m: m.author.id == izzi_id and m.channel.id == message.channel.id, timeout=10)
    if len(msg.embeds) == 0:
        await msg.add_reaction('<:co_fine:986642059282772009>')
        return
    title = msg.embeds[0].to_dict()["title"].split(" ")[0]
    if title == "Error":
        await msg.add_reaction('<a:co_pikasus:990206893005881345>')
        return
    else:
        # set new time
        try:
            new_time = database.get_dungeon_mana_time(message.author.id) + 4 * 60
        except:
            new_time = int(datetime.now().timestamp()) + 4 * 60
        database.set_dungeon_mana(message.author.id, new_time)
        await msg.add_reaction('<:co_okbear:986644165146345472>')

async def raid(client, database, message):

    if not database.is_registered(message.author.id):
        return

    # wait for izzi to reply with the mana
    msg = await client.wait_for('message', check=lambda m: m.author.id == izzi_id and m.channel.id == message.channel.id, timeout=10)
    # no raid energy
    if len(msg.embeds) == 0:
        await msg.add_reaction('<:co_fine:986642059282772009>')        
        return
    title = msg.embeds[0].to_dict()["title"]
    # raid ended
    if "Error" in title:
        await msg.add_reaction('<:co_crycry:986641739878105188>')
    # raid bt success
    else:
        database.raid_reminder(message.author.id, 8*60 + int(datetime.now().timestamp()))
        await msg.add_reaction('<:co_okbear:986644165146345472>')

async def lotto(client, database, message):

    if not database.is_registered(message.author.id):
        return

    # wait for izzi to reply with the mana
    msg = await client.wait_for('message', check=lambda m: m.author.id == izzi_id and m.channel.id == message.channel.id, timeout=10)
    # no lotto energy
    if "cooldown"  in msg.content:
        await msg.add_reaction('<:co_fine:986642059282772009>')
        match = re.match(r'.*in (\d+ : \d+ : \d+)', msg.content)
        time_str = match.group(1)
        database.set_lotto_reminder(message.author.id, int(datetime.now().timestamp()) + get_sec(time_str))
        return
    else:
        await msg.add_reaction('<:co_okbear:986644165146345472>')
        database.set_lotto_reminder(message.author.id, int(datetime.now().timestamp()) + 15*60)

async def hr(client, database, message):

    if not database.is_registered(message.author.id):
        return

    # wait for izzi to reply with the mana
    msg = await client.wait_for('message', check=lambda m: m.author.id == izzi_id and m.channel.id == message.channel.id, timeout=10)
    # no hr energy
    if "cooldown"  in msg.content:
        await msg.add_reaction('<:co_fine:986642059282772009>')
        match = re.match(r'.*in (\d+ : \d+ : \d+)', msg.content)
        time_str = match.group(1)
        database.set_hr_reminder(message.author.id, int(datetime.now().timestamp()) + get_sec(time_str))
        return
    else:
        await msg.add_reaction('<:co_okbear:986644165146345472>')
        database.set_hr_reminder(message.author.id, int(datetime.now().timestamp()) + 60*60)

async def raid_spawn(client, database, message):

    if not database.is_registered(message.author.id):
        return

    try:
        msg = await client.wait_for('message', check=lambda m: m.author.id == izzi_id and m.channel.id == message.channel.id, timeout=1)
        if "cooldown" in msg.content:
            await msg.add_reaction('<:co_fine:986642059282772009>')
            match = re.match(r'.*in (\d+ : \d+ : \d+)', msg.content)
            time_str = match.group(1)
            database.set_raid_spawn_reminder(message.author.id, int(datetime.now().timestamp()) + get_sec(time_str))
            return
    except Exception as e:
        print(e)
        await message.add_reaction('<:co_okbear:986644165146345472>')
        if check_premium(database, message.author.id):
            database.set_raid_spawn_reminder(message.author.id, int(datetime.now().timestamp()) + 2.5*60*60)
        else:
            database.set_raid_spawn_reminder(message.author.id, int(datetime.now().timestamp()) + 3*60*60)

async def vote(client, database, message):

    if not database.is_registered(message.author.id):
        return

    # wait for izzi to reply with the vote
    msg = await client.wait_for('message', check=lambda m: m.author.id == izzi_id and m.channel.id == message.channel.id, timeout=10)
    # Add reaction to message
    await msg.add_reaction('<:co_shy:986643994194878556>')
    # Wait for user to react
    try:
        await client.wait_for('reaction_add', check=lambda r, u: u.id == message.author.id and r.message.id == msg.id, timeout=60)
    except Exception as e:
        # No reaction from user, reply with error
        await msg.channel.send('Timeout, vote not registered')
    else:
        database.set_vote_reminder(message.author.id, int(datetime.now().timestamp()) + 12*60*60)
        # reply with success message
        await msg.channel.send('Vote registered! See you in 12 hours!')
        
async def rm(database, message, dungeon_open):
    if not database.is_registered(message.author.id):
        return

    # current time
    current_time = int(datetime.now().timestamp())

    # show reminder summary in embed
    embed = discord.Embed(title=f"{message.author.name} Reminder Summary", color=0x00ff00)
    embed.set_thumbnail(url="https://images-ext-1.discordapp.net/external/uEaCTwMrL5RxN7jpwv5F64oZdyL2WkQBX0svnm6dwNo/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/989772334879604786/dfdd2166e021399b8b0ac574ba43f41b.png?width=192&height=192")

    lotto_hr_msg = ""

    if lotto := database.get_lotto_reminder(message.author.id):
        if lotto - current_time > 0:
            lotto_hr_msg = f"💰 lottery **{timedelta(seconds=( lotto - current_time))}**\n"
        else:
            lotto_hr_msg = "💰 lottery **Ready**\n"
    else:
        lotto_hr_msg = "💰 lottery **Ready**\n"

    if hr := database.get_hr_reminder(message.author.id):
        if hr - current_time > 0:
            lotto_hr_msg += f"⏰ hourly **{timedelta(seconds=( hr - current_time))}**\n"
        else:
            lotto_hr_msg += "⏰ hourly **Ready**\n"
    else:
        lotto_hr_msg += "⏰ hourly **Ready**\n"

    embed.add_field(name="\u200b", value=lotto_hr_msg, inline=False)

    raid_msg = ""

    if raid := database.get_raid_reminder(message.author.id):
        if raid - current_time > 0:
            raid_msg = f"⚔ raid bt **{timedelta(seconds=( raid - current_time))}**\n"
        else:
            raid_msg = "⚔ raid bt **Ready**\n"
    else:
        raid_msg = "⚔ raid bt **Ready**\n"
    
    if raid_spawn := database.get_raid_spawn_reminder(message.author.id):
        if raid_spawn - current_time > 0:
            raid_msg += f"🎲 raid spawn **{timedelta(seconds=( raid_spawn - current_time))}**\n"
        else:
            raid_msg += "🎲 raid spawn **Ready**\n"
    else:
        raid_msg += "🎲 raid spawn **Ready**\n"

    embed.add_field(name="\u200B", value=raid_msg, inline=False)

    mana_msg = ""

    if mana := database.get_mana_time(message.author.id):
        if mana - current_time > 0:
            mana_msg = f"💧 mana **{timedelta(seconds=( mana - current_time))}**\n"
        else:
            mana_msg = "💧 mana **Full**\n"
    else:
        mana_msg = "💧 mana **Full**\n"

    if dungeon_open:
        if dungeon := database.get_dungeon_mana_time(message.author.id):
            if dungeon - current_time > 0:
                mana_msg += f"🗝 dungeon mana **{timedelta(seconds=( dungeon - current_time))}**\n"
            else:
                mana_msg += "🗝 dungeon mana **Full**\n"
        else:
            mana_msg += "🗝 dungeon mana **Full**\n"

    embed.add_field(name="\u200B", value=mana_msg, inline=False)

    vote_msg = ""

    if vote := database.get_vote_reminder(message.author.id):
        if vote - current_time > 0:
            vote_msg = f"🗳 vote **{timedelta(seconds=( vote - current_time))}**\n"
        else:
            vote_msg = "🗳 vote **Ready**\n"
    else:
        vote_msg = "🗳 vote **Ready**\n"

    embed.add_field(name="\u200B", value=vote_msg, inline=False)

    mobile = database.get_mobile(message.author.id)
    pings_msg = ""
    if mobile == 1:
        pings_msg = "📱 mobile **ON**\n"
    else:
        pings_msg = "📱 mobile **OFF**\n"
    ping = database.get_ping_reminder(message.author.id)
    if ping == 1:
        pings_msg += "📡 ping **ON**\n"
    else:
        pings_msg += "📡 ping **OFF**\n"
    embed.add_field(name="\u200B", value=pings_msg, inline=False)

    # send embed
    await message.channel.send(embed=embed)

async def rd_clear(database, message):

    if not database.is_registered(message.author.id):
        return

    database.clear_raid_reminded(message.author.id)
    await message.add_reaction('<:co_okbear:986644165146345472>')

async def rmping(database, message):

    if not database.is_registered(message.author.id):
        return

    match = re.match(r'oc rmping (on|off)', message.content)
    if not match:
        # show ping reminder status
        await message.channel.send(f"Ping reminder is {'on' if database.get_ping_reminder(message.author.id) == 1 else 'off'}")
    else:
        # set ping reminder status
        database.set_ping_reminder(message.author.id, 1 if match.group(1) == 'on' else 0)
        await message.channel.send(f"Ping reminder is now {match.group(1)}")

async def guild_donate(database, message):
    
        # get donation amount
        match = re.match(r'<@784851074472345633> guild donate (\d+)', message.content.lower())
        if not match:
            await message.channel.send('Invalid amount')
            return
    
        # get donation amount
        required_amount = 200000
        amount = int(match.group(1))
        if amount < required_amount:
            await message.channel.send(f'Amount below {required_amount}, last donation time not updated.')
            return
        else:
            database.set_last_donation(message.author.id, int(datetime.now().timestamp()))
            database.set_guild_remind(message.author.id, int(datetime.now().timestamp()) + 7*24*60*60)
            await message.channel.send('Donation successful! You will be reminded in 7 days.')

async def parse_event_lobbies(message):
    global global_event_list
    if message.embeds[0].title.startswith("Event"):
        # check contents of embed
        for field in message.embeds[0].fields:
            value = field.value
            match = re.match(r".*? (\d+) <:shard:\d+>.*?: (\d+) \*\*\[(\d).*", value)
            if match:
                # get values from regex
                shard = int(match.group(1))
                event_id = match.group(2)
                filled = int(match.group(3))
                # check if event is not full
                if filled < 6:
                    # check if shard > 36
                    if shard >= 36:
                        # check if event is in global list
                        if f"{message.channel.id}-{event_id}" not in global_event_list:
                            # add event to global list
                            global_event_list.append(f"{message.channel.id}-{event_id}")
                            # send message to event channel
                            asyncio.ensure_future(send_event_snipe(message, event_id, shard, filled))

async def send_event_snipe(message, event_id, shard, filled):
    global global_event_list
    my_message = await message.channel.send(f"`iz ev join {event_id}` | **{shard} shards** [{filled}/6]")
    # delete reply in 15 seconds
    await asyncio.sleep(15)
    await my_message.delete()
    global_event_list.remove(f"{message.channel.id}-{event_id}")

async def raid_lobby_wrapper(client, database, message, user):
    await parse_raid_lobbies(database, message, user)
    try:
        while True:
            old, new = await client.wait_for('message_edit', check=lambda o, n: n.author.id == izzi_id and n.id == message.id and n.channel == message.channel, timeout=30)
            await parse_raid_lobbies(database, new, user)
    except:
        await message.reply("Stopped snipe due to timeout.", delete_after=5)

async def parse_raid_lobbies(database, message, user):
    global global_raid_list

    # get user meta list from database
    meta_list = database.get_cards(user)

    # get user mobile
    mobile = database.get_mobile(user)
    
    # unpack meta list
    card_list = []
    for meta in meta_list:
        card_list.append(meta[0])
    meta_list = card_list
    
    if message.embeds[0].title.startswith("Raid Lobbies"):
        # check contents of embed
        for field in message.embeds[0].fields:
            value = field.value
            name = field.name
            value_match = re.match(r"^.*?ID: (\d+) \*\*\[(\d).*$", value)
            name_match = re.match(r"^#\d+ \| ([\w ]+).*?<:([\w\d]+):\d+>.*?, ([\w ]+).*?<:([\w\d]+):\d+>.*?, ([\w ]+).*?<:([\w\d]+):\d+>.*?\[((?:Immortal|Hard|Medium|Easy).*?)\]$", name)
            if value_match and name_match:
                # get values from regex
                raid_id = value_match.group(1)
                filled = int(value_match.group(2))
                # get names from regex
                name1 = name_match.group(1)[:-1]
                name2 = name_match.group(3)[:-1]
                name3 = name_match.group(5)[:-1]

                ability1 = ability_emote_mapping[name_match.group(2)]
                ability2 = ability_emote_mapping[name_match.group(4)]
                ability3 = ability_emote_mapping[name_match.group(6)]

                difficulty = name_match.group(7)
                # check if raid is not full
                if filled < 6:
                    # check if names appear in meta list
                    if name1 in meta_list or name2 in meta_list or name3 in meta_list:
                        # check if raid is in global list
                        if f"{message.channel.id}-{raid_id}" not in global_raid_list:
                            # add raid to global list
                            global_raid_list.append(f"{message.channel.id}-{raid_id}")
                            # see which card is in the meta list
                            display_name = ""
                            if name1 in meta_list:
                                display_name += name1 + " "
                            if name2 in meta_list:
                                display_name += name2 + " "
                            if name3 in meta_list:
                                display_name += name3 + " "
                            # send message to raid channel
                            asyncio.ensure_future(send_raid_snipe(mobile, message, raid_id, filled, display_name, difficulty, f"{ability1} {ability2} {ability3}"))


async def send_raid_snipe(mobile, message, raid_id, filled, display_name, difficulty, abilities):
    global global_raid_list
    if mobile == 0:
        my_message = await message.channel.send(f"`<@784851074472345633> raid join {raid_id}` | **{display_name}{filled}/6 [ {difficulty} ]** | {abilities}")
    else:
        my_message = await message.channel.send(f"<@784851074472345633> raid join {raid_id} | **{display_name}{filled}/6 [ {difficulty} ]** | {abilities}")
    # delete reply in 15 seconds
    await asyncio.sleep(15)
    await my_message.delete()
    global_raid_list.remove(f"{message.channel.id}-{raid_id}")

async def monday_guild_bonk(channel, database):
    table = database.get_guild_dono()
    more_than_7_days = ""
    # get user names
    for user,last_dono in table:
        userid = user
        # convert time to readable format time ago
        now = datetime.now()
        last_dono = datetime.fromtimestamp(last_dono)
        rd = relativedelta(now, last_dono)

        if rd.years > 0 or rd.months > 0 or rd.days > 7:
            more_than_7_days += f'<@{userid}> <:co_knife:986642571650543646>\n'

    if more_than_7_days != "":
        await channel.send(f"List of users who haven't donated in 7 days:\n{more_than_7_days}\n**Note:** The bot records donation on a weekly basis. Therefore, if you donate several weeks at once, it only records the first week. You can ignore this message and take note of yourself for the next due donation.")
    else:
        await channel.send(f"Everyone donated in the last 7 days 🎉\n\n**Note:** The bot records donation on a weekly basis. Therefore, if you donate several weeks at once, it only records the first week. You can ignore this message and take note of yourself for the next due donation.")

async def raid_view(message):
    match = ""
    for line in message.embeds[0].description.split("\n"):
        match = re.match(r"^\*\*Element Type:\*\* (.*)$", line)
        if match:
            match
            break
    match2 = re.match(r"(:\w+:)(:\w+:)(:\w+:)", match.group(1))
    if match2:
        element1 = element_to_eid[match2.group(1)]
        element2 = element_to_eid[match2.group(2)]
        element3 = element_to_eid[match2.group(3)]

        # get weaknesses
        weaknesses = []
        for element in [element1, element2, element3]:
            for weakness in element_weakness[element]:
                    weaknesses.append(weakness)
        
        # get weaknesses of weaknesses, add to list
        meta_weaknesses = []
        for weakness in list(set(weaknesses)):
            for weakness_meta in element_weakness[weakness]:
                if weakness_meta in [element1, element2, element3]:
                    meta_weaknesses.append(weakness)

        # remove meta weaknesses from weaknesses
        for meta_weakness in meta_weaknesses:
            weaknesses.remove(meta_weakness)

        # remove duplicates
        weaknesses = list(set(weaknesses))
        
        # get emote for each element in weaknesses
        weaknesses_emote = []
        for weakness in weaknesses:
            weaknesses_emote.append(eid_to_element[weakness])

        avoid_element = []
        # get elements that are weak to raid element
        for i in range(len(element_weakness)):
            for element in element_weakness[i]:
                if element in [element1, element2, element3]:
                    avoid_element.append(i)

        # remove duplicates
        avoid_element = list(set(avoid_element))

        # remove elements that are in weaknesses
        for element in avoid_element:
            if element in weaknesses:
                avoid_element.remove(element)
        
        # get emote for each element in avoid_element
        avoid_element_emote = []
        for element in avoid_element:
            avoid_element_emote.append(eid_to_element[element])
        
        # reply with weaknesses
        await message.channel.send(f"**Raid Elemental Weaknesses: (SPOILER)** ||{''.join(weaknesses_emote)}||\n**Avoid Elements: (SPOILER)** ||{''.join(avoid_element_emote)}||")