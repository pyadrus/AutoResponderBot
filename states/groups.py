# -*- coding: utf-8 -*-
from aiogram.fsm.state import StatesGroup, State


class EnterPrompt(StatesGroup):
    enter_prompt = State()
