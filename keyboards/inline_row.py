from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton


def make_inline_keyboard(texts: list[str]) -> InlineKeyboardMarkup:
    """
    Создаёт реплай-клавиатуру с кнопками в один ряд
    :param items: список текстов для кнопок
    :return: объект реплай-клавиатуры
    """
    inline_row = [InlineKeyboardButton(text=text, callback_data=text) for text in texts]
    return InlineKeyboardMarkup(inline_keyboard=[inline_row])
