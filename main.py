import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
# стратегии - если понадобятся
# from aiogram.fsm.strategy import FSMStrategy

# прочтение конфига
from config_reader import config
from handlers import common, create_task, view, ordering_food


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

    dp.include_router(common.router)
    dp.include_router(create_task.router)
    dp.include_router(view.router)
    dp.include_router(ordering_food.router)

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    asyncio.run(main())
