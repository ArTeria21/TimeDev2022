import asyncio

from aiogram import Router, F
from aiogram.filters.text import Text
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from config import tasks
from handlers.common import get_tasks
from keyboards.inline_2el_row import make_inline_2el_row_keyboard

router = Router()


class ProgressingTask(StatesGroup):
    choosing_task_number = State()
    choosing_result_text = State()
    choosing_result_photo = State()


# Выполнение задачи
@router.callback_query(Text(text="выполнить задачу", ignore_case=True))
@router.callback_query(Text(text="начать выполнение задачи", ignore_case=True))
async def callbacks_complete_task(callback: CallbackQuery, state: FSMContext):
    tasks_text = await get_tasks(callback)
    if tasks_text is None:
        return
    await callback.message.answer(
        text=f"Введите номер задачи, которую хотите выполнить: \n{tasks_text}"
    )
    await state.set_state(ProgressingTask.choosing_task_number)


@router.message(ProgressingTask.choosing_task_number)
async def task_number_chosen(message: Message, state: FSMContext):
    if not message.text.isnumeric():
        await message.answer(text="Укажите номер задачи. Используйте в записи только цифры и числа.")
        return
    global task, task_id
    task_id = int(message.text)
    try:
        task = list(tasks.find({"userID": message.from_user.id}))[task_id - 1]
        task_id = task['_id']
    except IndexError:
        await message.answer(
            text="Пожалуйста, укажите корректный номер задачи. "
        )
        return

    # включение функции таймера
    await message.answer(
        text=f"Я ставлю таймер на {task['taskTime']} минут. Продуктивно поработай!",
        reply_markup=make_inline_2el_row_keyboard(['Завершить работу'])
    )
    tasks.update_one({'_id': task_id}, {"$set": {"status": "работает"}})
    await state.clear()
    await task_time_sleep(message, state)


async def task_time_sleep(message: Message, state: FSMContext):
    await asyncio.sleep(int(task['taskTime']) * 60)
    await message.answer(
        text=f"Время на выполнение задачи {task['taskName']} вышло! "
             f"Теперь тебе нужно составить отчет о проделанной работе. "
             f"Напиши что ты сделал, трудно было или нет. (максимально - 600 символов)"
             f"Этот отчет оценят другие пользователи и тебе будут начислены монеты Focus."
    )
    await state.set_state(ProgressingTask.choosing_result_text)


@router.callback_query(Text(text="завершить работу", ignore_case=True))
async def callbacks_complete_task(callback: CallbackQuery, state: FSMContext):
    try:
        await asyncio.wait_for(task_time_sleep(callback.message, state), timeout=1.0)
    except asyncio.TimeoutError:
        await callback.message.answer(
            text="Отлично! Задача выполнена! Теперь тебе нужно составить отчет о проделанной работе. "
                 "Напиши что ты сделал, трудно было или нет. (максимально - 600 символов) "
                 "Этот отчет оценят другие пользователи и тебе будут начислены монеты Focus."
        )
        await state.set_state(ProgressingTask.choosing_result_text)


@router.message(ProgressingTask.choosing_result_text)
async def task_number_chosen(message: Message, state: FSMContext):
    if len(message.text) > 600:
        await message.answer(
            text="Пожалуйста, введите другой отчёт. \n"
                 "Максимальная длина отчёта - 600 символов."
        )
        return
    await state.update_data(chosen_result_text=message.text)
    await message.answer(
        text="Классно! А теперь приложи ОДНУ фотографию."
    )
    await state.set_state(ProgressingTask.choosing_result_photo)


@router.message(ProgressingTask.choosing_result_photo, F.photo)
async def task_photo_chosen(message: Message, state: FSMContext):
    res = await state.get_data()
    if tasks.find_one({'_id': task_id})['resImageID'] != 'не отправлено':
        return
    tasks.update_one({'_id': task_id}, {"$set": {"resImageID": message.photo[-1].file_id,
                                                 "resText": res['chosen_result_text']}})
    await message.answer(
        text="Отлично! Ваш отчет обязательно проверят! Focoin будут начислены на ваш кошелек"
    )
    await state.clear()


@router.message(ProgressingTask.choosing_result_photo)
async def task_photo_chosen_incorrectly(message: Message):
    await message.answer(
        text="Пожалуйста, приложи фотографии к отчёту!"
    )
