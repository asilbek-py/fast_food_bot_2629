import logging
from aiogram import Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart
from aiogram import F

from config import API_TOKEN, ADMIN_ID
from keyboards import main_menu, admin_main_menu, build_category_menu, build_products_menu
from database import (
    get_all_categories, add_category, delete_category_by_name,
    add_product, get_products_by_category, get_product_by_name_and_category, get_product_by_id, delete_product_by_name
)
from states import CategoryStates, ProductStates

bot = Bot(token=API_TOKEN)

# /start handler
async def command_start_handler(message: Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer(f"Assalomu alaykum, Admin {message.from_user.full_name}!", reply_markup=admin_main_menu())
    else:
        await message.answer(f"Assalomu alaykum, {message.from_user.full_name}!", reply_markup=main_menu())

# Show categories
async def show_menu_handler(message: Message, state: FSMContext):
    # show dynamic category keyboard
    await message.answer("Bo'limlardan birini tanlang:", reply_markup=build_category_menu())

# Admin: start add category
async def add_category_handler(message: Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        await message.answer("Siz admin emassiz.")
        return
    await message.answer("Yangi category nomini kiriting:")
    await state.set_state(CategoryStates.waiting_for_name)

# Receive category name
async def receive_category_name(message: Message, state: FSMContext):
    name = message.text.strip()
    await state.update_data(category_name=name)
    await message.answer(f"🆕 Category nomi: {name}\nTasdiqlaysizmi? (Ha/Yo'q)")
    await state.set_state(CategoryStates.confirmation)

# Confirm category
async def confirm_category(message: Message, state: FSMContext):
    text = message.text.lower()
    data = await state.get_data()
    name = data.get("category_name")
    if text in ("ha", "ha."):
        add_category(name)
        await message.answer(f"✅ Category '{name}' muvaffaqiyatli qo'shildi!", reply_markup=admin_main_menu())
        await state.clear()
    elif text in ("yo'q", "yoq", "yo'q."):
        await message.answer("❌ Category qo'shish bekor qilindi.", reply_markup=admin_main_menu())
        await state.clear()
    else:
        await message.answer("Iltimos, faqat 'Ha' yoki 'Yo'q' deb javob bering.")

# Admin: delete category
async def delete_category_start(message: Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        await message.answer("Siz admin emassiz.")
        return
    cats = get_all_categories()
    if not cats:
        await message.answer("Hozircha category yo'q.", reply_markup=admin_main_menu())
        return
    keyboard = build_category_menu()
    await message.answer("O'chirish uchun category tanlang:", reply_markup=keyboard)
    await state.set_state(CategoryStates.waiting_for_name)

async def delete_category_confirm(message: Message, state: FSMContext):
    name = message.text
    # avoid deleting "⬅️ Orqaga"
    if name == "⬅️ Orqaga":
        await message.answer("Bekor qilindi.", reply_markup=admin_main_menu())
        return
    delete_category_by_name(name)
    await message.answer(f"✅ Category '{name}' o'chirildi.", reply_markup=admin_main_menu())

# Admin: add product flow
async def add_product_start(message: Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        await message.answer("Siz admin emassiz.")
        return
    cats = get_all_categories()
    if not cats:
        await message.answer("Avval category qo'shing.", reply_markup=admin_main_menu())
        return
    # ask to choose category by name
    text = "Qaysi category ga product qo'shmoqchisiz? Iltimos category nomini yozing:"
    await message.answer(text, reply_markup=build_category_menu())
    await state.set_state(ProductStates.waiting_for_category)

async def product_receive_category(message: Message, state: FSMContext):
    # message.text should be category name
    category_name = message.text.strip()
    # find category id
    cats = get_all_categories()
    cat_map = {c[1]: c[0] for c in cats}
    if category_name not in cat_map:
        await message.answer("Noto'g'ri category nomi. Qaytadan tanlang.", reply_markup=build_category_menu())
        return
    await state.update_data(category_id=cat_map[category_name])
    await message.answer("Mahsulot nomini kiriting:")
    await state.set_state(ProductStates.waiting_for_name)

async def product_receive_name(message: Message, state: FSMContext):
    await state.update_data(product_name=message.text.strip())
    await message.answer("Mahsulot tavsifini kiriting:")
    await state.set_state(ProductStates.waiting_for_description)

async def product_receive_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text.strip())
    await message.answer("Mahsulot narxini (so'm) kiriting (raqam):")
    await state.set_state(ProductStates.waiting_for_price)

async def product_receive_price(message: Message, state: FSMContext):
    text = message.text.strip()
    if not text.isdigit():
        await message.answer("Iltimos narxni raqam sifatida kiriting (masalan: 25000).")
        return
    await state.update_data(price=int(text))
    await message.answer("Mahsulot rasmiga URL yuboring yoki rasmini yuboring (foto):")
    await state.set_state(ProductStates.waiting_for_image)

async def product_receive_image(message: Message, state: FSMContext):
    data = await state.get_data()
    category_id = data["category_id"]
    name = data["product_name"]
    description = data["description"]
    price = data["price"]
    image_url = None
    image_file_id = None

    # If user sent a photo
    if message.photo:
        # take the biggest size
        file_id = message.photo[-1].file_id
        image_file_id = file_id
    else:
        # treat text as URL
        maybe_url = message.text.strip()
        if maybe_url.startswith("http://") or maybe_url.startswith("https://"):
            image_url = maybe_url
        else:
            # if user wrote something else
            await message.answer("Iltimos rasm yuboring yoki valid URL yozing.")
            return

    # save product
    add_product(category_id, name, description, price, image_url=image_url, image_file_id=image_file_id)
    await message.answer(f"✅ Mahsulot '{name}' qo'shildi!", reply_markup=admin_main_menu())
    await state.clear()

# Admin: delete product
async def delete_product_start(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("Siz admin emassiz.")
        return
    cats = get_all_categories()
    if not cats:
        await message.answer("Hozircha category yo'q.", reply_markup=admin_main_menu())
        return
    await message.answer("Qaysi category ichidan product o'chirmoqchisiz? Tanlang:", reply_markup=build_category_menu())

async def delete_product_choose_category(message: Message, state: FSMContext):
    category_name = message.text.strip()
    cats = get_all_categories()
    cat_map = {c[1]: c[0] for c in cats}
    if category_name not in cat_map:
        await message.answer("Noto'g'ri category nomi.", reply_markup=admin_main_menu())
        return
    cid = cat_map[category_name]
    # show products
    prods = get_products_by_category(cid)
    if not prods:
        await message.answer("Bu category da mahsulot yo'q.", reply_markup=admin_main_menu())
        return
    buttons = [[KeyboardButton(text=p[1])] for p in prods]  # reuse KeyboardButton
    buttons += [[KeyboardButton(text="⬅️ Orqaga")]]
    from aiogram.types import ReplyKeyboardMarkup
    markup = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    await state.update_data(delete_category_id=cid)
    await message.answer("Qaysi product o'chirilishini tanlang:", reply_markup=markup)
    await state.set_state(ProductStates.confirmation)

async def delete_product_confirm(message: Message, state: FSMContext):
    product_name = message.text.strip()
    if product_name == "⬅️ Orqaga":
        await message.answer("Bekor qilindi.", reply_markup=admin_main_menu())
        await state.clear()
        return
    delete_product_by_name(product_name)
    await message.answer(f"✅ Product '{product_name}' o'chirildi.", reply_markup=admin_main_menu())
    await state.clear()

# User selects a category -> show products
async def user_selects_category_show_products(message: Message, state: FSMContext):
    # message.text is category name
    category_name = message.text.strip()
    cats = get_all_categories()
    cat_map = {c[1]: c[0] for c in cats}
    if category_name not in cat_map:
        # ignore other texts
        return
    cid = cat_map[category_name]
    prods = get_products_by_category(cid)
    if not prods:
        await message.answer("Bu kategoriyada mahsulotlar mavjud emas.", reply_markup=build_category_menu())
        return
    # build product keyboard
    from keyboards import build_products_menu
    await state.update_data(last_category_id=cid)
    await message.answer(f"📦 {category_name} bo'limidagi mahsulotlar:", reply_markup=build_products_menu(cid))

# User selects a product -> show details
async def user_selects_product_show_details(message: Message, state: FSMContext):
    prod_name = message.text.strip()
    data = await state.get_data()
    cid = data.get("last_category_id")
    if not cid:
        # no category context, ignore
        return
    product = get_product_by_name_and_category(prod_name, cid)
    if not product:
        return
    prod_id, name, description, price, image_url, image_file_id = product
    caption = f"📌 <b>{name}</b>\n\n💰 Narx: {price} so'm\n\n📝 Tavsif:\n{description}"
    # if we have file_id, send photo by file_id
    if image_file_id:
        await bot.send_photo(chat_id=message.chat.id, photo=image_file_id, caption=caption, parse_mode="HTML")
    elif image_url:
        await bot.send_photo(chat_id=message.chat.id, photo=image_url, caption=caption, parse_mode="HTML")
    else:
        await message.answer(caption, parse_mode="HTML")
