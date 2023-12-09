from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import ReplyKeyboardRemove
from BotPart.api import login_user_to_api
from BotPart.keyboards.default.login import my_account
from loader import dp
from BotPart.states.user import LoginState
import re


@dp.message_handler(state=LoginState.phone_number)
async def request_password(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        phone_number = message.text.strip()
        if not re.match(r'^\+998\d{9}$', phone_number):
            await message.answer(
                "Noto'g'ri telefon raqam formati. Iltimos, to'g'ri formatda kiriting, masalan: +998913333321")
            return

        data['phone_number'] = phone_number
        await message.answer("Passwordni kiriting:")
        await LoginState.password.set()


@dp.message_handler(state=LoginState.password)
async def process_password(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        password = message.text.strip()
        if len(password) != 8:
            await message.answer("Passwordni kiritishda xatolik bor! Passwordingiz 8 ta belgidan iborat bo'lsin.")
            return

        data['password'] = password

        response = login_user_to_api(data['phone_number'], data['password'])
        if response.status_code == 200:
            user_info = response.json()  # JSON javobni o'qish
            is_teacher = user_info.get('is_teacher', False)  # Agar "is_teacher" mavjud bo'lsa olish, aks holda False
            if is_teacher:
                await message.reply("<b>Siz teacher ekansiz !\n\nMuvaffaqiyatli login</b>",
                                    reply_markup=my_account())

            else:
                await message.reply("<b>Siz student ekansiz!</b>",
                                    reply_markup=ReplyKeyboardRemove())
            await state.finish()
        else:
            await message.reply(
                "Noto'g'ri telefon raqam yoki parol.\n<b><em>Iltimos telefon raqam va passwordingizni qayta kiriting!</em></b>")
            await LoginState.phone_number.set()
