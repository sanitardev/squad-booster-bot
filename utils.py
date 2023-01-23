import sqlite3
from aiogram.utils.markdown import hlink


def mention(name, usid):
    return hlink(name, f'tg://user?id={usid}')


def bold(text):
    return f"<b>{text}</b>"


def code(text):
    return f"<code>{text}</code>"


class DB:
    conn = sqlite3.connect('db.db')
    cur = conn.cursor()
    conn.isolation_level = None

    def insert(self, table, column, values, ignore=True):
        request = "INSERT"
        if ignore:
            request = request + " OR IGNORE"
        request = request + " INTO"
        self.cur.execute(f"{request} '{table}'({', '.join(map(str, column))}) VALUES({', '.join(map(str, values))})")

    def add_chat_table(self, message):
        self.cur.execute(f'''CREATE TABLE IF NOT EXISTS "{message.chat.id}" (
            "user_id"   INTEGER NOT NULL UNIQUE,
            "button_id" INTEGER DEFAULT 0,
            "time" INTEGER DEFAULT 0
        );''')

    def delete(self, table, wherecolumn, wherevalue):
        self.cur.execute(f"DELETE FROM {table} WHERE {wherecolumn} = {wherevalue}")

    def select(self, table, column, wherecolumn=None, wherevalue=None):
        requests = f"SELECT {column} FROM '{table}'"
        if wherecolumn is not None:
            requests = requests + f" WHERE {wherecolumn} = {wherevalue}"
        try:
            self.cur.execute(requests)
            if wherecolumn is not None:
                value = self.cur.fetchone()[0]
            else:
                value = self.cur.fetchall()
        except:
            value = None
        return value

    def update(self, table, column, value, where, wherewhat):
        self.cur.execute(f"UPDATE '{table}' SET {column} = '{value}' WHERE {where} = '{wherewhat}'")