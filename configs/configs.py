# -*- coding: utf-8 -*-
import os

from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()


def get_telegram_admin_id() -> str:
    """Возвращает ID администратора Telegram бота."""
    return os.getenv("ADMIN_ID")


def get_groq_api_key() -> str:
    """Возвращает API-ключ для Groq."""
    return os.getenv("GROQ_API_KEY")


def get_telegram_bot_token() -> str:
    """Возвращает токен Telegram бота."""
    return os.getenv("TELEGRAM_BOT_TOKEN")


# Настройки прокси
def get_proxy_user() -> str:
    """Возвращает логин для прокси."""
    return os.getenv("USER")


def get_proxy_password() -> str:
    """Возвращает пароль для прокси."""
    return os.getenv("PASSWORD")


def get_proxy_port() -> str:
    """Возвращает порт для прокси."""
    return os.getenv("PORT")


def get_proxy_ip() -> str:
    """Возвращает IP для прокси."""
    return os.getenv("IP")


if __name__ == '__main__':
    get_groq_api_key()
    get_telegram_bot_token()
    get_proxy_user()
    get_proxy_password()
    get_proxy_port()
    get_proxy_ip()
