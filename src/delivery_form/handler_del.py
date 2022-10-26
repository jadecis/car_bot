from aiogram.types import Message, CallbackQuery, MediaGroup, ReplyKeyboardRemove
from loader import bot, dp, html, Form2
from src.keyboard import persent_markup, next_button, problem_markup, main_menu, accept_menu
from aiogram.dispatcher import FSMContext
from config import admin_chat_del
from datetime import datetime, timedelta
import os
from PIL import Image
from fpdf import FPDF
import shutil
import emoji






@dp.message_handler(text= 'Delivery 🚚')
async def start_Form2_1(msg: Message):
    await msg.answer(text="<b>1.</b> Driver's name ?\n\nИмя водителя ?", parse_mode=html)
    await Form2.Q1.set()

@dp.message_handler(content_types=['text'], state=Form2.Q1)
async def q1_answer(msg: Message, state: FSMContext):
    await state.update_data(driver_name2= msg.text)
    await msg.answer(text="<b>2.</b> Customer name ?\n\nИмя Клиента ?", parse_mode=html)
    await Form2.Q2.set()

@dp.message_handler(content_types=['text'], state=Form2.Q2)
async def q2_answer(msg: Message, state: FSMContext):
    await state.update_data(customer_name2= msg.text)
    await msg.answer(text="<b>3.</b> Photo of Driving license, ID and Passport\nPlease, press on button <b>«Next»</b>, if you finish send media!\n\n"
                     +f"Пожалуйста, приложите фото водительских прав, паспорта или ID карту. По окончанию нажми на конпку <b>«Next»</b>", 
                     parse_mode=html,
                     reply_markup=next_button)
    await Form2.Q3.set()
    
@dp.message_handler(content_types=['photo', 'video', 'document'], state=Form2.Q3)
async def q3_answer(msg: Message, state: FSMContext):
    data = await state.get_data()
    print(data.get('media_doc'))
    media_list= []
    if data.get('media_doc') != None:
        for file_id in data.get('media_doc'):
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
    
    await state.update_data(media_doc=media_list)


@dp.message_handler(content_types=['text'], state=Form2.Q3)
async def q3_1_answer(msg: Message, state: FSMContext):
    data =await state.get_data()
    if msg.text == 'Next':
        if data.get('media_doc')!= None and len(data.get('media_doc')) >= 2:
            await msg.answer(text="<b>4.</b> Car model ?\n\nМодель автомобиля ?", parse_mode=html)
            await Form2.Q4.set()
        else:
            await msg.answer(text="You <b>must</b> send 2 photo of the car!\n\n<b>Обязательная</b> отправка фото! Минимальное количество <b>- 2</b>", parse_mode=html)
            await Form2.Q3.set()
    else:
        await msg.answer(text="I'm waiting for media (photo, video) of the car at the moment! Please, press on button <b>«Next»</b>, if you finish send media!"
                         +f"\n\nЯ жду медиа материал автомобиля в данный момент! Нажми на конпку <b>«Next»</b>, если ты отправил все фото!",
                         parse_mode=html)
        await Form2.Q3.set()

   
@dp.message_handler(content_types=['text'], state=Form2.Q4)
async def q4_answer(msg: Message, state: FSMContext):
    await state.update_data(car_model2= msg.text)
    await msg.answer(text="<b>5.</b> Plate number ?\n\nНомерной знак ?", parse_mode=html)
    await Form2.Q5.set()
    
@dp.message_handler(content_types=['text'], state=Form2.Q5)
async def q5_answer(msg: Message, state: FSMContext):
    await state.update_data(plate_number2= msg.text)
    await msg.answer(text="<b>6.</b> Car odometer ?\n\nОдометр автомобиля ?", parse_mode=html)
    await Form2.Q6.set()
    
@dp.message_handler(content_types=['text'], state=Form2.Q6)
async def q6_answer(msg: Message, state: FSMContext):
    await state.update_data(car_odometer2= msg.text)
    await msg.answer(text="<b>7.</b> Petrol level % ?\n\nУровень бензина в баке в % ?",
                     parse_mode=html,
                     reply_markup=persent_markup())
    await Form2.Q7.set()
    
@dp.callback_query_handler(text_contains= 'per_', state=Form2.Q7)
async def q7_answer(call: CallbackQuery, state: FSMContext):
    await state.update_data(per_level2= call.data.split('_')[1])
    await call.message.delete()
    await call.message.answer(text="<b>8.</b> Car 4 sides photo\nPlease, press on button <b>«Next»</b>, if you finish send media!\n\n"
                                 +f"Сфоткать авто снаружи с 4-х сторон и изнутри для фиксации состояния. По окончанию нажми на конпку <b>«Next»</b>",
                                 parse_mode=html,
                                 reply_markup=next_button)
    await Form2.Q8.set() 
    
@dp.message_handler(content_types=['photo', 'video', 'document'], state=Form2.Q8)
async def q8_answer(msg: Message, state: FSMContext):
    data = await state.get_data()
    print(data.get('media_side'))
    media_list= []
    if data.get('media_side') != None:
        for file_id in data.get('media_side'):
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
    
    await state.update_data(media_side=media_list)
    
@dp.message_handler(content_types=['text'], state=Form2.Q8)
async def q8_1_answer(msg: Message, state: FSMContext):
    
    data =await state.get_data()
    if msg.text == 'Next':
        if data.get('media_side') != None and len(data.get('media_side')) >= 4:
            await msg.answer(text="<b>9.</b> Any problems with the car ??\n\nЕсть ли какие нибудь проблемы сделанные клиентом ? Поломка, царапины ?",
                        parse_mode=html,
                        reply_markup= problem_markup)
            await Form2.Q9.set()
        else:
            await msg.answer(text="You <b>must</b> send 4 photo of the car!\n\n<b>Обязательная</b> отправка фото! Минимальное количество <b>- 4</b>", parse_mode=html)
            await Form2.Q8.set()
    else:
        await msg.answer(text="I'm waiting for media (photo, video) of the car 4 sides photo at the moment! Please, press on button <b>«Next»</b>, if you finish send media!"
                         +f"\n\nЯ жду медиа материал автомобиля снаружи в данный момент! Нажми на конпку <b>«Next»</b>, если ты отправил все фото!",
                         parse_mode=html)
        await Form2.Q8.set()
        
@dp.callback_query_handler(text_contains= 'prob_', state=Form2.Q9)
async def q9_answer(call: CallbackQuery, state: FSMContext):
    if call.data.split('_')[1] == 'yes':
        await call.message.delete()
        await call.message.answer(text="<b>9.</b> Photo of the problem ?\nPlease, press on button <b>«Next»</b>, if you finish send media!"
                                     +f"\n\nПожалуйста, сфоткайте именно проблемные места авто после получения для фиксации. По окончанию нажми на конпку <b>«Next»</b>",
                                     parse_mode=html, 
                                     reply_markup=next_button)
        await Form2.Q10.set()
    if call.data.split('_')[1] == 'no':
        await call.message.delete_reply_markup()
        await call.message.edit_text(text="<b>9.</b> Delivery address ?\n\nНапишите адрес", parse_mode=html)
        await Form2.Q11.set()
        
        
@dp.message_handler(content_types=['photo', 'video', 'document'], state=Form2.Q10)
async def q10_answer(msg: Message, state: FSMContext):
    data = await state.get_data()
    media_list= []
    if data.get('media_prob') != None:
        for file_id in data.get('media_prob'):
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

    await state.update_data(media_prob=media_list )
    
@dp.message_handler(content_types=['text'], state=Form2.Q10)
async def q10_1_answer(msg: Message, state: FSMContext):
    data = await state.get_data()
    if msg.text == 'Next':
        if data.get('media_prob') == None:
            await msg.answer(text="You <b>must</b> send media of the car!\n\n Отправка медиа машины <b>обязательна</b>!", parse_mode=html)
            await Form2.Q10.set()
        else:
            await msg.answer(text="<b>10.</b> Delivery address ?\n\nНапишите адрес", parse_mode=html, reply_markup=ReplyKeyboardRemove())
            await Form2.Q11.set()
    else:
        await msg.answer(text="I'm waiting for media (photo, video) of the problem car at the moment! Please, press on button <b>«Next»</b>, if you finish send media!"
                        +f"\n\nЯ жду медиа материал проблемных мест автомобиля в данный момент! Нажми на конпку <b>«Next»</b>, если ты отправил все фото!",
                         parse_mode=html)
        await Form2.Q10.set()
        
@dp.message_handler(content_types=['text'], state=Form2.Q11)
async def q11(msg: Message, state: FSMContext):
    data= await state.get_data()
    if data.get('media_prob') is None:
        answer_prob= 'No'
    else:
        answer_prob= 'Yes'
        
    form_user= f"""
⏱ <b>Date:</b> <code>{(datetime.now()+ timedelta(hours=1)).strftime('%d.%m.%Y %H:%M')}</code>   
🧔 <b>Driver's name:</b> <code>{data.get('driver_name2')}</code>
🙋‍♂️ <b>Customer name:</b> <code>{data.get('customer_name2')}</code>
🚘 <b>Car model:</b> <code>{data.get('car_model2')}</code>
🔢 <b>Plate number:</b> <code>{data.get('plate_number2')}</code>
📊 <b>Car odometer:</b> <code>{data.get('car_odometer2')}</code>
⛽️ <b>Petrol level %:</b> <code>{data.get('per_level2')}</code>
🗺 <b>Pickup address:</b> <code>{msg.text}</code>
🚒 <b>Any problems with the car ?:</b> <code>{answer_prob}</code>
"""  
    pdf_user= f"""
Date: {(datetime.now()+ timedelta(hours=1)).strftime('%d.%m.%Y %H:%M')}
Driver's name: {data.get('driver_name2')}
Customer name: {data.get('customer_name2')}
Car model: {data.get('car_model2')}
Plate number: {data.get('plate_number2')}
Car odometer: {data.get('car_odometer2')}
Petrol level %: {data.get('per_level2')}
Any problems with the car: {answer_prob}
Pickup address: {msg.text}"""  

    await state.update_data(form_text2=form_user )
    await state.update_data(pdf_text2=pdf_user )
    
    media = MediaGroup()
    media_prob = MediaGroup()
    media_side = MediaGroup()

    #try:
    for file_id in data.get('media_doc'):
        for k, v in file_id.items():
            if k == 'photo':
                media.attach_photo(v, 'Photo documents')
                await bot.download_file_by_id(v, destination_dir='src/delivery_form/media_data')
            elif k == 'video':
                media.attach_video(v, 'Photo documents')
    await state.update_data(media_doc_group= media)
    await msg.answer_media_group(media=media)
    
    for file_id in data.get('media_side'):
        for k, v in file_id.items():
            if k == 'photo':
                media_side.attach_photo(v, 'Car 4 sides photo')
                await bot.download_file_by_id(v, destination_dir='src/delivery_form/media_data')
            elif k == 'video':
                media_side.attach_video(v, 'Car 4 sides photo')
    await state.update_data(media_side_group= media_side)
    await msg.answer_media_group(media=media_side)
    
    if data.get('media_prob') != None:
        for file_id in data.get('media_prob'):
            for k, v in file_id.items():
                if k == 'photo':
                    media_prob.attach_photo(v, 'Photo of the problem')
                    await bot.download_file_by_id(v, destination_dir='src/delivery_form/media_data')
                elif k == 'video':
                    media_prob.attach_video(v, 'Photo of the problem')
        await state.update_data(media_prob_group= media_prob)
        await msg.answer_media_group(media=media_prob)
        
    await msg.answer(
                text=f"{form_user}",
                parse_mode=html,
                reply_markup=accept_menu)
    await Form2.Q12.set()
'''    except Exception as ex:
        print(ex)
        await msg.answer("An error has occurred! Please, take the test again\n\n"
                         +f"Произошла ошибка. Пожалуйста, пройдите тест заного !", reply_markup=main_menu)'''
        #await state.finish()
        
@dp.callback_query_handler(text_contains= 'accept_', state=Form2.Q12)
async def accept_answer(call: CallbackQuery, state: FSMContext):
    if call.data.split('_')[1] == 'accept':
        data= await state.get_data()
        media= data.get('media_doc_group')
        media_side= data.get('media_side_group')

            
        await call.message.answer('Thank for using the bot, requests successfully sent!\n\nСпасибо за использование бота, заявка успешно отправлена!', reply_markup=main_menu)
        await bot.send_message(chat_id=admin_chat_del,
                               text=f"Delivery @{call.message.chat.username}\n"
                               +f"{data.get('form_text2')}",
                               parse_mode=html)
        
        await bot.send_message(chat_id=admin_chat_del,
                               text=f"Photo documents")
        await bot.send_media_group(chat_id=admin_chat_del,
                                   media=media)
        await bot.send_message(chat_id=admin_chat_del,
                               text=f"Photo side car ")
        await bot.send_media_group(chat_id=admin_chat_del,
                                   media=media_side)
        
        if data.get('media_prob_group') != None:
            media_prob= data.get('media_prob_group')
            await bot.send_message(chat_id=admin_chat_del,
                               text=f"Photo problems")
            await bot.send_media_group(chat_id=admin_chat_del,
                                   media=media_prob)
        pdf= FPDF()
        pdf.add_page()
        pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
        pdf.set_font('DejaVu', size=14)
        pdf_user= data.get('pdf_text2')
        new_pdf_user= emoji.demojize(pdf_user)  

        pdf.cell(200, 10, txt=f'Delivery @{call.message.chat.username}', new_x="LMARGIN" , new_y="NEXT", align='C')

        pdf.write(txt= f"{new_pdf_user}", h=10)
        pdf.cell(400, 20, new_x="LMARGIN" , new_y="NEXT", align='L')
        imges= os.listdir('src/delivery_form/media_data/photos')
        for i in imges:
            im= Image.open(f"src/delivery_form/media_data/photos/{i}", "r")
            w, h = im.size
            im.close()
            if w > 100 or h > 100:
                mid_size = (w//100 + h//100) // 2
            else:
                mid_size=1
            pdf.image(
                name=f"src/delivery_form/media_data/photos/{i}",
                w=w // mid_size,
                h=h // mid_size,
            )
        shutil.rmtree('src/delivery_form/media_data/photos')

        pdf.output('delivery.pdf')

        await bot.send_document(chat_id=admin_chat_del,
                                document=open('delivery.pdf', "rb"))
        await state.finish()
    if call.data.split('_')[1] == 'cancel':
        await state.finish()
        await call.message.delete()
        await call.message.answer(text="<b>1.</b> Driver's name ?\n\nИмя водителя ?", parse_mode=html, reply_markup=main_menu)
        await Form2.Q2.set()