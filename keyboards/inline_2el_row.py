from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton


def make_inline_2el_row_keyboard(texts: list[str]) -> InlineKeyboardMarkup:
    """
    Создаёт реплай-клавиатуру с кнопками в один ряд
    :param items: список текстов для кнопок
    :return: объект реплай-клавиатуры
    """
    inline_buttons = [InlineKeyboardButton(text=text, callback_data=text) for text in texts]
    inline_rows = [[i, j] for i, j in zip(inline_buttons[0::2], inline_buttons[1::2])]
    return InlineKeyboardMarkup(inline_keyboard=inline_rows)
