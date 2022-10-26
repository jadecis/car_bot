import shutil
import emoji
import os
from aiogram.types import Message, CallbackQuery, MediaGroup, ReplyKeyboardRemove, BotCommand
from loader import bot, dp, html, Form
from src.keyboard import persent_markup, problem_markup, accept_menu, next_button, main_menu
from aiogram.dispatcher import FSMContext
from config import admin_chat_сar
from datetime import datetime, timedelta
from PIL import Image
import time
from fpdf import FPDF

@dp.message_handler(text= 'Pick Up 🆙')
async def start_form_1(msg: Message):
    await msg.answer(text="<b>1.</b> Driver's name ?\n\nИмя водителя ?", parse_mode=html)
    await Form.Q1.set()

@dp.message_handler(content_types=['text'], state=Form.Q1)
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
    await msg.answer(text="<b>6.</b> Petrol level % ?\n\nУровень бензина в баке в % ?",
                     parse_mode=html,
                     reply_markup=persent_markup())
    await Form.Q6.set()
    
@dp.callback_query_handler(text_contains= 'per_', state=Form.Q6)
async def q6_answer(call: CallbackQuery, state: FSMContext):
    await state.update_data(per_level= call.data.split('_')[1])
    await call.message.delete()
    await call.message.answer(text="<b>7.</b> Car 360 photo: Please upload 4 photos of the car\nPlease, press on button <b>«Next»</b>, if you finish send media!\n\n"
                                 +f"Сфоткать авто снаружи и изнутри для фиксации состояния. Пожалуйста, загрузите 4 фото авто. По окончанию нажми на конпку <b>«Next»</b>",
                                 parse_mode=html,
                                 reply_markup=next_button)
    #print(await state.get_data())
    await Form.Q7.set() 
    
@dp.message_handler(content_types=['photo', 'video', 'document'], state=Form.Q7)
async def q7_answer(msg: Message, state: FSMContext):
    data = await state.get_data()
    print(data.get('media'))
    media_list= []
    if data.get('media') != None:
        for file_id in data.get('media'):
            media_list.append(file_id)
    if msg.content_type == 'photo':
        media= {
            'photo' : msg.photo[-1].file_id
        }
        media_list.append(media)
    if msg.content_type == 'video':
        media= {
            'video' : msg.video.file_id
        }
        media_list.append(media)
    
    await state.update_data(media=media_list)


@dp.message_handler(content_types=['text'], state=Form.Q7)
async def q7_1_answer(msg: Message, state: FSMContext):
    data =await state.get_data()
    if msg.text == 'Next':
        if data.get('media') != None and len(data.get('media')) >= 4:
            await msg.answer(text="<b>8.</b> Any problems with the car ??\n\nЕсть ли какие нибудь проблемы сделанные клиентом ? Поломка, царапины ?",
                        parse_mode=html,
                        reply_markup= problem_markup)
            await Form.Q8.set()
        else:
            await msg.answer(text="“Please upload 4 photos of the car\n\n Пожалуйста, загрузите 4 фото авто!", parse_mode=html)
            await Form.Q7.set()
    else:
        await msg.answer(text="I'm waiting for media (photo, video) of the car at the moment! Please, press on button <b>«Next»</b>, if you finish send media!"
                         +f"\n\nЯ жду медиа материал автомобиля в данный момент! Нажми на конпку <b>«Next»</b>, если ты отправил все фото!",
                         parse_mode=html)
        await Form.Q7.set()


@dp.callback_query_handler(text_contains= 'prob_', state=Form.Q8)
async def q8_answer(call: CallbackQuery, state: FSMContext):
    if call.data.split('_')[1] == 'yes':
        await call.message.delete()
        await call.message.answer(text="<b>9.</b> Photo of the problem ?\nPlease, press on button <b>«Next»</b>, if you finish send media!"
                                     +f"\n\nПожалуйста, сфоткайте именно проблемные места авто после получения для фиксации. По окончанию нажми на конпку <b>«Next»</b>",
                                     parse_mode=html, 
                                     reply_markup=next_button)
        await Form.Q9.set()
    if call.data.split('_')[1] == 'no':
        await call.message.delete_reply_markup()
        await call.message.edit_text(text="<b>9.</b> Pickup address ?\n\nНапишите адрес", parse_mode=html)
        await Form.Q10.set()

@dp.message_handler(content_types=['photo', 'video', 'document'], state=Form.Q9)
async def q9_answer(msg: Message, state: FSMContext):
    data = await state.get_data()
    media_list= []
    if data.get('prob_media') != None:
        for file_id in data.get('prob_media'):
            media_list.append(file_id)
    if msg.content_type == 'photo':
        media= {
            'photo' : msg.photo[-1].file_id
        }
        media_list.append(media)
    if msg.content_type == 'video':
        media= {
            'video' : msg.video.file_id
        }
        media_list.append(media)

    await state.update_data(prob_media=media_list)
    
@dp.message_handler(content_types=['text'], state=Form.Q9)
async def q9_1_answer(msg: Message, state: FSMContext):
    data = await state.get_data()
    if msg.text == 'Next':
        if data.get('prob_media') == None:
            await msg.answer(text="You <b>must</b> send media of the car!\n\n Отправка медиа машины <b>обязательна</b>!", parse_mode=html)
            await Form.Q9.set()
        else:
            await msg.answer(text="<b>10.</b> Pickup address ?\n\nНапишите адрес", parse_mode=html, reply_markup=ReplyKeyboardRemove())
            await Form.Q10.set()
    else:
        await msg.answer(text="I'm waiting for media (photo, video) of the problem car at the moment! Please, press on button <b>«Next»</b>, if you finish send media!"
                        +f"\n\nЯ жду медиа материал проблемных мест автомобиля в данный момент! Нажми на конпку <b>«Next»</b>, если ты отправил все фото!",
                         parse_mode=html)
        await Form.Q9.set()

@dp.message_handler(content_types=['text'], state=Form.Q10)
async def q10_answer(msg: Message, state: FSMContext):
    data= await state.get_data()
    if data.get('prob_media') is None:
        answer_prob= 'No'
    else:
        answer_prob= 'Yes'
    

    form_user= f"""
⏱ <b>Date:</b> <code>{(datetime.now()+ timedelta(hours=1)).strftime('%d.%m.%Y %H:%M')}</code>
🧔 <b>Driver's name:</b> <code>{data.get('driver_name')}</code>
🙋‍♂️ <b>Customer name:</b> <code>{data.get('customer_name')}</code>
🚘 <b>Car model:</b> <code>{data.get('car_model')}</code>
🔢 <b>Plate number:</b> <code>{data.get('plate_number')}</code>
📊 <b>Car odometer:</b> <code>{data.get('car_odometer')}</code>
⛽️ <b>Petrol level %:</b> <code>{data.get('per_level')}</code>
🗺 <b>Pickup address:</b> <code>{msg.text}</code>
🚒 <b>Any problems with the car ?:</b> <code>{answer_prob}</code>
"""  
    pdf_user= f"""
Date: {(datetime.now()+ timedelta(hours=1)).strftime('%d.%m.%Y %H:%M')}
Driver's name: {data.get('driver_name')}
Customer name: {data.get('customer_name')}
Car model: {data.get('car_model')}
Plate number: {data.get('plate_number')}
Car odometer: {data.get('car_odometer')}
Petrol level %: {data.get('per_level')}
Any problems with the car: {answer_prob}
Pickup address: {msg.text}

"""  
    await state.update_data(form_text=form_user )
    await state.update_data(pdf_text=pdf_user )
    media = MediaGroup()
    prob_media = MediaGroup()
    try:
        print(data.get('media'))
        for file_id in data.get('media'):
            for k, v in file_id.items():
                if k == 'photo':
                    await bot.download_file_by_id(file_id=v, destination_dir='src/car_form/media_data')
                    media.attach_photo(v, 'Car 360 photo')
                elif k == 'video':
                    media.attach_video(v, 'Car 360 photo')
        await state.update_data(media_group= media)
        
        if  data.get('prob_media') != None:      
            for file_id_prob in data.get('prob_media'):
                for k, v in file_id_prob.items():
                    if k == 'photo':
                        await bot.download_file_by_id(file_id=v, destination_dir='src/car_form/media_data')
                        prob_media.attach_photo(v, 'Photo of the problem')
                    elif k == 'video':
                        prob_media.attach_video(v, 'Photo of the problem')
            await state.update_data(prob_media_group= prob_media)
            await msg.answer_media_group(media=prob_media)
            
        
        await msg.answer_media_group(media=media)
        await msg.answer(text=form_user, reply_markup=accept_menu, parse_mode=html)
        await Form.Q11.set()
    except Exception as ex:
        print(ex)
        await msg.answer("An error has occurred! Please, take the test again\n\n"
                         +f"Произошла ошибка. Пожалуйста, пройдите тест заного !", reply_markup=main_menu)
        await state.finish()
    
@dp.callback_query_handler(text_contains= 'accept_', state=Form.Q11)
async def accept_answer(call: CallbackQuery, state: FSMContext):
    if call.data.split('_')[1] == 'accept':
        data= await state.get_data()
        media= data.get('media_group')

        
        await call.message.answer('Thank for using the bot, requests successfully sent!\n\nСпасибо за использование бота, заявка успешно отправлена!', reply_markup=main_menu)
 
        await bot.send_message(chat_id=admin_chat_сar,
                               text=f"Pick up @{call.message.chat.username}\n"
                               +f"{data.get('form_text')}",
                               parse_mode=html)
        
        await bot.send_message(chat_id=admin_chat_сar,
                               text=f"Photo 360 car")
        await bot.send_media_group(chat_id=admin_chat_сar,
                                   media=media)
        if  data.get('prob_media') != None:
            prob_media= data.get('prob_media_group')
            await bot.send_message(chat_id=admin_chat_сar,
                               text=f"Photo problems")
            await bot.send_media_group(chat_id=admin_chat_сar,
                                    media=prob_media)
        
        pdf= FPDF()
        pdf.add_page()
        pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
        pdf.set_font('DejaVu', size=14)
        pdf_user= data.get('pdf_text')
        new_pdf_user= emoji.demojize(pdf_user)  

        pdf.cell(200, 10, txt=f'Pick up @{call.message.chat.username}', new_x="LMARGIN" , new_y="NEXT", align='C')

        pdf.write(txt= f"{new_pdf_user}", h=10)
        pdf.cell(400, 20, new_x="LMARGIN" , new_y="NEXT", align='L')
        imges= os.listdir('src/car_form/media_data/photos')
        for i in imges:
            pdf.cell(200, 10, new_x="LMARGIN" , new_y="NEXT", align='L')
            im= Image.open(f"src/car_form/media_data/photos/{i}", "r")
            w, h = im.size
            im.close()
            if w > 100 or h > 100:
                mid_size = (w//100 + h//100) // 2
            else:
                mid_size=1
            pdf.image(
                name=f"src/car_form/media_data/photos/{i}",
                w=w // mid_size,
                h=h // mid_size,
            )
        shutil.rmtree('src/car_form/media_data/photos')

        pdf.output('Pick up.pdf')

        await bot.send_document(chat_id=admin_chat_сar,
                                document=open('Pick up.pdf', "rb"))
        
        await state.finish()      
    if call.data.split('_')[1] == 'cancel':
        await state.finish()
        await call.message.delete()
        await call.message.answer(text="<b>1.</b> Driver's name ?\n\nИмя водителя ?", parse_mode=html, reply_markup=main_menu)
        await Form.Q1.set()