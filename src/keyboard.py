from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

start_markup= InlineKeyboardMarkup()
start_markup.add(InlineKeyboardButton("НАЧАТЬ", callback_data="start"))


def persent_markup():
    persent_menu= InlineKeyboardMarkup(row_width=3)
    buttons= ['10%', '20%', '30%', '40%', '50%', '60%','70%', '80%', '90%', '100%' ]
    for persent in buttons:
        persent_menu.insert(InlineKeyboardButton(text=persent, callback_data=f'per_{persent}'))

    return persent_menu

problem_markup= InlineKeyboardMarkup(row_width=2)

problem_markup.add(
    InlineKeyboardButton("Да", callback_data="prob_yes"),
    InlineKeyboardButton("Нет", callback_data="prob_no")
)