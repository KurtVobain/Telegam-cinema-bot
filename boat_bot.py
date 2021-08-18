import pandas as pd

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from BoatBot.config import load_config
from BoatBot.handlers.show_current_film import register_handlers_actual_film
from BoatBot.handlers.add_new_film import register_handlers_films
from BoatBot.handlers.common import register_handlers_common


logger = logging.getLogger(__name__)

# Registration of a commandes, to be shown in Telegram
async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Начать работу с ботом"),
        BotCommand(command="/add", description="Добавить фильм"),
        #BotCommand(command="/random", description="Выбрать случайный фильм"),
        BotCommand(command="/cancel", description="Отменить текущее действие"),
        BotCommand(command="/actual", description="Вывести текущий фильм")
    ]
    await bot.set_my_commands(commands)


async def main():
    # Logging in stdout
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot")

    # Parsing configuration file
    config = load_config("config/bot.ini")

    #Initialize bot and dispatcher 
    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher(bot, storage=MemoryStorage())

    #Handlers registration
    register_handlers_common(dp)#, config.tg_bot.admin_id)
    register_handlers_films(dp)
    register_handlers_actual_film(dp)

    #Set bot's commands
    await set_commands(bot)

    #Start pooling
    # await dp.skip_updates()  # Skip updates (not necessary)
    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(main())