from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from database import get_all_categories

admin_main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📂 Menyu"),
            KeyboardButton(text="🛒 Mening Savatim")
        ],
        [
            KeyboardButton(text="➕ Category qo'shish"),
            KeyboardButton(text="🗑️ Category o'chirish")
        ],
        [
            KeyboardButton(text="➕ Product qo'shish"),
            KeyboardButton(text="🗑️ Product o'chirish")  
        ],
        [
            KeyboardButton(text="🔙 Orqaga")
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Tanlang:"
)

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📂 Menyu"),
            KeyboardButton(text="🛒 Mening Savatim")
        ],
        [
            KeyboardButton(text="⚙️ Sozlamalar"),
            KeyboardButton(text="🏪 Filliallarimiz"),
            KeyboardButton(text="📞 Aloqa")
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Tanlang:"
)


category_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=category[1])] for category in get_all_categories()
    ] + [[KeyboardButton(text="⬅️ Orqaga")]],
    resize_keyboard=True,
    input_field_placeholder="Kategoriya tanlang:"
)