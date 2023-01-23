from aiogram import types
from dp import dp, bot
from key import add_buttons, add_inline_url
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from utils import *
from config import *
import os

db = DB()


class dialog(StatesGroup):
    question_text = State()
    answer_text = State()
    posting = State()
    feedback_mes_id = None


@dp.message_handler(commands=['start'])
async def start_command(msg: types.Message):
    if msg.chat.type == 'private':
        db.insert("private", ["user_id"], [msg.from_user.id])
        await msg.reply("""Добро пожаловать в Squad Booster!
Добавьте бота в группу и назначьте его администратором.""", reply_markup=add_buttons(["👤 Профиль", "✉ Обратная связь", "ℹ О боте", "📝 Команды"]))
    else:
        await msg.reply("""Привет!
Чтобы воспользоваться всеми моими функциями назначьте меня администратором.""")


@dp.message_handler(text="👤 Профиль")
async def profile_command(msg: types.Message):
    if not msg.chat.type == 'private':
        return
    me = await bot.get_me()
    await msg.reply(f"""👤 Профиль\n
❤ Пользователь: {msg.from_user.full_name}
🔑 Ваш ID: {msg.from_user.id}
➕ Добавлено в групп: [скоро]\n
📆 Дата регистрации: [скоро]""", reply_markup=add_inline_url("Добавить бота в чат", f"http://t.me/{me.username}?startgroup=hbase"))


@dp.message_handler(text="✉ Обратная связь")
async def feedback(message: types.Message):
    if not message.chat.type == 'private':
        return
    await message.reply(f"Обратная связь - здесь вы можете связаться с нашими модераторами, которые с удовольствием ответят на ваш вопрос.\nНапишите ваш вопрос:", reply_markup=add_buttons(["◀️ Назад"]))
    await dialog.question_text.set()


@dp.message_handler(state=dialog.question_text, content_types="any")
async def state_feedback_question(message: types.Message, state: FSMContext):
    if message.text == "◀️ Назад":
        await message.reply("Чтобы продолжить, выбери нужную кнопку на кливиатуре.", reply_markup=add_buttons(["👤 Профиль", "✉ Обратная связь", "ℹ О боте", "📝 Команды"]))
        await state.finish()
        return
    db.insert("feedback", ["user_id"], [message.from_user.id])
    quest = db.select("feedback", "quest", "user_id", message.from_user.id)
    await bot.send_message(admin_id, f"[{message.from_user.first_name}](tg://user?id={message.from_user.id}), говорит: (Message ID: {quest})", parse_mode="Markdown")
    await bot.forward_message(admin_id, message.chat.id, message.message_id)
    await state.finish()


@dp.message_handler(commands="answ")
async def answ(message: types.Message):
    if not message.from_user.id == admin_id:
        return
    msg = message.text.split()
    msg.remove("/answ")
    msg = " ".join(msg)
    user_id = db.select("feedback", "user_id", "quest", msg)
    if user_id is None:
        await message.reply("Ошибка!")
        return
    dialog.feedback_mes_id = user_id
    await message.reply("Введите ответ на этот вопрос:")
    await dialog.answer_text.set()
    db.delete("feedback", "quest", msg)


@dp.message_handler(state=dialog.answer_text, content_types="any")
async def state_feedback_answer(message: types.Message, state: FSMContext):
    await bot.send_message(dialog.feedback_mes_id, f'Ответ от модератора:')
    await bot.copy_message(dialog.feedback_mes_id, message.chat.id, message.message_id)
    await state.finish()


@dp.message_handler(text="ℹ О боте")
@dp.message_handler(commands=['help'])
async def about_command(msg: types.Message):
    if not msg.chat.type == 'private':
        return
    await msg.reply("Squad Booster Bot - создан для модерации групп. За новостями о боте можно следить на нашем канале @SquadBooster. Есть вопросы или какие-либо пожелания, то можете обратиться сюда - @iv4bn.")


@dp.message_handler(text="📝 Команды")
@dp.message_handler(commands=['help'])
async def help_command(msg: types.Message):
    if not msg.chat.type == 'private':
        return
    await msg.reply("""Команды:
/warn - предупреждение;
/unwarn - снять предупреждение;
/ban - выгнать участника из группы;
/unban - снятие ограничений на вход в группу для изгнанного участника:
/mute - запрет на написание сообщений в группе;
/umute - снятие ограничений;
/all - упомянуть всех в чате;
/online - упомянуть всех в чате кто онлайн.""")


@dp.message_handler(text="◀️ Назад")
async def back_command(msg: types.Message):
    await msg.reply("Чтобы продолжить, выбери нужную кнопку на кливиатуре.",
                        reply_markup=add_buttons(["👤 Профиль", "✉ Обратная связь", "ℹ О боте", "📝 Команды"]))


@dp.message_handler(commands="post")
async def post(message: types.Message):
    if not message.chat.type == 'private':
        return
    if not message.from_user.id == admin_id:
        return
    await message.reply("Введи сообщение для рассылки:")
    await dialog.posting.set()


@dp.message_handler(state=dialog.posting)
async def posting(message: types.Message, state: FSMContext):
    ids = db.select("private", "user_id")
    for usid in ids:
        try: await bot.copy_message(usid[0], message.chat.id, message.message_id)
        except: pass
    await state.finish()


@dp.message_handler(commands="info")
async def settings(message: types.Message):
    conn = sqlite3.connect('db.db')
    cur = conn.cursor()
    if not message.from_user.id == admin_id:
        return
    cur.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
    tables = cur.fetchall()
    tables.remove(('private',))
    tables.remove(('sett',))
    tables.remove(('feedback',))
    cur.execute("SELECT user_id FROM private ")
    users = cur.fetchall()
    with open('newfile.txt', 'w+', encoding="utf-8") as file:
        file.write(f"Список чатов в которых был добавлен бот({len(tables)}): {tables}\n")
        file.write(f"Пользователи которые нажали на старт({len(users)}): {users}\n")
        file.close()
    doc = open("newfile.txt", "rb")
    await bot.send_document(message.chat.id, doc)
    os.remove("newfile.txt")
