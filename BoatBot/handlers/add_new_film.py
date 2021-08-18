from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, IDFilter
from aiogram.dispatcher.filters.state import State, StatesGroup


class AddFilm(StatesGroup):
	waiting_for_film_name = State()
	waiting_for_film_director = State()
	waiting_for_film_year = State()
	waiting_for_user_name = State()


async def add_film_name(message: types.Message):
	"""Ask for a film's name"""
	await message.answer('Введите название фильма:', reply_markup=types.ReplyKeyboardRemove())
	await AddFilm.waiting_for_film_name.set()


async def film_name_choosen(message: types.Message, state: FSMContext):
	#Save film's name in a dict with key "chosen_film_name"
	await state.update_data(chosen_film_name=message.text.lower())

	#Ask for the film's director 
	await AddFilm.next()
	await message.answer('Введите имя режиссера:')


async def film_director_choosen(message: types.Message, state: FSMContext):
	#Save film's director in the dict with key "chosen_film_director"
	await state.update_data(chosen_film_director=message.text.lower())
	
	#Ask for the film's year
	await AddFilm.next()
	await message.answer('Введите год выхода фильма:')


async def film_year_choosen(message: types.Message, state: FSMContext):
	#Save film's year in the dict with key "chosen_film_year"
	await state.update_data(chosen_film_year=message.text.lower())
	
	#Ask for the user's name
	await AddFilm.next()
	await message.answer('Введите Ваше имя:')


async def user_name_choosen(message: types.Message, state: FSMContext):
	#Save user's name in the dict with key "chosen_user_name"
	await state.update_data(chosen_user_name=message.text.lower())
	#Save status of the film
	await state.update_data(status='Не просмотрен')

	
	"""Add row to the dataframe"""
	#Get data(dict) from the FSM
	film_data = await state.get_data()

	#Inform about adding succes
	await message.answer(f"Фильм добавлен:\n {film_data.get('chosen_film_name')}, {film_data.get('chosen_film_director')}, {film_data.get('chosen_film_year')}, {film_data.get('chosen_user_name')}")

	#Reset state and data
	await state.finish()



def register_handlers_films(dp: Dispatcher):
	"""Register handlers"""
	dp.register_message_handler(add_film_name, commands='add', state="*")
	dp.register_message_handler(add_film_name, Text(equals='добавить новый фильм', ignore_case=True), state="*")
	dp.register_message_handler(film_name_choosen, state=AddFilm.waiting_for_film_name)
	dp.register_message_handler(film_director_choosen, state=AddFilm.waiting_for_film_director)
	dp.register_message_handler(film_year_choosen, state=AddFilm.waiting_for_film_year)
	dp.register_message_handler(user_name_choosen, state=AddFilm.waiting_for_user_name)