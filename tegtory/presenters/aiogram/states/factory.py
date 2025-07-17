from aiogram.fsm.state import State, StatesGroup


class Create(StatesGroup):
    name = State()


class Rename(StatesGroup):
    new_name = State()
