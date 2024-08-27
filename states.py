from aiogram.fsm.state import State, StatesGroup

class UserState():
    id = None,
    first_name = None,
    last_name = None,
    is_premium = None,
    is_bot = None

class ExchangeState(StatesGroup):
    exchange_amount = State()