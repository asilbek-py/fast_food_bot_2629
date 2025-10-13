import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.filters import StateFilter

from keyboards import main_menu, category_menu, admin_main_menu
from config import API_TOKEN, ADMIN_ID
from handlers import menu_handler, add_category_handler, receive_category_name, confirm_category
from states import RegistrationStates, CategoryStates, ProductStates
from database import create_tables

dp = Dispatcher()
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)


@dp.message(CommandStart())
async def command_start_handler(message: Message):
    if message.from_user.id in ADMIN_ID:
        await message.answer(f"Assalomu alaykum, Admin {message.from_user.full_name}!", reply_markup=admin_main_menu)
    else:
        await message.answer(f"Assalomu alaykum, {message.from_user.full_name}!", reply_markup=main_menu)


@dp.message(F.text == "📂 Menyu")
async def menu_handler(message: Message):
    await message.answer("Bo'limlardan birini tanlang:", reply_markup=category_menu)
  

async def main():
    dp.message.register(add_category_handler, F.text == "➕ Category qo'shish")
    dp.message.register(receive_category_name, StateFilter(CategoryStates.category_name))
    dp.message.register(confirm_category, StateFilter(CategoryStates.confirmation))
    await dp.start_polling(bot)


if __name__ == "__main__":
    # Fayl manzili aniqlanadi
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(BASE_DIR, "fast_food.db")

    # Ma'lumotlar bazasi fayli mavjud bo'lmasa, yaratamiz
    if not os.path.exists(DB_PATH):
        print("📦 Ma'lumotlar bazasi yaratilmoqda...")
    create_tables()
    print("✅ Jadval(lar) tayyor!")

    asyncio.run(main())
