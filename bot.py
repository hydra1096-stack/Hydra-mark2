import asyncio
import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram import F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import google.generativeai as genai

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not TOKEN or not GEMINI_API_KEY:
    raise ValueError("TOKEN или GEMINI_API_KEY не найден!")

genai.configure(api_key=GEMINI_API_KEY)

# Новая актуальная модель
model = genai.GenerativeModel('gemini-3.1-flash-lite')

bot = Bot(token=TOKEN)
dp = Dispatcher()

user_modes = {}
user_history = {}

HUMOR_PROMPT = """Ты — дерзкий токсичный русскоязычный мемный приколист 2026 года. Отвечай с матом, стёбом, сарказмом и жёстким юмором."""
WIKI_PROMPT = """Ты — умный и точный помощник. Отвечай подробно, структурировано и по делу."""

def get_mode_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="😂 Юморист-Приколист", callback_data="mode_humor")],
        [InlineKeyboardButton(text="📚 Умный Помощник", callback_data="mode_wiki")]
    ])

@dp.message(Command("start"))
async def start(message: types.Message):
    if message.from_user.id not in user_modes:
        await message.answer("👋 Привет! Выбери режим работы бота:", reply_markup=get_mode_keyboard())
    else:
        await message.answer("✅ Бот готов. Просто пиши сообщения.")

@dp.callback_query(lambda c: c.data.startswith("mode_"))
async def set_mode(callback: types.CallbackQuery):
    mode = "humor" if callback.data == "mode_humor" else "wiki"
    user_modes[callback.from_user.id] = mode
    await callback.message.edit_text("✅ Режим успешно установлен!")
    await callback.answer()

@dp.message(F.text)
async def chat(message: types.Message):
    user_id = message.from_user.id
    
    if user_id not in user_modes:
        await message.answer("Сначала выбери режим:", reply_markup=get_mode_keyboard())
        return

    await message.answer("⏳ Думаю...")

    try:
        system_prompt = HUMOR_PROMPT if user_modes[user_id] == "humor" else WIKI_PROMPT
        full_prompt = f"{system_prompt}\n\nВопрос: {message.text}"
        
        response = model.generate_content(full_prompt)
        answer = response.text
        
        await message.answer(answer)
        
    except Exception as e:
        logging.error(f"Ошибка Gemini: {str(e)}")
        await message.answer("❌ Ошибка соединения с ИИ. Попробуй ещё раз.")

async def main():
    print("✅ Бот с Gemini-2.5-flash запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
