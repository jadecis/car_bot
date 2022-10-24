from aiogram.types import Message
from loader import dp, html
from aiogram.dispatcher.filters import CommandStart
from src.keyboard import main_button




@dp.message_handler(CommandStart(), state="*")
@dp.message_handler(CommandStart())
async def start_command(msg: Message):
    print(msg.chat.id)
    await msg.answer(text= f"Привет, @{msg.chat.username} !\n\n"
                     +f"<i>Этот бот принимает заявки от пользователей, просто отвечайте на вопросы бота и следуй его командам!</i>\n"
                     +f"Чтобы пройти анкетирование нажмите <b>«Pick Up 🆙»</b>",
                     reply_markup=main_button,
                     parse_mode=html)
