import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram import F

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("TOKEN не найден! Добавь его в Variables на Railway.")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# ==================== КОМАНДЫ ====================

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "👋 Привет! Я твой бот.\n\n"
        "Напиши /help, чтобы увидеть все команды."
    )

@dp.message(Command("help"))
async def help_command(message: types.Message):
    await message.answer(
        "📋 <b>Доступные команды:</b>\n\n"
        "/start — Приветствие\n"
        "/help — Показать это сообщение\n\n"
        "Просто пиши текст — я отвечу.",
        parse_mode="HTML"
    )

# Ответ на любое текстовое сообщение
@dp.message(F.text)
async def echo(message: types.Message):
    if message.text.startswith('/'):
        return  # Игнорируем неизвестные команды
    await message.answer(f"Ты написал: {message.text}")

# ================================================

async def main():
    print("✅ Бот успешно запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
