from aiogram import Router
from aiogram.filters.command import Command
from aiogram.filters.text import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.inline_2el_row import make_inline_2el_row_keyboard

router = Router()

available_menu_buttons = ['Создать задачу', 'Просмотреть задачи', 'Начать выполнение задачи', 'Кошелёк']


@router.message(Command(commands=["start"], ignore_case=True))
@router.message(Text(text="старт", ignore_case=True))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Приветствую вас! Для того, чтобы узнать возможности бота, введите /menu или фразу 'меню'",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(Command(commands=["menu"], ignore_case=True))
@router.message(Text(text="меню", ignore_case=True))
async def cmd_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Вы находитесь в главном меню бота. Выберите одну из представленных возможностей: ",
        reply_markup=make_inline_2el_row_keyboard(available_menu_buttons)
    )


@router.message(Command(commands=["cancel"], ignore_case=True))
@router.message(Text(text="отмена", ignore_case=True))
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Действие отменено",
        reply_markup=ReplyKeyboardRemove()
    )
