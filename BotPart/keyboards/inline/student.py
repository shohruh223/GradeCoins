from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from BotPart.api import get_students


def inner_back_button():
    ikm = InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn = InlineKeyboardButton(text="⏮️  Orqaga qaytish", callback_data="back_inner")
    ikm.add(btn)
    return ikm


def get_student(group_id):
    ikm = InlineKeyboardMarkup(row_width=1)
    students = get_students(group_id=group_id)

    for student in students:
        button = InlineKeyboardButton(text=f"{student['fullname']}", callback_data=f"{student['id']}")
        ikm.add(button)
    btn1 = InlineKeyboardButton(text=" ⬅️  Orqaga qaytish", callback_data='back_button')
    ikm.add(btn1)
    return ikm


def get_student_for_add(group_id):
    ikm = InlineKeyboardMarkup(row_width=1)
    students = get_students(group_id=group_id)
    for student in students:
        button = InlineKeyboardButton(text=f"ID : {student['id']}  Fullname : {student['fullname']}",
                                      callback_data=f"{student['id']}")
        ikm.add(button)
    btn1 = InlineKeyboardButton(text=" ⬅️  Orqaga qaytish", callback_data='back_button')
    ikm.add(btn1)
    return ikm


def inline_student_button():
    ikm = InlineKeyboardMarkup(row_width=1)
    button = InlineKeyboardButton(text="✅ Hamma studentlar", callback_data="all_students")
    button2 = InlineKeyboardButton(text="✅ Studentning bahosini qo'shish", callback_data="add_student")
    button3 = InlineKeyboardButton(text="✅ Studentning bahosini o'zgartirish", callback_data="update_student")
    ikm.add(button, button2, button3)
    return ikm