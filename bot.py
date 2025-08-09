from aiogram import Bot, Dispatcher
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.context import FSMContext
from deep_translator import GoogleTranslator
import asyncio
from aiogram.client.session.aiohttp import AiohttpSession

BOT_TOKEN = "8447059971:AAFGcLR4k5OcBsKSiuEv70bUo8gtpxdF7vA"

session = AiohttpSession(proxy="http://proxy.example.com:3128")  # Haqiqiy proxy manzilini yozing
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML), session=session)
dp = Dispatcher(storage=MemoryStorage())

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="/start"), KeyboardButton(text="/clear")],
        [KeyboardButton(text="🇺🇿 O'zbekcha"), KeyboardButton(text="🇷🇺 Русский")],
        [KeyboardButton(text="🇬🇧 English"), KeyboardButton(text="🇹🇯 Тоҷикӣ"), KeyboardButton(text="🇩🇪 Deutsch")]
    ],
    resize_keyboard=True
)

def fast_translate(text, src='auto', dest='en'):
    try:
        return GoogleTranslator(source=src, target=dest).translate(text)
    except Exception as e:
        return f"❌ Tarjima qilishda xatolik yuz berdi: {e}"

def language_response(lang_code: str) -> str:
    responses = {
        "uz": "✅ Til tanlandi: <b>O'zbekcha</b>\nEndi tarjima qilmoqchi bo‘lgan matningizni yuboring.",
        "ru": "✅ Язык выбран: <b>Русский</b>\nТеперь отправьте текст для перевода.",
        "en": "✅ Language selected: <b>English</b>\nNow send the text you want to translate.",
        "tg": "✅ Забон интихоб гардид: <b>Тоҷикӣ</b>\nМатни хоҳиши тарҷима шударо равон фиристед.",
        "de": "✅ Sprache gewählt: <b>Deutsch</b>\nBitte senden Sie den zu übersetzenden Text."
    }
    return responses.get(lang_code, "✅ Til tanlandi. Matn yuboring.")

@dp.message(lambda message: message.text == "/start")
async def start_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Bu bot sizga matnlarni avtomatik tarjima qilishda yordam beradi.\n"
        "Tilni tanlang yoki matn yuboring – bot uni avtomatik tarjima qiladi 🌐📲\n\n"
        "🤖 <b>Bot haqida:</b>\n"
        "Bu tarjima bot <b>@Amirkhonvv</b> tomonidan yaratilgan.\n"
        "✉️ Murojaat uchun: @Amirkhonvv\n\n"
        "⬇️ Quyidan tilni tanlang yoki matn yuboring:",
        reply_markup=main_menu
    )

@dp.message(lambda message: message.text == "/clear")
async def clear_handler(message: Message):
    await message.answer("🧹 Chat tozalandi. Yangi matn yuboring yoki til tanlang.", reply_markup=main_menu)

@dp.message()
async def translate_handler(message: Message, state: FSMContext):
    text = message.text

    lang_map = {
        "🇺🇿 O'zbekcha": 'uz',
        "🇷🇺 Русский": 'ru',
        "🇬🇧 English": 'en',
        "🇹🇯 Тоҷикӣ": 'tg',
        "🇩🇪 Deutsch": 'de'
    }

    data = await state.get_data()
    lang = data.get("target_lang", "en")

    if text in lang_map:
        lang = lang_map[text]
        await state.update_data(target_lang=lang)
        reply = language_response(lang)
        await message.answer(reply)
    else:
        result = fast_translate(text, dest=lang)
        await message.answer(f"<b>Tarjima:</b> {result}")

async def main():
    print("✅ Bot ishga tushdi!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("⛔ Bot to‘xtadi.")
