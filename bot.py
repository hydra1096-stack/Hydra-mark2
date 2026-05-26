import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram import F

# Получаем токен из переменных окружения
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("Токен не найден! Добавь переменную TOKEN в Railway.")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Команда /start
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "👋 Привет! Я твой бот.\n\n"
        "Просто напиши мне что-нибудь, я отвечу."
    )

# Ответ на любое текстовое сообщение
@dp.message(F.text)
async def echo(message: types.Message):
    await message.answer(f"Ты написал: {message.text}")

# Запуск бота
async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
