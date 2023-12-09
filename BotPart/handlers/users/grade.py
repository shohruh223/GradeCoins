from aiogram import types
from aiogram.dispatcher import FSMContext
from BotPart.api import get_student_by_id, update_grade_in_server
from loader import dp
from BotPart.states.user import UpdateGradeState


@dp.message_handler(lambda message: message.text.isdigit(), state=UpdateGradeState.id)
async def process_student_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['person_id'] = int(message.text)
        student_id = int(message.text)
        student = get_student_by_id(person_id=student_id)
        if student:
            data['student_id'] = student_id
            await message.answer("Iltimos, talaba uchun bahoni yangilang:")
            await UpdateGradeState.score.set()
        else:
            await message.answer(text="Bu id tegishli student yo'q\n"
                                      "<b>Iltimos qayta kiriting </b>")


@dp.message_handler(state=UpdateGradeState.score)
async def process_score(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['score'] = float(message.text)

    # Yangi baho qiymatini serverga yuborish
    success = update_grade_in_server(data['person_id'], data['score'])

    if success:
        await message.answer(
            f"<b>{data['person_id']}- id ga tegishli studentning bahosi {data['score']} bahoga yangilandi </b>")
    else:
        await message.answer(f"Bahoni yangilashda xatolik yuz berdi. Iltimos  qayta urinib ko'ring.")