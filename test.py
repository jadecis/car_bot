from fpdf import FPDF
from datetime import date
import os
from PIL import Image


pdf= FPDF()
pdf.add_page()
pdf.add_font('DejaVu', '' ,'font/DejaVuSans.ttf', uni=True )
pdf.set_font('DejaVu', size=14)

pdf_user= f"""
Driver's name: Artem
Customer name: Artem
Car model: BMW
Plate number: 12213
Car odometer: 132321321
Petrol level %: 70%
Any problems with the car: Yes
Pickup address: st ret

"""  


pdf.cell(200, 10, txt=f'Pick up @jadeciss', ln=1 ,align='C')

pdf.write(txt= f"Date: {date.today()} {pdf_user}", h=10)
imges= os.listdir('media_data')
for i in imges:
    im= Image.open(f"media_data\{i}")
    wi, hi = im.size
    mid_size = (wi/100 + hi/100) // 2
    pdf.image(
        name=f"media_data\{i}",
        w=wi/mid_size,
        h=hi/mid_size
    )
pdf.output('Pick up.pdf')