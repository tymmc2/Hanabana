import sqlite3
import discord
from random import random as rand
from CommandTemplate import CommandTemplate as template
from sqlite3 import Error

class SqlLoader:
    # Load and test the database
    def create_connection(self, db_file):
        """ Creates the connection to the SQLite database """
        self.conn = None
        try:
            self.conn = sqlite3.connect(db_file)
            if db_file == 'ranks.db':
                self.ranks_db_file = db_file
                self.create_new_ranks_db()
            elif db_file == 'commands.db':
                self.cmds_db_file = db_file
                self.create_new_cmds_db()
            else:
                self.db_file = db_file
            print(f'Connected to {db_file}!')
            try:
                c = self.conn.cursor()
            except Error:
                if db_file == 'ranks.db':
                    self.create_new_ranks_db()
                elif db_file == 'commands.db':
                    self.create_new_cmds_db()
                else:
                    print('Invalid database')
        except Error as e:
            print(e)
        finally:
            if self.conn:
                self.conn.close()

    # Ranks Database
    def add_xp_to_user(self, user, guild):
        """ Adds XP to a given user in a certain server """
        self.conn = sqlite3.connect(self.ranks_db_file)
        c = self.conn.cursor()
        try:
            c.execute(f"SELECT xp FROM ranks WHERE user = {user} AND guild = {guild}")
            current_xp_value = c.fetchone()
            new_xp_value = current_xp_value[0] + round(rand() * 20) + 1
            c.execute(f"UPDATE ranks SET xp = {new_xp_value} WHERE user = {user} AND guild = {guild}")
        except TypeError:
            start_xp_value = round(rand() * 20) + 1
            c.execute(f"INSERT INTO ranks VALUES ('{guild}','{user}','{start_xp_value}')")
        self.conn.commit()
        self.conn.close()

    def get_rank(self, user, guild):
        """ Gets the level and xp of a user in a certain server """
        self.conn = sqlite3.connect(self.ranks_db_file)
        c = self.conn.cursor()
        try:
            c.execute(f"SELECT xp FROM ranks WHERE user = {user} AND guild = {guild}")
            current_xp_value = c.fetchone()
            return int(current_xp_value[0])
        except TypeError:
            return 0
        self.conn.commit()
        self.conn.close()

    def create_new_ranks_db(self):
        """ Creates the table in case it does not exist yet """
        c = self.conn.cursor()
        c.execute('''CREATE TABLE ranks
        (guild int, user int, xp int)''')
        self.conn.commit()
        self.conn.close()

    # Commands database
    def get_commands(self, guild):
        """ Gets all of the given commands of a server """
        self.conn = sqlite3.connect(self.cmds_db_file)
        c = self.conn.cursor()
        try:
            c.execute(f"SELECT * FROM commands WHERE guild = {guild}")
            return c.fetchall()
        except TypeError:
            return None

    def run_command(self, guild, user, arg1, name):
        """ Executes the custom command of a server """
        self.conn = sqlite3.connect(self.cmds_db_file)
        c = self.conn.cursor()
        c.execute(f"SELECT * FROM commands WHERE guild = {guild} AND command = '{name}'")
        row = c.fetchone()
        temp = template(user, arg1, row[1], row[2], row[3], row[4], url=row[5], min=row[6], max=row[7])
        return temp.embed

    def create_new_cmds_db(self):
        """ Creates the table in case it does not exist yet """
        c = self.conn.cursor()
        c.execute('''CREATE TABLE commands
        (guild int, command text, type text, info text, description text, url text, min int, max int)''')
        self.conn.commit()
        self.conn.close()

    # Initiate the databases
    def __init__(self):
        self.create_connection(r"ranks.db")
        self.create_connection(r"commands.db")


