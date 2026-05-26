import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram import F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import google.generativeai as genai

TOKEN = os.getenv("TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not TOKEN:
    raise ValueError("TOKEN не найден!")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY не найден!")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')  # хорошая и быстрая модель

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Хранилище режима и истории
user_modes = {}     # user_id: "humor" или "wiki"
user_history = {}   # user_id: список сообщений

# ==================== ПРОМПТЫ ====================

HUMOR_PROMPT = """Ты — дерзкий, токсичный и очень смешной русскоязычный приколист 2026 года.
Отвечай с матом, стёбом, актуальным сленгом, иронией и жёстким юмором. Не стесняйся быть пошлым и злым, если это уместно. Главное — чтобы было смешно."""

WIKI_PROMPT = """Ты — высокоинтеллектуальный помощник. Отвечай максимально точно, структурировано и информативно.
Используй списки, выделения и чёткую структуру, когда это нужно."""

def get_mode_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="😂 Юморист-Приколист", callback_data="mode_humor")],
        [InlineKeyboardButton(text="Умный Помощник", callback_data="mode_wiki")]
    ])

@dp.message(Command("start"))
async def start(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_modes:
        await message.answer(
            "👋 Привет! Добро пожаловать в бота.\n\n"
            "Выбери режим, в котором я буду отвечать:",
            reply_markup=get_mode_keyboard()
        )
    else:
        mode_name = "😂 Приколист" if user_modes[user_id] == "humor" else "Умный"
        await message.answer(f"Сейчас ты в режиме: <b>{mode_name}</b>\n\nНапиши что-нибудь!", parse_mode="HTML")

@dp.callback_query(lambda c: c.data.startswith("mode_"))
async def set_mode(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    mode = "humor" if callback.data == "mode_humor" else "wiki"
    user_modes[user_id] = mode
    user_history[user_id] = []  # сбрасываем историю при смене режима
    
    mode_name = "😂 Юморист-Приколист" if mode == "humor" else "Умный Помощник"
    await callback.message.edit_text(f"✅ Режим изменён на: <b>{mode_name}</b>", parse_mode="HTML")
    await callback.answer()

@dp.message(Command("humor"))
async def set_humor(message: types.Message):
    user_modes[message.from_user.id] = "humor"
    user_history[message.from_user.id] = []
    await message.answer("😂 Режим Приколист активирован!")

@dp.message(Command("wiki"))
async def set_wiki(message: types.Message):
    user_modes[message.from_user.id] = "wiki"
    user_history[message.from_user.id] = []
    await message.answer("Режим Умный Помощник активирован!")

@dp.message(F.text)
async def chat(message: types.Message):
    user_id = message.from_user.id
    
    if user_id not in user_modes:
        await message.answer("Сначала выбери режим:", reply_markup=get_mode_keyboard())
        return

    await message.answer("⏳ Думаю...")

    try:
        # Выбираем промпт
        system_prompt = HUMOR_PROMPT if user_modes[user_id] == "humor" else WIKI_PROMPT
        
        # История диалога
        if user_id not in user_history:
            user_history[user_id] = []
        
        user_history[user_id].append({"role": "user", "parts": [message.text]})
        
        # Формируем чат
        chat = model.start_chat(history=[])
        response = chat.send_message(f"{system_prompt}\n\nПользователь: {message.text}")
        
        answer = response.text
        
        # Сохраняем ответ в историю
        user_history[user_id].append({"role": "model", "parts": [answer]})
        
        await message.answer(answer)
        
    except Exception as e:
        await message.answer("❌ Произошла ошибка при запросе к ИИ. Попробуй ещё раз.")

# ================================================

async def main():
    print("✅ Бот с Gemini успешно запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
