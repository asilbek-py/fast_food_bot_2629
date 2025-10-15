from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from database import get_all_categories

def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📂 Menyu"), KeyboardButton(text="🛒 Mening Savatim")],
            [KeyboardButton(text="⚙️ Sozlamalar"), KeyboardButton(text="🏪 Filliallarimiz"), KeyboardButton(text="📞 Aloqa")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Tanlang:"
    )

def admin_main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📂 Menyu"), KeyboardButton(text="🛒 Mening Savatim")],
            [KeyboardButton(text="➕ Category qo'shish"), KeyboardButton(text="🗑️ Category o'chirish")],
            [KeyboardButton(text="➕ Product qo'shish"), KeyboardButton(text="🗑️ Product o'chirish")],
            [KeyboardButton(text="🔙 Orqaga")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Admin:"
    )

def build_category_menu():
    cats = get_all_categories()
    # if no categories, show only back
    buttons = [[KeyboardButton(text=cat[1])] for cat in cats] if cats else []
    buttons += [[KeyboardButton(text="⬅️ Orqaga")]]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, input_field_placeholder="Kategoriya tanlang:")

def build_products_menu(category_id):
    from database import get_products_by_category
    prods = get_products_by_category(category_id)
    buttons = [[KeyboardButton(text=f"{p[1]}")] for p in prods] if prods else []
    buttons += [[KeyboardButton(text="⬅️ Orqaga")]]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, input_field_placeholder="Mahsulot tanlang:")
