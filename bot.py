import asyncio
import os
import logging
import json
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram import F
import google.generativeai as genai

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not TOKEN or not GEMINI_API_KEY:
    raise ValueError("TOKEN или GEMINI_API_KEY не найден!")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Режим быдлячества
blyadenok_mode = False

GOPNIK_PROMPT = """Ты - дерзкий и токсичный русскоязычный гопник. 
Стиль: стеб, самоирония, неожиданные панчлайны, пацанский сленг.
Используй мат часто. Главное - чтобы было СМЕШНО. Делай сильные панчлайны в конце."""

BLYADENOK_PROMPT = """Ты - максимально токсичный, злой и быдлятский гопник. 
Мата не жалей, стеби по полной, будь максимально грубым и пошлым. Никаких тормозов."""

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Здарова, братан! Пиши чё надо. Вот команды: /joke; /roast; /advice; /razbor; /blyadenok")

@dp.message(Command("joke"))
async def joke(message: types.Message):
    await message.answer("Ща расскажу...")

@dp.message(Command("roast"))
async def roast(message: types.Message):
    text = message.text.replace("/roast", "").strip()
    if not text:
        text = "этот чел"
    await message.answer("Ща зажгу...")

@dp.message(Command("advice"))
async def advice(message: types.Message):
    await message.answer("Сейчас дам совет...")

@dp.message(Command("razbor"))
async def razbor(message: types.Message):
    await message.answer("Ща разберём эту хуйню...")

@dp.message(Command("blyadenok""))
async def blyadenok(message: types.Message):
    global blyadenok_mode
    blyadenok_mode = not blyadenok_mode
    status = "ВКЛЮЧЁН" if blyadenok_mode else "ВЫКЛЮЧЕН"
    await message.answer(f"Режим 'БЛЯДЁНОК' {status} 🔥")

@dp.message(F.text)
async def chat(message: types.Message):
    prompt = BLYADENOK_PROMPT if blyadenok_mode else GOPNIK_PROMPT
    
    try:
        full_prompt = f"{prompt}\n\nПользователь: {message.text}"
        response = model.generate_content(full_prompt)
        answer = response.text.strip()
        await message.answer(answer)
    except:
        await message.answer("Бля, щас не получилось, попробуй ещё раз.")

# Обработка голосовых сообщений
@dp.message(F.voice)
async def voice_handler(message: types.Message):
    await message.answer("Голосуху принял, ща послушаю...")

# Обработка фото
@dp.message(F.photo)
async def photo_handler(message: types.Message):
    await message.answer("Фото принял. Чё там за хуйня?")

async def main():
    print("✅ Гопник-бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())