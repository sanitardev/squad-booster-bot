from aiogram import types


def add_buttons(buttons: list):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)
    return keyboard


def add_inline_url(text, url):
    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text=text, url=url)
    keyboard.add(button)
    return keyboard

def add_inline(text, data):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    buttons = [types.InlineKeyboardButton(text=text, callback_data=data)]
    keyboard.add(*buttons)
    return keyboard