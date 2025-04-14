from aiogram.fsm.state import StatesGroup, State


class LanguageState(StatesGroup):
    language = State()

class MenuState(StatesGroup):
    menu = State()



class Messeage(StatesGroup):
    rating = State()
    opinion=State()
    objective=State()
    photo=State()
    accept=State()

