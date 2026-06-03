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
Используй мат часто. Главное - чтобы было СМЕШНО."""

BLYADENOK_PROMPT = """Ты - максимально токсичный и быдлятский гопник. 
Мата не жалей, стеби жёстко и по полной."""

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Здарова, братан! Урал на связи🤣🤘\n\nВот че я могу:\n/joke - Расскажу шутейку\n/roast - Прожарка кого-нибудь🔥\n/advice - Дам совет\n/razbor - Дам свое мнение\n/blyadenok - буду под водярой😂")

@dp.message(Command("joke"))
async def joke(message: types.Message):
    await message.answer("Ща расскажу шутку...")
    prompt = f"{BLYADENOK_PROMPT if blyadenok_mode else GOPNIK_PROMPT}\n\nСгенерируй смешную шутку в гопник стиле."
    try:
        response = model.generate_content(prompt)
        await message.answer(response.text.strip())
    except:
        await message.answer("Бля, шутка не пошла, попробуй ещё.")

@dp.message(Command("roast"))
async def roast(message: types.Message):
    text = message.text.replace("/roast", "").strip() or "этот чел"
    await message.answer("Ща прожарю...")
    prompt = f"{BLYADENOK_PROMPT if blyadenok_mode else GOPNIK_PROMPT}\n\nПрожарь жёстко вот это: {text}"
    try:
        response = model.generate_content(prompt)
        await message.answer(response.text.strip())
    except:
        await message.answer("Не получилось прожарить, попробуй ещё.")

@dp.message(Command("advice"))
async def advice(message: types.Message):
    text = message.text.replace("/advice", "").strip() or "по жизни"
    await message.answer("Сейчас дам совет...")
    prompt = f"{BLYADENOK_PROMPT if blyadenok_mode else GOPNIK_PROMPT}\n\nДай пацанский совет по теме: {text}"
    try:
        response = model.generate_content(prompt)
        await message.answer(response.text.strip())
    except:
        await message.answer("Совет не зашёл.")

@dp.message(Command("razbor"))
async def razbor(message: types.Message):
    text = message.text.replace("/razbor", "").strip() or "какая-то хуйня"
    await message.answer("Ща разберём...")
    prompt = f"{BLYADENOK_PROMPT if blyadenok_mode else GOPNIK_PROMPT}\n\nСделай токсичный разбор вот этого: {text}"
    try:
        response = model.generate_content(prompt)
        await message.answer(response.text.strip())
    except:
        await message.answer("Разбор не получился.")

@dp.message(Command("blyadenok"))
async def toggle_blyadenok(message: types.Message):
    global blyadenok_mode
    blyadenok_mode = not blyadenok_mode
    status = "ВКЛЮЧЁН" if blyadenok_mode else "ВЫКЛЮЧЁН"
    await message.answer(f"🔥 Режим БЛЯДЁНОК {status}!")

@dp.message(F.text)
async def chat(message: types.Message):
    if message.text.startswith('/'):
        return  # Игнорируем неизвестные команды
    prompt = BLYADENOK_PROMPT if blyadenok_mode else GOPNIK_PROMPT
    try:
        full_prompt = f"{prompt}\n\nПользователь: {message.text}"
        response = model.generate_content(full_prompt)
        await message.answer(response.text.strip())
    except:
        await message.answer("Бля, щас не получилось.")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    print("✅ Гопник-бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())