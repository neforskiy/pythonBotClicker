from aiogram.fsm.state import State, StatesGroup

class State():
    id = None,
    first_name = None,
    last_name = None,
    is_premium = None,
    is_bot = None

class UserState(StatesGroup):
    exchange_amount = State()