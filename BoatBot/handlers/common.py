from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, IDFilter

markup = types.ReplyKeyboardMarkup(row_width=1)
btn1 = types.KeyboardButton('Показать актуальный фильм')
btn2 = types.KeyboardButton('Добавить новый фильм')
markup.add(btn1, btn2)


async def cmd_start(message: types.Message, state: FSMContext):
    """Realize functionality to start bot"""
    await state.finish()
    await message.answer(
        'Выберите действие:',
        reply_markup=markup
    )

async def cmd_cancel(message: types.Message, state: FSMContext):
    """Cancel all states """
    await state.finish()
    await message.answer("Действие отменено", reply_markup=types.ReplyKeyboardRemove())


def register_handlers_common(dp: Dispatcher):
    """Register handlers"""
    dp.register_message_handler(cmd_start, commands="start", state="*")
    dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
    dp.register_message_handler(cmd_cancel, Text(equals="отмена", ignore_case=True), state="*")