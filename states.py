from aiogram.fsm.state import StatesGroup, State


class RegistrationStates(StatesGroup):
    full_name = State()
    phone_number = State()

class CategoryStates(StatesGroup):
    category_name = State()
    confirmation = State()

class ProductStates(StatesGroup):
    category = State()
    product_name = State()
    description = State()
    price = State()
    image = State()
    confirmation = State()