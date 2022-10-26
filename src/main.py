from aiogram.types import Message
from loader import dp, html, bot
from aiogram.dispatcher.filters import CommandStart
from src.keyboard import main_menu
from aiogram.dispatcher import FSMContext
import emoji
from datetime import date




@dp.message_handler(CommandStart(), state="*")
@dp.message_handler(CommandStart())
async def start_command(msg: Message, state: FSMContext):
    await state.finish()
    print(msg.chat.id)
    await msg.answer(text= f"Привет, @{msg.chat.username} !\n\n"
                     +f"Этот бот, компании <b>Royal Dream 🚗</b>, принимает анкеты от водителей 👨\n"
                     +f"<i>Просто отвечайте на вопросы бота и следуйте его командам!\nЧтобы пройти анкетирование выбирете форму !</i>",
                     reply_markup=main_menu,
                     parse_mode=html)