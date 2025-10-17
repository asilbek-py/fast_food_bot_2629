import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from config import API_TOKEN, ADMIN_ID, DB_NAME
from database import create_tables
from handlers import (
    command_start_handler, show_menu_handler,
    add_category_handler, receive_category_name, confirm_category,
    delete_category_start, delete_category_confirm,
    add_product_start, product_receive_category, product_receive_name,
    product_receive_description, product_receive_price, product_receive_image,
    delete_product_start, delete_product_choose_category, delete_product_confirm,
    user_selects_category_show_products, user_selects_product_show_details
)
from aiogram.types import Message

logging.basicConfig(level=logging.INFO)

# ensure DB exists and tables created
create_tables()

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# register handlers
dp.message.register(command_start_handler, CommandStart())
dp.message.register(show_menu_handler, F.text == "📂 Menyu")

# admin category
dp.message.register(add_category_handler, F.text == "➕ Category qo'shish")

# Because we used States, register with StateFilter patterns:
from aiogram.filters import StateFilter
from states import CategoryStates, ProductStates

dp.message.register(receive_category_name, StateFilter(CategoryStates.waiting_for_name))
dp.message.register(confirm_category, StateFilter(CategoryStates.confirmation))

dp.message.register(delete_category_start, F.text == "🗑️ Category o'chirish")
dp.message.register(delete_category_confirm, StateFilter(CategoryStates.waiting_for_name))  # naive: will be triggered for any text; but we will guard inside

# admin product
dp.message.register(add_product_start, F.text == "➕ Product qo'shish")
dp.message.register(product_receive_category, StateFilter(ProductStates.waiting_for_category))
dp.message.register(product_receive_name, StateFilter(ProductStates.waiting_for_name))
dp.message.register(product_receive_description, StateFilter(ProductStates.waiting_for_description))
dp.message.register(product_receive_price, StateFilter(ProductStates.waiting_for_price))
dp.message.register(product_receive_image, StateFilter(ProductStates.waiting_for_image))

dp.message.register(delete_product_start, F.text == "🗑️ Product o'chirish")
dp.message.register(delete_product_choose_category, F.text,  StateFilter(ProductStates.waiting_for_category))  # not ideal but works with guard inside
dp.message.register(delete_product_confirm, StateFilter(ProductStates.confirmation))

# user flow: selecting category and product
dp.message.register(user_selects_category_show_products, F.text)  # will be filtered inside function
dp.message.register(user_selects_product_show_details, F.text)   # same

async def main():
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
