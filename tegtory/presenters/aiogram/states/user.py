from aiogram.fsm.state import State, StatesGroup


class ChangeNick(StatesGroup):
    new_nickname = State()
