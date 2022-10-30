from aiogram.types import Message
from loader import dp, html
from aiogram.dispatcher.filters import CommandStart
from src.keyboard import main_menu
from aiogram.dispatcher import FSMContext
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from PIL import Image



def send_email(title, filename, file_path = None , header= None, ):
    password= "prtzqbnxpmvdlmub"
    sender= "royaldreamreports@gmail.com"
    recipient= "magicslesh@gmail.com"#forms@royaldream.ae
    message= MIMEMultipart()
    message["From"]= sender
    message["To"]= recipient
    message["Subject"]= header
    message.attach(MIMEText(f"{title}"))
    
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    try:
        server.login(sender, password)
        
        with open(f"{file_path}", "rb") as f:
            file= MIMEApplication(f.read(), 'pdf')
        file.add_header('content-disposition', 'attachment', filename=f'{filename}')
        message.attach(file)
        server.sendmail(from_addr=sender,
                        to_addrs=recipient,
                        msg=message.as_string())
    except Exception as ex:
        print(ex)

def add_imges_pdf(list_imges, file_pdf, path):
    for i in list_imges:
        file_pdf.cell(200, 10, new_x="LMARGIN" , new_y="NEXT", align='L')
        
        im= Image.open(f"{path}/{i}", "r")
        w, h = im.size
        im.close()
        if w > 100 or h > 100:
            mid_size = (w//100 + h//100) // 2
        else:
            mid_size=1
        file_pdf.image(
            name=f"{path}/{i}",
            w=w // mid_size,
            h=h // mid_size
        )

    


@dp.message_handler(CommandStart(), state="*")
@dp.message_handler(CommandStart())
async def start_command(msg: Message, state: FSMContext):
    await state.finish()
    #send_email(title="123")
    print(msg.chat.id)
    await msg.answer(text= f"Привет, @{msg.chat.username} !\n\n"
                     +f"Этот бот, компании <b>Royal Dream 🚗</b>, принимает анкеты от водителей 👨\n"
                     +f"<i>Просто отвечайте на вопросы бота и следуйте его командам!\nЧтобы пройти анкетирование выбирете форму !</i>",
                     reply_markup=main_menu,
                     parse_mode=html)
    
    
