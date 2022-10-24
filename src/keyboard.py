from threading import main_thread
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup



def persent_markup():
    persent_menu= InlineKeyboardMarkup(row_width=3)
    buttons= ['10%', '20%', '30%', '40%', '50%', '60%','70%', '80%', '90%', '100%' ]
    for persent in buttons:
        persent_menu.insert(InlineKeyboardButton(text=persent, callback_data=f'per_{persent}'))

    return persent_menu

problem_markup= InlineKeyboardMarkup(row_width=2)

problem_markup.add(
    InlineKeyboardButton("Yes", callback_data="prob_yes"),
    InlineKeyboardButton("No", callback_data="prob_no")
)

accept_menu= InlineKeyboardMarkup(row_width=2)
accept_menu.add(
    InlineKeyboardButton('✅ Submit', callback_data='accept_accept'),
    InlineKeyboardButton('✏️ Change', callback_data='accept_cancel')
)

next_button = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
next_button.add('Next')

main_button= ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
main_button.add('Pick Up 🆙')