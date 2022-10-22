import asyncio
import logging
from pymongo import MongoClient

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from pymongo.server_api import ServerApi

# прочтение конфига
from config_reader import config
from handlers import common, create_task, view, ordering_food


# подключение базы данных
conn_str = "mongodb+srv://timeDev:timeDevPassword@timedev22.gxnyxls.mongodb.net/?retryWrites=true&w=majority"
# даётся 5 секунд на подключение
client = MongoClient(conn_str, server_api=ServerApi('1'), serverSelectionTimeoutMS=5000)
try:
    print(client.server_info())
except Exception:
    print("Не удалось подключиться к серверу MongoDB")
    exit()
db = client['data']
tasks = db['tasks']


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
    bot = Bot(config.bot_token.get_secret_value())

    # подключение роутеров
    dp.include_router(common.router)
    dp.include_router(create_task.router)
    dp.include_router(view.router)
    dp.include_router(ordering_food.router)

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    asyncio.run(main())
