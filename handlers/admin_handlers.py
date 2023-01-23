from dp import dp, bot
from aiogram import types
from utils import *
from pytimeparse import parse
from time import time
from datetime import datetime, timedelta
import pytz
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

db = DB()


class dialog(StatesGroup):
    ruls = State()


@dp.message_handler(is_bot_restrict=True, member_can_restrict=True, commands=["ban"], commands_prefix="!/")
async def ban(message: types.Message):
    db.add_chat_table(message)
    db.insert("sett", ["chat_id"], [message.chat.id])
    db.insert(message.chat.id, ["user_id"], [message.from_user.id])

    allow = db.select("sett", "ban_allow", "chat_id", message.chat.id)
    if allow == 0:
        return

    if not message.reply_to_message:
        await message.reply("Это не ответ на сообщение!")
        return

    user = await message.bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id)
    if user.is_chat_admin():
        await message.reply("Я не могу заблокировать администратора!")
        return

    args = message.get_args()
    parsetime = parse(args)
    if parsetime is not None:
        mute_time = time()+parsetime
        current_date = datetime.now(pytz.timezone('Europe/Moscow')) + timedelta(seconds=parsetime)
        mute_date = current_date.strftime("%d.%m.%Y, %H:%M")
    else:
        mute_time = None

    await message.bot.delete_message(message.chat.id, message.message_id)
    await message.bot.kick_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id, until_date=mute_time)

    if parsetime is None or parsetime <= 59 or parsetime >= 30672000:
        await message.reply_to_message.reply(f"Пользователь {mention(user.user.first_name, user.user.id)} успешно заблокирован навсегда!")
    else:
        await message.reply_to_message.reply(f"Пользователь {mention(user.user.first_name, user.user.id)} успешно заблокирован до {mute_date}.")


@dp.message_handler(is_bot_restrict=True, member_can_restrict=True, commands=["unban"], commands_prefix="!/")
async def unban(message: types.Message):
    db.add_chat_table(message)
    db.insert("sett", ["chat_id"], [message.chat.id])
    db.insert(message.chat.id, ["user_id"], [message.from_user.id])

    allow = db.select("sett", "ban_allow", "chat_id", message.chat.id)
    if allow == 0:
        return

    if not message.reply_to_message:
        await message.reply("Это не ответ на сообщение!")
        return

    user = await message.bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id)
    if user.is_chat_admin():
        await message.reply("Я не могу заблокировать администратора!")
        return

    await message.bot.delete_message(message.chat.id, message.message_id)
    await message.bot.unban_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id)

    await message.reply_to_message.reply(f"Пользователь {mention(user.user.first_name, user.user.id)} успешно разблокирован!")


@dp.message_handler(is_bot_restrict=True, member_can_restrict=True, commands=["mute"], commands_prefix="!/")
async def mute(message: types.Message):
    db.add_chat_table(message)
    db.insert("sett", ["chat_id"], [message.chat.id])
    db.insert(message.chat.id, ["user_id"], [message.from_user.id])

    allow = db.select("sett", "mut_allow", "chat_id", message.chat.id)
    if allow == 0:
        return

    if not message.reply_to_message:
        await message.reply("Это не ответ на сообщение!")
        return

    user = await message.bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id)
    if user.is_chat_admin():
        await message.reply("Я не могу заглушить администратора!")
        return
    args = message.get_args()
    parsetime = parse(args)
    if parsetime is not None:
        mute_time = time()+parsetime
        current_date = datetime.now(pytz.timezone('Europe/Moscow')) + timedelta(seconds=parsetime)
        mute_date = current_date.strftime("%d.%m.%Y, %H:%M")
    else:
        mute_time = None
    await message.bot.delete_message(message.chat.id, message.message_id)
    await bot.restrict_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id, can_send_messages=False, until_date=mute_time)
    if parsetime is None or parsetime <= 59 or parsetime >= 30672000:
        await message.reply_to_message.reply(f"Пользователь {mention(user.user.first_name, user.user.id)} успешно заглушен навсегда!")
    else:
        await message.reply_to_message.reply(f"Пользователь {mention(user.user.first_name, user.user.id)} успешно заглушен до {mute_date}.")

@dp.message_handler(is_bot_restrict=True, member_can_restrict=True, commands=["unmute"], commands_prefix="!/")
async def unmute(message: types.Message):
    db.add_chat_table(message)
    db.insert("sett", ["chat_id"], [message.chat.id])
    db.insert(message.chat.id, ["user_id"], [message.from_user.id])

    allow = db.select("sett", "mut_allow", "chat_id", message.chat.id)
    if allow == 0:
        return

    if not message.reply_to_message:
        await message.reply("Это не ответ на сообщение!")
        return

    user = await message.bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id)
    if user.is_chat_admin():
        await message.reply("Я могу разглушить администратора!")
        return

    await message.bot.delete_message(message.chat.id, message.message_id)
    await bot.restrict_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id, can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True, can_add_web_page_previews=True)

    await message.reply_to_message.reply(f"Пользователь {mention(user.user.first_name, user.user.id)} успешно разглушен!")


@dp.message_handler(is_bot_admin=True, is_admin=True, commands=["all"], commands_prefix="!/")
async def all(message: types.Message):
    db.add_chat_table(message)
    db.insert("sett", ["chat_id"], [message.chat.id])
    db.insert(message.chat.id, ["user_id"], [message.from_user.id])

    allow = db.select("sett", "all_allow", "chat_id", message.chat.id)
    if allow == 0:
        return

    users = db.select(message.chat.id, "user_id")
    mentions = []
    for us in users:
        mentions.append(mention("⠀", us[0]))
    mentions = "".join(mentions)
    await message.reply("Общий сбор" + mentions)


def settings_butt(chat_id):
    conn = sqlite3.connect('db.db')
    cur = conn.cursor()
    namelist = [["Бан", "ban_allow"], ["Мут", "mut_allow"], ["Удалять сообщения от групп", "delgroup"], ["All", "all_allow"], ["whoes", "update_sett"]]
    cur.execute(f"INSERT OR IGNORE INTO sett(chat_id) VALUES({chat_id})")
    conn.commit()
    cur.execute(f"SELECT ban_allow, mut_allow, delgroup, all_allow, update_sett FROM sett WHERE chat_id = '{chat_id}'")
    sett = cur.fetchall()
    sett = list(sett[0])
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    buttons = []

    idx = 0
    for set in sett:

        if namelist[idx][0] == "whoes":
            if set == 0:
                onoroff = "Создатель"
            elif set == 1:
                onoroff = "Админы"
            buttons.append(types.InlineKeyboardButton(text=onoroff, callback_data=namelist[idx][1]))
        else:
            if set == 0:
                onoroff = "❌"
            elif set == 1:
                onoroff = "✅"
            buttons.append(types.InlineKeyboardButton(text=namelist[idx][0] + onoroff, callback_data=namelist[idx][1]))
        idx = idx + 1

    buttons.append(types.InlineKeyboardButton(text="Правила", callback_data="rules"))

    keyboard.add(*buttons)
    return keyboard


@dp.message_handler(commands="settings", is_admin=True, is_bot_admin=True)
async def settings(message: types.Message):
    db.add_chat_table(message)
    db.insert("sett", ["chat_id"], [message.chat.id])
    db.insert(message.chat.id, ["user_id"], [message.from_user.id])

    await message.reply("Настройки:", reply_markup=settings_butt(message.chat.id))


@dp.callback_query_handler(is_call_admin=True)
async def calls(call: types.CallbackQuery):
    conn = sqlite3.connect('db.db')
    cur = conn.cursor()
    cur.execute(f"SELECT update_sett FROM sett WHERE chat_id = {call.message.chat.id}")
    update_sett = cur.fetchone()[0]
    if update_sett == 0 or call.data == "update_sett":
        member = await bot.get_chat_member(call.message.chat.id, call.from_user.id)
        if not member.status == "creator":
            return

    if call.data == "rules":
        await dialog.ruls.set()
        await call.message.reply("Введи правила чата:")
        return

    cur.execute(f"SELECT {call.data} FROM sett WHERE chat_id = {call.message.chat.id}")
    allow = cur.fetchone()[0]
    if allow == 0:
        cur.execute(f"UPDATE sett SET {call.data} = 1 WHERE chat_id = {call.message.chat.id}")
        conn.commit()
        await call.message.edit_text("Настройки:", reply_markup=settings_butt(call.message.chat.id))
    else:
        cur.execute(f"UPDATE sett SET {call.data} = 0 WHERE chat_id = {call.message.chat.id}")
        conn.commit()
        await call.message.edit_text("Настройки:", reply_markup=settings_butt(call.message.chat.id))


@dp.message_handler(state=dialog.ruls)
async def rulss(message: types.Message, state: FSMContext):
    conn = sqlite3.connect('db.db')
    cur = conn.cursor()
    cur.execute(f"INSERT OR IGNORE INTO sett(chat_id) VALUES({message.chat.id})")
    cur.execute(f"""UPDATE sett SET rules = '{message.text}
        ' WHERE chat_id = {message.chat.id}""")
    conn.commit()
    await message.reply("Готово✅")
    await state.finish()

@dp.message_handler(is_admin=True, commands=["who"], commands_prefix="!/")
async def who(message: types.Message):
        who = await message.bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id)
        await message.reply(who)