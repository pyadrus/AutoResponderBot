# -*- coding: utf-8 -*-
import os

from dotenv import load_dotenv

from configs.configs import get_proxy_user, get_proxy_password, get_proxy_port, get_proxy_ip

load_dotenv()  # Загружаем переменные окружения из файла .env


def setup_proxy():
    # Указываем прокси для HTTP и HTTPS
    os.environ['http_proxy'] = f"http://{get_proxy_user()}:{get_proxy_password()}@{get_proxy_ip()}:{get_proxy_port()}"
    os.environ['https_proxy'] = f"http://{get_proxy_user()}:{get_proxy_password()}@{get_proxy_ip()}:{get_proxy_port()}"


if __name__ == '__main__':
    setup_proxy()
