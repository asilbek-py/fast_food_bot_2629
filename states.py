from aiogram.fsm.state import StatesGroup, State

class RegistrationStates(StatesGroup):
    full_name = State()
    phone_number = State()

class CategoryStates(StatesGroup):
    waiting_for_name = State()
    confirmation = State()

class ProductStates(StatesGroup):
    waiting_for_category = State()       # category id or name selection step
    waiting_for_name = State()
    waiting_for_description = State()
    waiting_for_price = State()
    waiting_for_image = State()          # accept photo or URL
    confirmation = State()
