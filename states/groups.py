# -*- coding: utf-8 -*-
from aiogram.fsm.state import StatesGroup, State


class EnterTime(StatesGroup):
    enter_time = State()


class EnterPrompt(StatesGroup):
    enter_prompt = State()


class EnterKnowledge(StatesGroup):
    enter_knowledge = State()
