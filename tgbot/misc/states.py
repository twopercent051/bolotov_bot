from aiogram.dispatcher.filters.state import State, StatesGroup

class FSMAdmin(StatesGroup):
    home = State()
    greeting = State()
    how_it_work = State()
    heating = State()
    what_i_need = State()


class FSMUser(StatesGroup):
    home = State()
    year = State()
    height = State()
    weight = State()
    smoking = State()
    drinking = State()
    timezone = State()




