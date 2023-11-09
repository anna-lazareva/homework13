import logging
import sys
import asyncio
from os import getenv
import time

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from aiogram.enums import ParseMode

import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

req = urllib3.requests.post(url, verify=False)


bot_token = getenv("ERBAUER_BOT_TOKEN")
if not bot_token:
    exit("Error: no token provided")

# Инициализируем диспетчер
dp = Dispatcher()


# Обработчик команды /start
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    Отправляет приветственное сообщение при команде /start
    """
    await message.answer(
        "Привет! Я твой телеграм-бот. Чтобы начать, просто напиши мне что-нибудь.")


# Обработчик текстовых сообщений "привет" (регистр не имеет значения)
@dp.message(lambda message: message.text.lower() == 'привет')
async def greet(message: types.Message):
    """
    Отправляет сообщение "Привет, {username}!"
    """
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")
    
    
# Обработчик команды /ban
@dp.message(Command('ban'))
async def ban_user(message: types.Message):
    user_id = message.reply_to_message.from_user.id
    await message.chat.restrict(user_id, until_date=int(time.time()) + 60)
    await message.answer(f"Пользователь {user_id} has been banned for 1 minute.")


# Обработчик неизвестных команд
@dp.message()
async def echo_handler(message: types.Message) -> None:
    """
    Отвечает на все остальные сообщения, кроме команд /start и "привет"
    """
    await message.answer("Я не понимаю тебя. Попробуй команду /start или напиши 'привет'.")


async def main() -> None:
    bot = Bot(bot_token, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
    