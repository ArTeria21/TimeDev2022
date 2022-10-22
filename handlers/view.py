from aiogram import Router
from aiogram.filters.text import Text
from aiogram.types import CallbackQuery

from keyboards.inline_row import make_inline_keyboard

router = Router()


# Просмотр задач
@router.callback_query(Text(text="просмотреть задачи", ignore_case=True))
async def callbacks_check_tasks(callback: CallbackQuery):
    # ОГРАНИЧЕНИЕ НА ВЫВОД ТАСКОВ, ДА И В ОБЩЕМ НА КОЛИЧЕСТВО ТАСКОВ
    tasks = [{"name": "idu", "time": "45"}, {"name": "idu2", "time": "10"}]
    # ВЗЯТЬ С БД
    if tasks is None:
        await callback.message.answer(
            text="Ты пока не поставил никаких задач! Давай создадим новую!",
            reply_markup=make_inline_keyboard(['Создать задачу'])
        )
        return
    tasks_text = ''.join([f'{taskID}) {task["name"]} - займёт {task["time"]} минут \n'
                          for taskID, task in zip(range(1, len(tasks) + 1), tasks)])
    await callback.message.answer(
        text=f"   Список задач на день: \n{tasks_text}",
        reply_markup=make_inline_keyboard(['Выполнить задачу', 'Меню'])
    )


# Просмотр кошелька
@router.callback_query(Text(text="кошелёк", ignore_case=True))
@router.callback_query(Text(text="кошелек", ignore_case=True))
async def callbacks_check_wallet(callback: CallbackQuery):
    # ПРИКРУТИТЬ МОНЕТУ И БД
    balance = 10
    rating_position = 4
    users = [{"name": "idk1", "balance": 1}, {"name": "idk2", "balance": 45},
             {"name": "idk3", "balance": 17}, {"name": "idk4", "balance": 2},
             {"name": "idk5", "balance": 46}, {"name": "idk6", "balance": 5}]
    rating_list = ''.join([f'{ratingID}) {user["name"]} - {user["balance"]} монет \n'
                           for ratingID, user in zip(range(1, 4), users[0:3])])
    await callback.message.answer(
        text=f"Ваш баланс: {balance} \n"
             f"Твоя позиция в рейтинге: {rating_position} \n"
             f"Чтобы заработать больше монет и поднять рейтинг выполняй больше задач, "
             f"пиши более развернутые отчеты и зарабатывай! \n"
             f"   Топ рейтинга: \n{rating_list}"
    )
