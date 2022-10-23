import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from pymongo import MongoClient
from pymongo.server_api import ServerApi

# прочтение конфига
from config import BOT_TOKEN
from handlers import common, create_task, view


# ВОЗМОЖНО ПОФИКСИТЬ КОЛБЭК НА МЕНЮ (ПОВТОРЯЕТ КОМАНДУ)
# СДЕЛАТЬ ПО-ДРУГОМУ КОНФИГ
# ОГРАНИЧЕНИЕ НА ВЫВОД ТАСКОВ ДА И В ОБЩЕМ НА КОЛИЧЕСТВО ТАСКОВ
# ПОФИКСИТЬ БЕЗОПАСНОСТЬ (ЗАКИНУТЬ В КОНФИГ НУЖНОЕ И ЕГО НЕ КИДАТЬ В ГИТХАБ)
# СДЕЛАТЬ ТЕСТ НА РАЗНЫЙ РЕГИСТ В КОМАНДАХ (СЕЙЧАС ЕСТЬ, НО НЕ РАБОТАЕТ)
# ПЕРЕПИСАТЬ CHECH_INT
# ПОФИКСИТЬ КОСТЫЛЬ С LAMBDA НА ФУНКЦИИ ФИЛЬТРОВ В СОЗДАНИИ ЗАДАЧИ


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s - %(message)s \n---------------------------------------------------"
    )

    # создаём Dispatcher и Bot
    dp = Dispatcher(storage=MemoryStorage())
    bot = Bot(BOT_TOKEN)

    # подключение роутеров
    dp.include_router(common.router)
    dp.include_router(create_task.router)
    dp.include_router(view.router)

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    asyncio.run(main())
