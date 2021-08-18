import os

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, IDFilter
from aiogram.dispatcher.filters.state import State, StatesGroup

import pandas as pd

film_database = pd.read_csv(r'C:\py\Telegram bots\film bot\Data\film_database.csv')

"""Shows current film and info"""
async def show_current_film(message: types.Message):
	#Get from database name of the film with mark "Actual"
	current_film = film_database['Название'][film_database['Статус'] == 'Актуальный'].to_numpy()
	await message.reply(f'Нужно посмотреть: {current_film[0]}')


"""Register function if we dont use decorator(@)"""
def register_handlers_actual_film(dp: Dispatcher):
	dp.register_message_handler(show_current_film, commands='actual')
	dp.register_message_handler(show_current_film, Text(equals="показать актуальный фильм", ignore_case=True), state="*")