import asyncio
import os
import logging
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

blyadenok_mode = False

GOPNIK_PROMPT = """Ты - дерзкий и токсичный русскоязычный гопник. 
Стиль: стеб, самоирония, неожиданные панчлайны, пацанский сленг.
Используй мат часто. Главное - чтобы было СМЕШНО. Делай сильные панчлайны."""

BLYADENOK_PROMPT = """Ты - максимально токсичный и быдлятский гопник. 
Мата не жалей, стеби жёстко и по полной."""

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Здарова, братан! Урал на связи🤣🤘 Вот че я могу исполнять:/joke - Расскажу шутейку; /roast - Прожарка кого-нибудь🔥; /advice - Дам совет; /razbor - Дам свое мнение насчёт чего-нибудь; /blyadenok - буду под водярой😂😂")

@dp.message(Command("joke"))
async def joke(message: types.Message):
    await message.answer("Ща расскажу шутку...")

@dp.message(Command("roast"))
async def roast(message: types.Message):
    await message.answer("Ща кого-то прожгу...")

@dp.message(Command("advice"))
async def advice(message: types.Message):
    await message.answer("Сейчас дам пацанский совет...")

@dp.message(Command("razbor"))
async def razbor(message: types.Message):
    await message.answer("Ща разберём эту хуйню...")

@dp.message(Command("blyadenok"))
async def toggle_blyadenok(message: types.Message):
    global blyadenok_mode
    blyadenok_mode = not blyadenok_mode
    status = "ВКЛЮЧЁН" if blyadenok_mode else "ВЫКЛЮЧЁН"
    await message.answer(f"🔥 Режим БЛЯДЁНОК {status}!")

@dp.message(F.text)
async def chat(message: types.Message):
    prompt = BLYADENOK_PROMPT if blyadenok_mode else GOPNIK_PROMPT
    try:
        full_prompt = f"{prompt}\n\nПользователь: {message.text}"
        response = model.generate_content(full_prompt)
        answer = response.text.strip()
        await message.answer(answer)
    except Exception as e:
        logging.error(f"Ошибка: {e}")
        await message.answer("Бля, щас не получилось, попробуй позже.")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    print("✅ Гопник-бот запущен с командами")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())