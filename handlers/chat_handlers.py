from aiogram import types
from dp import dp, bot
from utils import *
from key import *
from time import time
import asyncio, aioschedule

db = DB()

@dp.message_handler(commands="rules")
async def rules(message: types.Message):
    db.add_chat_table(message)
    db.insert("sett", ["chat_id"], [message.chat.id])
    db.insert(message.chat.id, ["user_id"], [message.from_user.id])
    rules = db.select("sett", "rules", "chat_id", message.chat.id)
    await message.reply(rules)

@dp.message_handler(content_types=['new_chat_members'])
async def send_welcome(message: types.Message):
    me = await bot.get_me()
    for chat_member in message.new_chat_members:
        db.add_chat_table(message)
        db.insert("sett", ["chat_id"], [message.chat.id])
        if chat_member.id == me.id:
            await message.reply("Привет! Чтобы воспользоваться всеми моими функциями назначьте меня администратором.")
        else:
            db.insert(message.chat.id, ["user_id"], [message.from_user.id])
            if message.from_user.is_bot:
                return
            db.add_chat_table(message)
            db.insert(message.chat.id, ["user_id"], [message.from_user.id])
            await bot.restrict_chat_member(message.chat.id, chat_member.id,
                                               can_send_messages=False,
                                               can_send_media_messages=False,
                                               can_send_other_messages=False,
                                               can_add_web_page_previews=False)
            rules = db.select("sett", "rules", "chat_id", message.chat.id)
            but = await message.reply(f"""{rules}""", reply_markup=add_inline("Ознакомлен", "ready"))
            db.update(message.chat.id, "time", time()+900, "user_id", chat_member.id)
            db.update(message.chat.id, "button_id", but.message_id, "user_id", chat_member.id)


@dp.callback_query_handler(text="ready")
async def unmute(call: types.CallbackQuery):
    user = db.select(call.message.chat.id, "user_id", "button_id", call.message.message_id)
    if not call.from_user.id == user:
        return
    db.update(call.message.chat.id, "time", 0, "user_id", call.from_user.id)
    await bot.restrict_chat_member(call.message.chat.id, user,
    can_send_messages=True,
    can_send_media_messages=True,
    can_send_other_messages=True,
    can_add_web_page_previews=True)
    await bot.delete_message(call.message.chat.id, call.message.message_id)

@dp.message_handler(content_types=['any'])
async def add_to_db(message: types.Message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        if message.from_user.is_bot:
            return
        db.add_chat_table(message)
        db.insert("sett", ["chat_id"], [message.chat.id])
        db.insert(message.chat.id, ["user_id"], [message.from_user.id])

async def noon_print():
    conn = sqlite3.connect('db.db')
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
    tables = cur.fetchall()
    tables.remove(('private',))
    tables.remove(('feedback',))
    tables.remove(('sett',))
    for table in tables:
        cur.execute(f"SELECT user_id FROM '{table[0]}' WHERE time != 0")
        users = cur.fetchall()
        for us in users:
            cur.execute(f"SELECT time FROM '{table[0]}' WHERE user_id = {us[0]}")
            us_time = cur.fetchone()[0]
            if int(us_time) - int(time()) <= 0:
                try:
                    await bot.kick_chat_member(chat_id=table[0], user_id=us[0])
                    await bot.unban_chat_member(chat_id=table[0], user_id=us[0])
                except:
                    pass

async def scheduler():
    aioschedule.every().minute.do(noon_print)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

async def on_startup(_):
    asyncio.create_task(scheduler())