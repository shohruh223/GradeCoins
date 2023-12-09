from aiogram import types
from aiogram.dispatcher import FSMContext
from BotPart.handlers.users.start import bot_start
from BotPart.keyboards.default.login import main_menu_cancel
from BotPart.keyboards.inline.student import inline_student_button, get_student
from loader import dp
from BotPart.states.user import LoginState, ShowUserState, AddUserState, UpdateGradeState


@dp.callback_query_handler()
async def check_buttons(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == "about_bot":
        await callback.message.answer_photo(
            photo="https://images.pexels.com/photos/8566470/pexels-photo-8566470.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
            caption="Bizning bot orqali siz o'zingizning baholaringizni va bundan tashqari"
                    "guruhingizdagi o'quvchilar baholarini ko'rib borishingiz mumkin !",
            reply_markup=main_menu_cancel())

    elif callback.data == "login":
        await callback.message.answer(text="<b>Tizimga kirish uchun telefon raqamingizni kiriting ! \n"
                                           "</b>")
        await LoginState.phone_number.set()

    elif callback.data == "cancel":
        # mana shu jarayonda yana start commandi qayta ishga tushiriladi !
        await bot_start(message=callback.message, state=state)
        await state.finish()
    elif callback.data == "back_button":
        await callback.message.answer_photo(
            photo="https://img.freepik.com/free-vector/college-or-university-students-group-young-happy-people"
                  "-standing-isolated-on-white-background_575670-66.jpg?size=626&ext=jpg&ga=GA1.1.1413502914.1696896000&semt=ais",
            reply_markup=inline_student_button())
        await state.finish()

    elif callback.data == "back_inner":
        await callback.message.answer_photo(
            photo="https://img.freepik.com/free-vector/college-or-university-students-group-young-happy-people"
                  "-standing-isolated-on-white-background_575670-66.jpg?size=626&ext=jpg&ga=GA1.1.1413502914.1696896000&semt=ais",
            reply_markup=inline_student_button())
        await state.finish()

    elif callback.data == "all_students":
        await callback.message.answer_photo(
            photo="https://img.freepik.com/free-vector/college-or-university-students-group-young-happy-people"
                  "-standing-isolated-on-white-background_575670-66.jpg?size=626&ext=jpg&ga=GA1.1.1413502914.1696896000&semt=ais",
            reply_markup=get_student(1)
        )
        await ShowUserState.id.set()
    elif callback.data == "add_student":
        await callback.message.answer(text="Qaysi id ga tegishli studentlar baho kiritmoqchisiz ?\n"
                                           "<b><em> ID raqamni kiriting </em></b>")
        await AddUserState.id.set()

    elif callback.data == "update_student":
        await callback.message.answer(text="Qaysi studentni tahrirlamaoqchisiz\n"
                                           "<b>ID raqamni kiriting  : </b>")
        await UpdateGradeState.next()