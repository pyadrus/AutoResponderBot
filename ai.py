# from datetime import datetime
#
# from aiogram.types import Message
# # from litellm import completion
# from gigachat import GigaChat
# # from groq import Groq
# from loguru import logger
# from langchain_core.messages import HumanMessage, SystemMessage
# from langchain_gigachat.chat_models import GigaChat
# from settings import secrets
#
#
# def system_prompt(work):
#     """Промт для ИИ"""
#
#     if work == 'Время не рабочее':
#         return """Текущее время является нерабочим. Ваш запрос будет рассмотрен позже. Спасибо за понимание! 🕒📅"""
#     else:
#         return """Сейчас рабочее время. Ваш запрос будет рассмотрен в ближайшее время. 🕐📋"""
#
#
# async def get_chat_completion(message: Message, work):
#     """Возвращает ответ пользователя"""
#
#     # Авторизация в GigaChat
#     llm = GigaChat(credentials=secrets.giga_chat, scope="GIGACHAT_API_PERS", model="GigaChat",
#         # Отключает проверку наличия сертификатов НУЦ Минцифры
#         verify_ssl_certs=False,
#         streaming=False,)
#
#     messages = [SystemMessage(content=system_prompt(work)), HumanMessage(content=message.text),]
#
#     response = llm.invoke(messages)
#     print("GigaChat: ", response.content)
#
#     return response.content
#
# # async def get_chat_completion(message: Message, work):
# #     """Возвращает ответ пользователя"""
# #
# #     # client = Groq(api_key=secrets.openai_key)
# #
# #     # chat_completion = client.chat.completions.create(
# #     #     messages=[
# #     #         {"role": "system", "content": system_prompt(work)},
# #     #         {"role": "user", "content": message.text},
# #     #     ],
# #     #     model="llama3-groq-70b-8192-tool-use-preview",
# #     # )
# #
# #     # return chat_completion.choices[0].message.content
# #
# #     # Авторизация в GigaChat
# #     llm = GigaChat(
# #         credentials=secrets.giga_chat,
# #         scope="GIGACHAT_API_PERS",
# #         model="GigaChat",
# #         # Отключает проверку наличия сертификатов НУЦ Минцифры  pip install gigachain-cli
# #         verify_ssl_certs=False,
# #         streaming=False,
# #     )
# #
# #     messages = [
# #         SystemMessage(
# #             content=system_prompt(work)
# #         )
# #     ]
# #
# #     # return chat_completion.choices[0].message.content
# #
# #     # while (True):
# #     #     user_input = input("Пользователь: ")
# #     #     if user_input == "пока":
# #     #         break
# #     messages.append(HumanMessage(content=work))
# #     res = llm.invoke(messages)
# #     messages.append(res)
# #     print("GigaChat: ", res.content)
# #
# #     return res.content.message.content
#
# async def handle_business_message(message: Message):
#     """
#     Обрабатывает сообщение от пользователя. И проверяет рабочее время или нет. Если рабочее время, то бот отвечает пользователю,
#     Если время не рабочее, то не отвечает.
#     """
#     id_usser = message.from_user.id
#     user_name = message.from_user.username
#
#     logger.info(f"Пользователь ID: {id_usser}. Username {user_name} написал сообщение.")
#
#     # Создаем словарь с рабочим временем
#     working_hours = {
#         "start": {"hour": 8, "minute": 0},  # Начало рабочего дня в 09:00
#         "end": {"hour": 20, "minute": 0},  # Окончание рабочего дня в 18:00
#     }
#
#     # Получаем текущее время
#     current_time = datetime.now()
#     current_hour = current_time.hour
#     current_minute = current_time.minute
#
#     # Проверяем, находится ли текущее время внутри рабочего интервала
#     if (
#             (
#                     current_hour >= working_hours["start"]["hour"]
#                     and current_hour <= working_hours["end"]["hour"]
#             )
#             or (
#             current_hour == working_hours["start"]["hour"]
#             and current_minute >= working_hours["start"]["minute"]
#     )
#             or (
#             current_hour == working_hours["end"]["hour"]
#             and current_minute < working_hours["end"]["minute"]
#     )
#     ):
#         print("Время рабочее")
#         work = "Время рабочее"
#     else:
#         print("Время не рабочее")
#         work = "Время не рабочее"
#
#     answer = await get_chat_completion(message, work)
#     await message.reply(answer)
