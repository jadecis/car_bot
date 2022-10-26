from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from config import bot_token
import logging


bot = Bot(token=bot_token)
logging.basicConfig(level=logging.INFO)
dp= Dispatcher(bot, storage=MemoryStorage())
html= types.ParseMode.HTML#<- &lt; >- &gt; &- &amp;


class Form(StatesGroup):
    Q1= State()
    Q2= State()
    Q3= State()
    Q4= State()
    Q5= State()
    Q6= State()
    Q7= State()
    Q8= State()
    Q9= State()
    Q10= State()
    Q11= State()
    
class Form2(StatesGroup):
    Q1= State()
    Q2= State()
    Q3= State()
    Q4= State()
    Q5= State()
    Q6= State()
    Q7= State()
    Q8= State()
    Q9= State()
    Q10= State()
    Q11= State()
    Q12= State()