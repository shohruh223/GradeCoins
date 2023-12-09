from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from BotPart.api import get_students


def login_button():
    rkm = InlineKeyboardMarkup(row_width=1)
    btn = InlineKeyboardButton(text="👤  Tizimga kirish", callback_data='login')
    btn2 = InlineKeyboardButton(text="🤖 Bot haqida", callback_data='about_bot')
    rkm.add(btn, btn2)
    return rkm


def main_menu_cancel():
    rkm = InlineKeyboardMarkup(row_width=1)
    btn = InlineKeyboardButton(text="⬅️  Orqaga qaytish", callback_data='cancel')
    rkm.add(btn)
    return rkm


def my_account():
    rkm = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn = KeyboardButton(text="👤 My account")
    return rkm.add(btn)