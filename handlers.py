from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states import CategoryStates
from keyboards import category_menu
from database import add_category

async def menu_handler(message: Message):
    await message.answer("Bo'limlardan birini tanlang:", reply_markup=category_menu)


async def add_category_handler(message: Message, state: FSMContext):
    await message.answer("Yangi category nomini kiriting:")
    await state.set_state(CategoryStates.category_name)  # ✅ to‘g‘ri yo‘l


async def receive_category_name(message: Message, state: FSMContext):
    category_name = message.text
    await state.update_data(category_name=category_name)
    await message.answer(f"🆕 Category nomi: {category_name}\nTasdiqlaysizmi? (Ha/Yo‘q)")
    await state.set_state(CategoryStates.confirmation)  # ✅ to‘g‘ri yo‘l


async def confirm_category(message: Message, state: FSMContext):
    confirmation = message.text.lower()
    data = await state.get_data()
    category_name = data.get("category_name")

    if confirmation == "ha":
        add_category(category_name)
        await message.answer(
            f"✅ Category '{category_name}' muvaffaqiyatli qo‘shildi!",
            reply_markup=category_menu
        )
        await state.clear()
    elif confirmation == "yo‘q":
        await message.answer("❌ Category qo‘shish bekor qilindi.", reply_markup=category_menu)
        await state.clear()
    else:
        await message.answer("Iltimos, faqat 'Ha' yoki 'Yo‘q' deb javob bering.")
