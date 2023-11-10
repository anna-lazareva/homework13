import logging
import sys
import asyncio
from os import getenv

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from aiogram.enums import ParseMode
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

bot_token = getenv("ERBAUER_BOT_TOKEN")
if not bot_token:
    exit("Error: no token provided")

# Инициализируем диспетчер
dp = Dispatcher()

# Клавиатура с кнопками
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="/start"),
            KeyboardButton(text="/help"),
        ],
    ],
    resize_keyboard=True, one_time_keyboard=True
)


# Обработчик команды /start
@dp.message(CommandStart())
async def cmd_start(message: Message) -> None:
    """
    Отправляет приветственное сообщение при команде /start
    """
    await message.reply(
        "Привет! 👋 Я твой телеграм-бот. Чтобы начать, просто напиши мне что-нибудь.",
        reply_markup=ReplyKeyboardRemove())
    
    
# Обработчик команды /help
@dp.message(Command("help"))
async def cmd_help(message: Message) -> None:
    """
    Отправляет сообщение с клавиатурой при команде /help
    """
    await message.reply("Вот доступные команды:", reply_markup=keyboard)
    

# Обработчик кнопки "/start"
@dp.message(lambda message: message.text == "/start")
async def cmd_button_1(message: Message) -> None:
    """
    Обработчик нажатия на кнопку "/start"
    """
    await cmd_start(message)
    
    
# Обработчик кнопки "/help"
@dp.message(lambda message: message.text == "/help")
async def cmd_button_2(message: Message) -> None:
    """
    Обработчик нажатия на кнопку "/help"
    """
    await cmd_help(message)
    
    
# Обработчик текстовых сообщений "привет" (регистр не имеет значения)
@dp.message(lambda message: message.text.lower() == 'привет')
async def greet(message: types.Message) -> None:
    """
    Отправляет сообщение "Привет, {username}!"
    """
    await message.answer(f"Привет, {hbold(message.from_user.full_name)}!")


# Обработчик неизвестных команд
@dp.message()
async def echo_handler(message: types.Message) -> None:
    """
    Отвечает на все остальные сообщения, кроме команд /help и "привет"
    """
    await message.answer("Я не понимаю тебя. Попробуй команду /help или напиши 'привет'.")


async def main() -> None:
    bot = Bot(bot_token, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
    