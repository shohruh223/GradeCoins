from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove
from BotPart.api import get_student_by_id, add_grade_student
from BotPart.handlers.users.start import bot_start
from BotPart.keyboards.inline.student import inline_student_button, inner_back_button
from loader import dp
from BotPart.states.user import ShowUserState, AddUserState


@dp.message_handler(Text(equals="👤 My account"))
async def check_user(message: types.Message):
    await message.answer(text="Mavjud studentlar",
                         reply_markup=ReplyKeyboardRemove())
    await message.answer_photo(
        photo="https://images.pexels.com/photos/1558690/pexels-photo-1558690.jpeg?auto=compress&cs=tinysrgb&w=1600",
        reply_markup=inline_student_button())


@dp.callback_query_handler(lambda callback: callback.data.isdigit() or callback.data == "back_button",
                           state=ShowUserState.id)
async def get_item(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == "back_button":
        await callback.message.answer("Back button clicked.")
        await bot_start(message=callback.message, state=state)
        await state.finish()

    else:
        student_id = int(callback.data)
        student = get_student_by_id(person_id=student_id)
        if "score" in student and student['score']:
            await callback.message.answer_photo(
                photo="https://static.vecteezy.com/system/resources/thumbnails/005/545/335/small/user-sign-icon-person-symbol-human-avatar-isolated-on-white-backogrund-vector.jpg",
                caption=
                f"\n\n\n\n\n\n<b><em>Student Name: {student['fullname']}\n"
                f"Student Phone Number: {student['phone_number']}\n"
                f"Student Group : {student['group']} group\n"
                f"Student grade : {student['score']}</em></b>",
                reply_markup=inner_back_button()
            )
            await state.finish()
        else:
            await callback.message.answer_photo(
                photo="https://static.vecteezy.com/system/resources/thumbnails/005/545/335/small/user-sign-icon-person-symbol-human-avatar-isolated-on-white-backogrund-vector.jpg",
                caption=
                f"\n\n\n\n\n\n<b><em>Student Name: {student['fullname']}\n"
                f"Student Phone Number: {student['phone_number']}\n"
                f"Student Group : {student['group']} group</em></b>",
                reply_markup=inner_back_button()
            )
            await state.finish()


@dp.message_handler(lambda message: message.text.isdigit(), state=AddUserState.id)
async def process_student_grade(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        student_id = int(message.text)
        student = get_student_by_id(person_id=student_id)
        if student:
            data['student_id'] = student_id
            await message.answer("Iltimos, talaba uchun bahoni kiriting:")
            await AddUserState.score.set()
        else:
            await message.answer(text="Bu id tegishli student yo'q\n"
                                      "<b>Iltimos qayta kiriting </b>")


@dp.message_handler(lambda message: message.text.replace(".", "").isdigit(), state=AddUserState.score)
async def process_student_score(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['score'] = float(message.text)

    if 'student_id' in data:
        response = add_grade_student(data['student_id'], data['score'])

        if response.status_code == 201:
            await message.answer(f"Baho {data['score']} student uchun saqlandi.")
            await message.answer_photo(
                photo="https://images.pexels.com/photos/1558690/pexels-photo-1558690.jpeg?auto=compress&cs=tinysrgb&w=1600",
                reply_markup=inline_student_button())

        else:
            await message.answer("Bahoni saqlashda xatolik yuz berdi. Iltimos keyinroq qayta urinib ko'ring.")
    else:
        await message.answer("Iltimos, talaba ID ni kiritib chiqing.")

    await state.finish()
