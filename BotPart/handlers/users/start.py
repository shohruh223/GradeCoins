from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import ReplyKeyboardRemove
from BotPart.api import get_student_by_id, update_grade_in_server, login_user_to_api, add_grade_student
from BotPart.keyboards.default.login import login_button, main_menu_cancel, my_account
from BotPart.keyboards.inline.student import inline_student_button, get_student, inner_back_button
from loader import dp
from BotPart.states.user import LoginState, ShowUserState, AddUserState, UpdateGradeState
import re


@dp.message_handler(CommandStart)
async def bot_start(message: types.Message):
    await message.answer(text=f"Assalomu alaykum {message.from_user.full_name}")

    await message.answer_photo(
        photo="https://images.pexels.com/photos/1558690/pexels-photo-1558690.jpeg?auto=compress&cs=tinysrgb&w=1600",
        reply_markup=login_button())








