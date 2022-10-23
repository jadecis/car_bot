from email import message
from pkgutil import get_data
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import Dispatcher
from loader import bot, dp, html, Form
from aiogram.dispatcher.filters import CommandStart
from src.keyboard import start_markup, persent_markup, problem_markup
from aiogram.dispatcher import FSMContext

@dp.message_handler(CommandStart())
async def start_command(msg: Message):
    await msg.answer(text= f"Привет, @{msg.chat.username} !\n\n"
                     +f"<i>Этот бот принимает заявки от пользователей, просто отвечайте на вопросы бота и следуй его командам!</i>\n\n"
                     +f"Чтобы пройти анкетирование нажмите <b>«НАЧАТЬ»</b>", 
                     parse_mode=html, 
                     reply_markup=start_markup)
    
@dp.callback_query_handler(text= 'start')
async def start_form(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(text="<b>1.</b> Driver's name ?\n\nИмя водителя ?", parse_mode=html)
    await Form.Q1.set()
    
    
#@dp.message_handler(content_types=['text'], state=Form.Q1)
async def q1_answer(msg: Message, state: FSMContext):
    await state.update_data(driver_name= msg.text)
    await msg.answer(text="<b>2.</b> Customer name ?\n\nИмя Клиента ?", parse_mode=html)
    await Form.Q2.set()
    
@dp.message_handler(content_types=['text'], state=Form.Q2)
async def q2_answer(msg: Message, state: FSMContext):
    await state.update_data(customer_name= msg.text)
    await msg.answer(text="<b>3.</b> Car model ?\n\nМодель автомобиля ?", parse_mode=html)
    await Form.Q3.set()
    
@dp.message_handler(content_types=['text'], state=Form.Q3)
async def q3_answer(msg: Message, state: FSMContext):
    await state.update_data(car_model= msg.text)
    await msg.answer(text="<b>4.</b> Plate number ?\n\nНомерной знак ?", parse_mode=html)
    await Form.Q4.set()
    
@dp.message_handler(content_types=['text'], state=Form.Q4)
async def q4_answer(msg: Message, state: FSMContext):
    await state.update_data(plate_number= msg.text)
    await msg.answer(text="<b>5.</b> Car odometer ?\n\nОдометр автомобиля ?", parse_mode=html)
    await Form.Q5.set()
    
@dp.message_handler(content_types=['text'], state=Form.Q5)
async def q5_answer(msg: Message, state: FSMContext):
    await state.update_data(car_odometer= msg.text)
    await msg.answer(text="<b>5.</b> Petrol level % ?\n\nУровень бензина в баке в % ?",
                     parse_mode=html,
                     reply_markup=persent_markup())
    await Form.Q6.set()
    
@dp.callback_query_handler(text_contains= 'per_', state=Form.Q6)
async def q6_answer(call: CallbackQuery, state: FSMContext):
    await state.update_data(per_level= call.data.split('_')[1])
    await call.message.edit_text(text="<b>6.</b> Car 360 photo ?\n\nСфоткать авто снаружи и изнутри для фиксации состояния", parse_mode=html)
    #print(await state.get_data())
    await Form.Q7.set() 
    
@dp.message_handler(content_types=['photo', 'video', 'document'], state=Form.Q7)
async def q7_answer(msg: Message, state: FSMContext):
    if msg.content_type == 'photo':
        await state.update_data(media= msg.photo[-1].file_id)
    if msg.content_type == 'video':
        await state.update_data(media= msg.video.file_id)
    if msg.content_type == 'document':
        await state.update_data(media= msg.document.file_id)
    await msg.answer(text="<b>7.</b> Any problems with the car ??\n\nЕсть ли какие нибудь проблемы сделанные клиентом ? Поломка, царапины ?",
                     parse_mode=html,
                     reply_markup= problem_markup)
    await Form.Q8.set()

@dp.callback_query_handler(text_contains= 'prob_', state=Form.Q8)
async def q8_answer(call: CallbackQuery, state: FSMContext):
    if call.data.split('_')[1] == 'yes':
        await call.message.edit_text(text="<b>8.</b> Photo of the problem ?\n\nПожалуйста, сфоткайте именно проблемные места авто после получения для фиксации", parse_mode=html)
        await Form.Q9.set()
    if call.data.split('_')[1] == 'no':
        await call.message.edit_text(text="<b>8.</b> Pickup address ?\n\nНапишите адрес", parse_mode=html)
        await Form.Q10.set()
        #print(await state.get_data())

@dp.message_handler(content_types=['photo', 'video', 'document'], state=Form.Q9)
async def q7_answer(msg: Message, state: FSMContext):
    if msg.content_type == 'photo':
        await state.update_data(prob_media= msg.photo[-1].file_id)
    if msg.content_type == 'video':
        await state.update_data(prob_media= msg.video.file_id)
    if msg.content_type == 'document':
        await state.update_data(prob_media= msg.document.file_id)
    await msg.answer(text="<b>9.</b> Pickup address ?\n\nНапишите адрес", parse_mode=html)
    await Form.Q10.set()
     

@dp.message_handler(content_types=['text'], state=Form.Q10)
async def q10_answer(msg: Message, state: FSMContext):
    data= await state.get_data()

