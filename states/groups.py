# -*- coding: utf-8 -*-
from aiogram.fsm.state import StatesGroup, State


class FormeditMainMenu(StatesGroup):
    text_edit_main_menu = State()


class SettingsClass(StatesGroup):
    setting_start_hour = State()
    setting_start_minute = State()
    setting_end_hour = State()
    setting_end_minute = State()


class EnterPrompt(StatesGroup):
    enter_prompt = State()

