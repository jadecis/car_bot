from loader import dp
from aiogram import executor
from src import main 


executor.start_polling(dp, skip_updates=False)