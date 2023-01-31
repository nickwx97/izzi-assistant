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

# DB functions for the database

import sqlite3

DB_PATH = '/home/ubuntu/oc/oc.db'

class DB:

    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)

    def insert_user(self, uid, last_channel):
        """
        Inserts a user into the database
        """
        c = self.conn.cursor()
        try:
            c.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?)", (uid, 0, last_channel, 1, 0))
            self.conn.commit()
        except sqlite3.IntegrityError:
            return False
        return True

    def delete_user(self, uid):
        """
        Deletes a user from the database
        """
        c = self.conn.cursor()
        c.execute("DELETE FROM users WHERE id = ?", (uid,))
        self.conn.commit()

    def set_premium(self, uid, premium):
        """
        Sets a user's premium status
        """
        c = self.conn.cursor()
        c.execute("UPDATE users SET premium = ? WHERE id = ?", (premium, uid))
        self.conn.commit()

    def get_premium(self, uid):
        """
        Returns a user's premium status
        """
        c = self.conn.cursor()
        c.execute("SELECT premium FROM users WHERE id = ?", (uid,))
        return c.fetchone()[0]

    def set_mana(self, uid, max_mana, mana_mins):
        """
        Sets a user's mana
        """
        c = self.conn.cursor()
        c.execute("INSERT OR REPLACE INTO mana VALUES (?, ?, ?)", (uid, max_mana, mana_mins))
        self.conn.commit()

    def set_dungeon_mana(self, uid, dungeon_mana_mins):
        """
        Sets a user's dungeon mana
        """
        c = self.conn.cursor()
        c.execute("INSERT OR REPLACE INTO dungeon_mana VALUES (?, ?)", (uid, dungeon_mana_mins))
        self.conn.commit()
    
    def set_last_channel(self, uid, channel_id):
        """
        Sets a user's last channel
        """
        c = self.conn.cursor()
        c.execute("UPDATE users SET last_channel = ? WHERE id = ?", (channel_id, uid))
        self.conn.commit()

    def is_registered(self, uid):
        """
        Checks if a user exists in the database
        """
        c = self.conn.cursor()
        c.execute("SELECT * FROM users WHERE id = ?", (uid,))
        return c.fetchone() is not None

    def get_expired_mana(self, current_time):
        """
        Returns a list of users with expired mana
        """
        c = self.conn.cursor()
        c.execute("SELECT * FROM mana WHERE remind_time < ?", (current_time,))
        return c.fetchall()

    def get_expired_dungeon_mana(self, current_time):
        """
        Returns a list of users with expired dungeon mana
        """
        c = self.conn.cursor()
        c.execute("SELECT * FROM dungeon_mana WHERE remind_time < ?", (current_time,))
        return c.fetchall()

    def clear_mana_reminded(self, uid):
        """
        Delete entry from mana table
        """
        c = self.conn.cursor()
        c.execute("DELETE FROM mana WHERE uid = ?", (uid,))
        self.conn.commit()
    
    def clear_dungeon_mana_reminded(self, uid):
        """
        Delete entry from dungeon mana table
        """
        c = self.conn.cursor()
        c.execute("DELETE FROM dungeon_mana WHERE uid = ?", (uid,))
        self.conn.commit()

    def get_last_channel(self, uid):
        """
        Returns a user's last channel
        """
        c = self.conn.cursor()
        c.execute("SELECT last_channel FROM users WHERE id = ?", (uid,))
        ret = c.fetchone()
        if ret is not None:
            return ret[0]
        else:
            return None

    def get_mobile(self, uid):
        """
        Returns a user's mobile status
        """
        c = self.conn.cursor()
        c.execute("SELECT mobile FROM users WHERE id = ?", (uid,))
        return c.fetchone()[0]

    def set_mobile(self, uid, mobile):
        """
        Sets a user's mobile status
        """
        c = self.conn.cursor()
        c.execute("UPDATE users SET mobile = ? WHERE id = ?", (mobile, uid))
        self.conn.commit()

    def get_max_mana(self, uid):
        """
        Returns a user's max mana
        """
        c = self.conn.cursor()
        c.execute("SELECT max_mana FROM mana WHERE uid = ?", (uid,))
        try:
            return c.fetchone()[0]
        except:
            return None
    
    def get_mana_time(self, uid):
        """
        Returns a user's mana time
        """
        c = self.conn.cursor()
        c.execute("SELECT remind_time FROM mana WHERE uid = ?", (uid,))
        try:
            return c.fetchone()[0]
        except:
            return None

    def get_dungeon_mana_time(self, uid):
        """
        Returns a user's dungeon mana time
        """
        c = self.conn.cursor()
        c.execute("SELECT remind_time FROM dungeon_mana WHERE uid = ?", (uid,))
        try:
            return c.fetchone()[0]
        except:
            return None

    def raid_reminder(self, uid, remind_time):
        """
        Sets a user's raid reminder
        """
        c = self.conn.cursor()
        c.execute("INSERT OR REPLACE INTO raid VALUES (?, ?)", (uid, remind_time))
        self.conn.commit()

    def get_raid_reminder(self, uid):
        """
        Returns a user's raid reminder
        """
        c = self.conn.cursor()
        c.execute("SELECT remind_time FROM raid WHERE uid = ?", (uid,))
        try:
            return c.fetchone()[0]
        except:
            return None

    def get_expired_raid(self, current_time):
        """
        Returns a list of users with expired raid reminders
        """
        c = self.conn.cursor()
        c.execute("SELECT * FROM raid WHERE remind_time < ?", (current_time,))
        return c.fetchall()

    def clear_raid_reminded(self, uid):
        """
        Delete entry from raid reminders table
        """
        c = self.conn.cursor()
        c.execute("DELETE FROM raid WHERE uid = ?", (uid,))
        self.conn.commit()
    
    def set_lotto_reminder(self, uid, remind_time):
        """
        Sets a user's lotto reminder
        """
        c = self.conn.cursor()
        c.execute("INSERT OR REPLACE INTO lotto VALUES (?, ?)", (uid, remind_time))
        self.conn.commit()

    def get_lotto_reminder(self, uid):
        """
        Returns a user's lotto reminder
        """
        c = self.conn.cursor()
        c.execute("SELECT remind_time FROM lotto WHERE uid = ?", (uid,))
        try:
            return c.fetchone()[0]
        except:
            return None

    def get_expired_lotto(self, current_time):
        """
        Returns a list of users with expired lotto reminders
        """
        c = self.conn.cursor()
        c.execute("SELECT * FROM lotto WHERE remind_time < ?", (current_time,))
        return c.fetchall()
    
    def clear_lotto_reminded(self, uid):
        """
        Delete entry from lotto reminders table
        """
        c = self.conn.cursor()
        c.execute("DELETE FROM lotto WHERE uid = ?", (uid,))
        self.conn.commit()

    def set_hr_reminder(self, uid, remind_time):
        """
        Sets a user's hr reminder
        """
        c = self.conn.cursor()
        c.execute("INSERT OR REPLACE INTO hr VALUES (?, ?)", (uid, remind_time))
        self.conn.commit()

    def get_hr_reminder(self, uid):
        """
        Returns a user's hr reminder
        """
        c = self.conn.cursor()
        c.execute("SELECT remind_time FROM hr WHERE uid = ?", (uid,))
        try:
            return c.fetchone()[0]
        except:
            return None

    def get_expired_hr(self, current_time):
        """
        Returns a list of users with expired hr reminders
        """
        c = self.conn.cursor()
        c.execute("SELECT * FROM hr WHERE remind_time < ?", (current_time,))
        return c.fetchall()

    def clear_hr_reminded(self, uid):
        """
        Delete entry from hr reminders table
        """
        c = self.conn.cursor()
        c.execute("DELETE FROM hr WHERE uid = ?", (uid,))
        self.conn.commit()
    
    def set_raid_spawn_reminder(self, uid, remind_time):
        """
        Sets a user's raid reminder
        """
        c = self.conn.cursor()
        c.execute("INSERT OR REPLACE INTO spawn VALUES (?, ?)", (uid, remind_time))
        self.conn.commit()

    def get_raid_spawn_reminder(self, uid):
        """
        Returns a user's raid spawn reminder
        """
        c = self.conn.cursor()
        c.execute("SELECT remind_time FROM spawn WHERE uid = ?", (uid,))
        try:
            return c.fetchone()[0]
        except:
            return None
    
    def get_expired_spawn(self, current_time):
        """
        Returns a list of users with expired spawn reminders
        """
        c = self.conn.cursor()
        c.execute("SELECT * FROM spawn WHERE remind_time < ?", (current_time,))
        return c.fetchall()

    def clear_spawn_reminded(self, uid):
        """
        Delete entry from spawn reminders table
        """
        c = self.conn.cursor()
        c.execute("DELETE FROM spawn WHERE uid = ?", (uid,))
        self.conn.commit()

    def set_vote_reminder(self, uid, remind_time):
        """
        Sets a user's vote reminder
        """
        c = self.conn.cursor()
        c.execute("INSERT OR REPLACE INTO vote VALUES (?, ?)", (uid, remind_time))
        self.conn.commit()

    def get_vote_reminder(self, uid):
        """
        Returns a user's vote reminder
        """
        c = self.conn.cursor()
        c.execute("SELECT remind_time FROM vote WHERE uid = ?", (uid,))
        try:
            return c.fetchone()[0]
        except:
            return None

    def get_expired_vote(self, current_time):
        """
        Returns a list of users with expired vote reminders
        """
        c = self.conn.cursor()
        c.execute("SELECT * FROM vote WHERE remind_time < ?", (current_time,))
        return c.fetchall()

    def clear_vote_reminded(self, uid):
        """
        Delete entry from vote reminders table
        """
        c = self.conn.cursor()
        c.execute("DELETE FROM vote WHERE uid = ?", (uid,))
        self.conn.commit()

    def set_ping_reminder(self, uid, ping):
        """
        Sets a user's ping reminder
        """
        c = self.conn.cursor()
        c.execute("UPDATE users SET ping = ? WHERE id = ?", (ping, uid))

    def get_ping_reminder(self, uid):
        """
        Returns a user's ping reminder
        """
        c = self.conn.cursor()
        c.execute("SELECT ping FROM users WHERE id = ?", (uid,))
        try:
            return c.fetchone()[0]
        except:
            return None

    def add_guild_user(self, uid):
        """
        Adds a user to the guild table
        """
        c = self.conn.cursor()
        c.execute("INSERT INTO guild VALUES (?, ?)", (uid, 0))
        self.conn.commit()

    def remove_guild_user(self, uid):
        """
        Removes a user from the guild table
        """
        c = self.conn.cursor()
        c.execute("DELETE FROM guild WHERE uid = ?", (uid,))
        self.conn.commit()

    def get_guild_users(self):
        """
        Returns a list of users in the guild
        """
        c = self.conn.cursor()
        c.execute("SELECT uid FROM guild")
        return c.fetchall()

    def get_guild_dono(self):
        """
        Returns a list of users in the guild
        """
        c = self.conn.cursor()
        c.execute("SELECT * FROM guild")
        return c.fetchall()

    def set_last_donation(self, uid, time):
        """
        Sets a user's last donation time
        """
        c = self.conn.cursor()
        c.execute("UPDATE guild SET last_donation = ? WHERE uid = ?", (time, uid))
        self.conn.commit()

    def check_if_guild_user(self, uid):
        """
        Checks if a user is in the guild
        """
        c = self.conn.cursor()
        c.execute("SELECT * FROM guild WHERE uid = ?", (uid,))
        return c.fetchone() is not None

    def set_guild_remind(self, uid, remind_time):
        """
        Sets a user's guild reminder
        """
        c = self.conn.cursor()
        c.execute("INSERT OR REPLACE INTO guild_remind VALUES (?, ?)", (uid, remind_time))
        self.conn.commit()
    
    def get_expired_guild_remind(self, current_time):
        """
        Returns a list of users with expired guild reminders
        """
        c = self.conn.cursor()
        c.execute("SELECT * FROM guild_remind WHERE remind_time < ?", (current_time,))
        return c.fetchall()

    def clear_guild_reminded(self, uid):
        """
        Delete entry from guild reminders table
        """
        c = self.conn.cursor()
        c.execute("DELETE FROM guild_remind WHERE uid = ?", (uid,))
        self.conn.commit()

    def set_dungeon_status(self, value):
        """
        Sets global dungeon status
        """
        c = self.conn.cursor()
        c.execute("INSERT OR REPLACE INTO admin VALUES ('dungeon', ?)", (value,))
        self.conn.commit()

    def get_dungeon_status(self):
        """
        Returns global dungeon status
        """
        c = self.conn.cursor()
        c.execute("SELECT value FROM admin WHERE key = 'dungeon'")
        val = c.fetchone()
        return val[0]

    def insert_card(self, uid, card):
        """
        Inserts a card into the user's card table
        """
        c = self.conn.cursor()
        c.execute("INSERT INTO cards VALUES (?, ?)", (uid, card))
        self.conn.commit()
        # return number of rows affected
        return c.rowcount

    def get_cards(self, uid):
        """
        Returns a user's card table
        """
        c = self.conn.cursor()
        c.execute("SELECT card FROM cards WHERE uid = ?", (uid,))
        return c.fetchall()

    def delete_card(self, uid, card):
        """
        Deletes a card from the user's card table
        """
        c = self.conn.cursor()
        c.execute("DELETE FROM cards WHERE uid = ? AND card = ?", (uid, card))
        self.conn.commit()
        # return number of rows deleted
        return c.rowcount

    def delete_all_cards(self, uid):
        """
        Deletes all cards from the user's card table
        """
        c = self.conn.cursor()
        c.execute("DELETE FROM cards WHERE uid = ?", (uid,))
        self.conn.commit()
        # return number of rows deleted
        return c.rowcount

    def insert_fav(self, uid, fav):
        """
        Inserts a channel into the user's favorite table
        """
        c = self.conn.cursor()
        c.execute("INSERT INTO favs VALUES (?, ?)", (uid, fav))
        self.conn.commit()
        # return number of rows affected
        return c.rowcount

    def get_favs(self, uid):
        """
        Returns a user's favorite table
        """
        c = self.conn.cursor()
        c.execute("SELECT fav FROM favs WHERE uid = ?", (uid,))
        return c.fetchall()

    def delete_fav(self, uid, fav):
        """
        Deletes a channel from the user's favorite table
        """
        c = self.conn.cursor()
        c.execute("DELETE FROM favs WHERE uid = ? AND fav = ?", (uid, fav))
        self.conn.commit()
        # return number of rows deleted
        return c.rowcount