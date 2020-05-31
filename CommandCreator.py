import sqlite3
from sqlite3 import Error


def create(file, guild, name, type, info="Empty", description="Empty", url='None', min=0, max=1):
    """ This function creates an empty command structure within the SQL database """
    conn = sqlite3.connect(file)
    c = conn.cursor()
    if already_exists(c, name, guild):
        return 'Already exists'
    try:
        c.execute(f"INSERT INTO commands VALUES ('{guild}','{name}','{type}','{info}','{description}','{url}','{min}','{max}')")
        conn.close()
        return 'Command added successfully.'
    except TypeError:
        conn.close()
        return 'Failed to add command.'

def already_exists(conn, name, guild):
    """ Checks the database to see if the command already exists """
    default_commands = ['reddit', 'level', 'help', 'command']
    for x in default_commands:
        if name == x:
            return True
    conn.execute(f"SELECT command FROM commands WHERE guild = '{guild}'")
    server_commands = conn.fetchall()
    for x in server_commands:
        if x[0] == name:
            return True
    return False

# print(create(r'commands.db', '582704905945612309', 'wow', 'random'))

def edit(file, guild, current_name, new_name=None, type=None, info=None, description=None, url=None, min=0, max=1):
    """ Modifies a given command to have certain functions provided by the user """
    conn = sqlite3.connect(file)
    c = self.conn.cursor()
    name = current_name
    if newName != None:
        c.execute(f"UPDATE commands SET command = '{new_name}' WHERE guild = {guild} AND command = '{currentName}'")
        name = new_name
    if type != None:
        c.execute(f"UPDATE commands SET type = '{type}' WHERE guild = {guild} AND command = '{name}'")
    if info != None:
        c.execute(f"UPDATE commands SET info = '{info}' WHERE guild = {guild} AND command = '{name}'")
    if description != None:
        c.execute(f"UPDATE commands SET description = '{description}' WHERE guild = {guild} AND command = '{name}'")
    if url != None:
        c.execute(f"UPDATE commands SET url = '{url}' WHERE guild = {guild} AND command = '{name}'")
    if min != 0:
        c.execute(f"UPDATE commands SET min = '{min}' WHERE guild = {guild} AND command = '{name}'")
    if max != 1:
        c.execute(f"UPDATE commands SET max = '{max}' WHERE guild = {guild} AND command = '{name}'")
    conn.commit()
    conn.close()
    return "done"

def remove(file, guild, name):
    """ Removes a command from the database """
    conn = sqlite3.connect(file)
    c = conn.cursor()
    try:
        c.execute(f"DELETE FROM commands WHERE command = '{name}'")
        conn.close()
        return 'Success!'
    except Error:
        conn.close()
        return None