from aiogram import Router
from aiogram.filters.text import Text
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from config import tasks
from keyboards.inline_2el_row import make_inline_2el_row_keyboard

router = Router()


class CreateTask(StatesGroup):
    choosing_task_name = State()
    choosing_task_time = State()


# Создание новой задачи
@router.callback_query(Text(text="создать задачу", ignore_case=True))
@router.callback_query(Text(text="создать ещё одну задачу", ignore_case=True))
async def callbacks_create_task(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text="Введите название новой задачи (максимальная длина - 300 символов): "
    )
    await state.set_state(CreateTask.choosing_task_name)


@router.message(CreateTask.choosing_task_name)
async def task_name_chosen(message: Message, state: FSMContext):
    if len(message.text) > 300:
        await message.answer(
            text="Пожалуйста, введите название новой задачи. \n"
                 "Максимальная длина названия - 300 символов."
        )
        return
    await state.update_data(chosen_task_name=message.text)
    await message.answer(
        text="Введите время в минутах, которое необходимо для новой задачи (максимально - 600 минут): "
    )
    await state.set_state(CreateTask.choosing_task_time)


@router.message(CreateTask.choosing_task_time)
async def task_time_chosen(message: Message, state: FSMContext):
    error_time = "Пожалуйста, введите время в минутах, которое необходимо для новой задачи. \n" \
                 "Используйте только целое число, никаких дополнительных символов. Максимально - 600 минут."
    if not message.text.isnumeric():
        await message.answer(text=error_time)
        return
    if int(message.text) > 600:
        await message.answer(text=error_time)
        return
    await message.answer(
        text="Задача успешно сохранена! Можете создать ещё одну задачу по кнопке ниже",
        reply_markup=make_inline_2el_row_keyboard(['Создать ещё одну задачу'])
    )
    created_task = await state.get_data()
    tasks.insert_one({"userID": message.from_user.id, "status": "не отправлено",
                      "taskName": created_task['chosen_task_name'], "taskTime": int(message.text),
                      "resImageID": "не отправлено", "resText": "не отправлено"})

    # Сброс состояния и сохранённых данных у пользователя
    await state.clear()
