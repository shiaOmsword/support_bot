from aiogram.fsm.state import State, StatesGroup

class IntakeFlow(StatesGroup):
    waiting_initial_text = State()
    waiting_role = State()
    waiting_adv_type = State()