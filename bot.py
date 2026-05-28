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
model = genai.GenerativeModel('gemini-3.1-flash')

bot = Bot(token=TOKEN)
dp = Dispatcher()

user_modes = {}

# Новый улучшенный промпт для юмора
HUMOR_PROMPT = """Ты — очень остроумный, дерзкий и умный русский ютубер юмористического контента как "Кель'" или "Shapka" или Папич.
Стиль: лёгкий стёб, самоирония, неожиданные панчлайны, актуальный сленг.
Умерено используй мат.
Главное — чтобы было СМЕШНО. Делай сильные, неожиданные панчлайны в конце ответа.
Будь живым, ироничным и чуть токсичным, но с шармом."""

WIKI_PROMPT = """Ты — умный и точный помощник. 
Отвечай подробно, структурировано и по делу. 
Отвечай ТОЛЬКО обычным текстом, БЕЗ Markdown."""

def get_mode_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="😂 Юморист-Приколист", callback_data="mode_humor")],
        [InlineKeyboardButton(text="📚 Умный Помощник", callback_data="mode_wiki")]
    ])

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("👋 Привет! Используй /pitstop чтобы выбрать режим.")

@dp.message(Command("pitstop"))
async def pitstop(message: types.Message):
    await message.answer("🔄 Выбери режим:", reply_markup=get_mode_keyboard())

@dp.callback_query(lambda c: c.data.startswith("mode_"))
async def set_mode(callback: types.CallbackQuery):
    mode = "humor" if callback.data == "mode_humor" else "wiki"
    user_modes[callback.from_user.id] = mode
    mode_name = "😂 Приколист" if mode == "humor" else "📚 Умный"
    await callback.message.edit_text(f"✅ Режим: <b>{mode_name}</b>", parse_mode="HTML")
    await callback.answer()

@dp.message(F.text)
async def chat(message: types.Message):
    user_id = message.from_user.id
    
    if user_id not in user_modes:
        await message.answer("Сначала выбери режим: /pitstop", reply_markup=get_mode_keyboard())
        return

    await message.answer("⏳ Думаю...")

    try:
        system_prompt = HUMOR_PROMPT if user_modes[user_id] == "humor" else WIKI_PROMPT
        full_prompt = f"{system_prompt}\n\nВопрос: {message.text}"
        
        response = model.generate_content(full_prompt)
        answer = response.text.strip()
        
        await message.answer(answer)
        
    except Exception as e:
        logging.error(f"Ошибка: {e}")
        await message.answer("❌ Ошибка ИИ. Попробуй ещё раз.")

async def main():
    print("✅ Бот запущен (улучшенный юмор)")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
