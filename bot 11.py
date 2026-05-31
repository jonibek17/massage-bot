import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message, CallbackQuery,
    InlineKeyboardMarkup, InlineKeyboardButton,
    KeyboardButton, ReplyKeyboardMarkup,
    ReplyKeyboardRemove
)
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

TOKEN = "8641373861:AAEFQtdsAej7Qfsf6m6acDOXL_ttAZhnLPs"
ADMIN_ID = 815471118

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# ─── Услуги ──────────────────────────────────────────────────────

SERVICES_RU = [
    ("Общий и лечебный массаж", 200_000),
    ("Коррекция фигуры", 250_000),
    ("Медовый массаж", 150_000),
    ("Релакс массаж", 150_000),
    ("Лимфодренажный массаж", 150_000),
    ("Антицеллюлитный массаж", 150_000),
    ("Массаж шейно-воротниковой зоны", 70_000),
    ("Массаж лица (лифтинг)", 50_000),
    ("Массаж спины", 100_000),
    ("Массаж головы", 50_000),
    ("Массаж живота", 100_000),
    ("Массаж ног", 50_000),
    ("Массаж рук", 30_000),
    ("Детский массаж", 50_000),
    ("Хиджама оздоровительная", 20_000),
]

SERVICES_UZ = [
    ("Umumiy va davolash massaji", 200_000),
    ("Tana korreksiyasi", 250_000),
    ("Asal massaji", 150_000),
    ("Relaks massaji", 150_000),
    ("Limfodrenaж massaji", 150_000),
    ("Tsellyulitga qarshi massaj", 150_000),
    ("Bo'yin-yoqa zonasi massaji", 70_000),
    ("Yuz massaji (lifting)", 50_000),
    ("Orqa massaji", 100_000),
    ("Bosh massaji", 50_000),
    ("Qorin massaji", 100_000),
    ("Oyoq massaji", 50_000),
    ("Qo'l massaji", 30_000),
    ("Bolalar massaji", 50_000),
    ("Tibbiy hijama", 20_000),
]

CERTS = [
    "🎓 Diplom (Rossiya)",
    "🎓 Diplom (O'zbekiston, Kasb-hunar kolleji)",
    "📜 Massajist-universal — barcha massaj turlari, LFK, fizioterapiya (Surayyo, 2024)",
    "📜 Massajist-universal — korreksiya, limfodrenaж, holat, qo'l liftingi (Surayyo)",
    "📜 Yuz massaji (Surayyo)",
    "📜 Bolalar massaji — 200 soat (2023)",
    "📜 Ayol 1.0 onlayn kursi",
]

# ─── Тексты на двух языках ────────────────────────────────────────

T = {
    "welcome": {
        "ru": "💆‍♀️ *MASSAGE FARANGIS*\n\nДобро пожаловать!\nМастер: *Халмирзаева Фарангиз*\nПрофессиональный массажист с дипломами и сертификатами 🏆\n\nВыберите нужный раздел 👇",
        "uz": "💆‍♀️ *MASSAGE FARANGIS*\n\nXush kelibsiz!\nUsta: *Xolmirzayeva Farangiz*\nDiplom va sertifikatlari bor professional massajist 🏆\n\nKerakli bo'limni tanlang 👇",
    },
    "services_title": {
        "ru": "💆 *Услуги и цены*\n\n_Курс массажа — 10 дней (полный сеанс)_\n\n",
        "uz": "💆 *Xizmatlar va narxlar*\n\n_Massaj kursi — 10 kun (to'liq seans)_\n\n",
    },
    "address": {
        "ru": "📍 *Адрес*\n\nТашкент, ул. Гулистон\n\nКлиент приходит к мастеру 🏠",
        "uz": "📍 *Manzil*\n\nToshkent, Guliston ko'chasi\n\nMijoz ustaga keladi 🏠",
    },
    "certs_title": {
        "ru": "🏆 *Дипломы и сертификаты*\n\n",
        "uz": "🏆 *Diplomlar va sertifikatlar*\n\n",
    },
    "reviews": {
        "ru": "⭐ *Отзывы клиентов*\n\n💬 _«Рахмат куллариз дард курмасин, яқин орада яна бошлаймиз худо хохласа, сиздан бошқасига массаж килдирмаймиз»_ 🥰\n\n📸 Результаты детского массажа — видимое улучшение осанки за курс 10 дней ✅",
        "uz": "⭐ *Mijozlar fikrlari*\n\n💬 _«Rahmat qo'llaringiz dard ko'rmasin, yaqin orada yana boshlaymiz, xudo xohlasa sizdan boshqasiga massaj qildirmaymiz»_ 🥰\n\n📸 Bolalar massaji natijalari — 10 kunlik kursda holat sezilarli yaxshilandi ✅",
    },
    "contacts": {
        "ru": "📞 *Контакты*\n\n📱 Телефон: +998 90 125 16 87\n💬 Telegram: @farangis\\_1987\n📸 Instagram (личный): @farangis.87.87\n📸 Instagram (массаж): @massage\\_farangis\\_kh",
        "uz": "📞 *Kontaktlar*\n\n📱 Telefon: +998 90 125 16 87\n💬 Telegram: @farangis\\_1987\n📸 Instagram (shaxsiy): @farangis.87.87\n📸 Instagram (massaj): @massage\\_farangis\\_kh",
    },
    "book_name": {
        "ru": "📅 *Запись на массаж*\n\nШаг 1️⃣ из 4️⃣\n\nВведите ваше имя:",
        "uz": "📅 *Massajga yozilish*\n\nQadam 1️⃣ / 4️⃣\n\nIsmingizni kiriting:",
    },
    "book_phone": {
        "ru": "Шаг 2️⃣ из 4️⃣\n\nВведите номер телефона или нажмите кнопку 👇",
        "uz": "Qadam 2️⃣ / 4️⃣\n\nTelefon raqamingizni kiriting yoki tugmani bosing 👇",
    },
    "book_service": {
        "ru": "Шаг 3️⃣ из 4️⃣\n\nВыберите услугу:",
        "uz": "Qadam 3️⃣ / 4️⃣\n\nXizmatni tanlang:",
    },
    "book_time": {
        "ru": "Шаг 4️⃣ из 4️⃣\n\nУкажите удобное время и дату:\n\n_Например: завтра в 14:00 или 5 июня в 10:00_",
        "uz": "Qadam 4️⃣ / 4️⃣\n\nQulay vaqt va sanani kiriting:\n\n_Masalan: ertaga soat 14:00 yoki 5-iyun soat 10:00_",
    },
    "book_done": {
        "ru": "✅ *Заявка принята!*\n\nМастер Фарангиз свяжется с вами в ближайшее время.\n\nЕсли срочно — напишите напрямую: @farangis\\_1987",
        "uz": "✅ *Arizangiz qabul qilindi!*\n\nFarangiz usta siz bilan tez orada bog'lanadi.\n\nShoshilinch bo'lsa — to'g'ridan-to'g'ri yozing: @farangis\\_1987",
    },
    "send_contact": {
        "ru": "📱 Отправить номер",
        "uz": "📱 Raqamni yuborish",
    },
    "map_btn": {
        "ru": "🗺 Открыть на карте",
        "uz": "🗺 Xaritada ochish",
    },
    "back": {
        "ru": "🔙 Главное меню",
        "uz": "🔙 Asosiy menyu",
    },
    "write_review": {
        "ru": "✍️ Написать отзыв",
        "uz": "✍️ Fikr bildirish",
    },
    "write_tg": {
        "ru": "💬 Написать в Telegram",
        "uz": "💬 Telegramga yozish",
    },
    "insta_btn": {
        "ru": "📸 Instagram массаж",
        "uz": "📸 Instagram massaj",
    },
    "menu_services": {
        "ru": "💆 Услуги и цены",
        "uz": "💆 Xizmatlar va narxlar",
    },
    "menu_book": {
        "ru": "📅 Записаться",
        "uz": "📅 Yozilish",
    },
    "menu_address": {
        "ru": "📍 Адрес",
        "uz": "📍 Manzil",
    },
    "menu_certs": {
        "ru": "🏆 Дипломы и сертификаты",
        "uz": "🏆 Diplomlar",
    },
    "menu_reviews": {
        "ru": "⭐ Отзывы",
        "uz": "⭐ Fikrlar",
    },
    "menu_contacts": {
        "ru": "📞 Контакты",
        "uz": "📞 Kontaktlar",
    },
}

def t(key, lang):
    return T[key].get(lang, T[key]["ru"])

# ─── FSM ─────────────────────────────────────────────────────────

class Booking(StatesGroup):
    name = State()
    phone = State()
    service = State()
    time = State()

# ─── Клавиатуры ──────────────────────────────────────────────────

def lang_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru"),
            InlineKeyboardButton(text="🇺🇿 O'zbek", callback_data="lang_uz"),
        ]
    ])

def main_menu(lang):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t("menu_services", lang), callback_data=f"services_{lang}")],
        [InlineKeyboardButton(text=t("menu_book", lang), callback_data=f"book_{lang}")],
        [InlineKeyboardButton(text=t("menu_address", lang), callback_data=f"address_{lang}")],
        [InlineKeyboardButton(text=t("menu_certs", lang), callback_data=f"certs_{lang}")],
        [InlineKeyboardButton(text=t("menu_reviews", lang), callback_data=f"reviews_{lang}")],
        [InlineKeyboardButton(text=t("menu_contacts", lang), callback_data=f"contacts_{lang}")],
    ])

def back_btn(lang):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t("back", lang), callback_data=f"main_{lang}")]
    ])

def phone_keyboard(lang):
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=t("send_contact", lang), request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

# ─── Handlers ────────────────────────────────────────────────────

@dp.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "💆‍♀️ *MASSAGE FARANGIS*\n\nВыберите язык / Tilni tanlang:",
        parse_mode="Markdown",
        reply_markup=lang_keyboard()
    )

@dp.callback_query(F.data.startswith("lang_"))
async def choose_lang(callback: CallbackQuery, state: FSMContext):
    lang = callback.data.replace("lang_", "")
    await state.update_data(lang=lang)
    await callback.message.edit_text(
        t("welcome", lang),
        parse_mode="Markdown",
        reply_markup=main_menu(lang)
    )

@dp.callback_query(F.data.startswith("main_"))
async def go_main(callback: CallbackQuery, state: FSMContext):
    lang = callback.data.replace("main_", "")
    await state.update_data(lang=lang)
    await callback.message.edit_text(
        t("welcome", lang),
        parse_mode="Markdown",
        reply_markup=main_menu(lang)
    )

# ─── Услуги ──────────────────────────────────────────────────────

@dp.callback_query(F.data.startswith("services_"))
async def show_services(callback: CallbackQuery):
    lang = callback.data.replace("services_", "")
    services = SERVICES_RU if lang == "ru" else SERVICES_UZ
    text = t("services_title", lang)
    for name, price in services:
        text += f"▪️ {name} — *{price:,} сум*\n".replace(",", " ")
    await callback.message.edit_text(
        text, parse_mode="Markdown", reply_markup=back_btn(lang)
    )

# ─── Адрес ───────────────────────────────────────────────────────

@dp.callback_query(F.data.startswith("address_"))
async def show_address(callback: CallbackQuery):
    lang = callback.data.replace("address_", "")
    await callback.message.edit_text(
        t("address", lang),
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=t("map_btn", lang), url="https://maps.google.com/maps?q=41.021397,70.068799&ll=41.021397,70.068799&z=16")],
            [InlineKeyboardButton(text=t("back", lang), callback_data=f"main_{lang}")],
        ])
    )

# ─── Дипломы ─────────────────────────────────────────────────────

@dp.callback_query(F.data.startswith("certs_"))
async def show_certs(callback: CallbackQuery):
    lang = callback.data.replace("certs_", "")
    text = t("certs_title", lang)
    for cert in CERTS:
        text += f"{cert}\n\n"
    await callback.message.edit_text(
        text, parse_mode="Markdown", reply_markup=back_btn(lang)
    )

# ─── Отзывы ──────────────────────────────────────────────────────

@dp.callback_query(F.data.startswith("reviews_"))
async def show_reviews(callback: CallbackQuery):
    lang = callback.data.replace("reviews_", "")
    await callback.message.edit_text(
        t("reviews", lang),
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=t("write_review", lang), url="https://t.me/farangis_1987")],
            [InlineKeyboardButton(text=t("back", lang), callback_data=f"main_{lang}")],
        ])
    )

# ─── Контакты ────────────────────────────────────────────────────

@dp.callback_query(F.data.startswith("contacts_"))
async def show_contacts(callback: CallbackQuery):
    lang = callback.data.replace("contacts_", "")
    await callback.message.edit_text(
        t("contacts", lang),
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=t("write_tg", lang), url="https://t.me/farangis_1987")],
            [InlineKeyboardButton(text=t("insta_btn", lang), url="https://www.instagram.com/massage_farangis_kh/")],
            [InlineKeyboardButton(text=t("back", lang), callback_data=f"main_{lang}")],
        ])
    )

# ─── Запись ──────────────────────────────────────────────────────

@dp.callback_query(F.data.startswith("book_"))
async def book_start(callback: CallbackQuery, state: FSMContext):
    lang = callback.data.replace("book_", "")
    await state.update_data(lang=lang)
    await state.set_state(Booking.name)
    await callback.message.edit_text(
        t("book_name", lang), parse_mode="Markdown"
    )

@dp.message(Booking.name)
async def book_name(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    await state.update_data(name=message.text)
    await state.set_state(Booking.phone)
    await message.answer(t("book_phone", lang), reply_markup=phone_keyboard(lang))

@dp.message(Booking.phone, F.contact)
async def book_phone_contact(message: Message, state: FSMContext):
    await state.update_data(phone=message.contact.phone_number)
    await _ask_service(message, state)

@dp.message(Booking.phone, F.text)
async def book_phone_text(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await _ask_service(message, state)

async def _ask_service(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    await state.set_state(Booking.service)
    services = SERVICES_RU if lang == "ru" else SERVICES_UZ
    buttons = []
    for i, (name, price) in enumerate(services):
        buttons.append([InlineKeyboardButton(
            text=f"{name} — {price:,} сум".replace(",", " "),
            callback_data=f"svc_{i}"
        )])
    await message.answer(
        t("book_service", lang),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
    )

@dp.callback_query(Booking.service, F.data.startswith("svc_"))
async def book_service(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    idx = int(callback.data.replace("svc_", ""))
    services = SERVICES_RU if lang == "ru" else SERVICES_UZ
    service_name, price = services[idx]
    await state.update_data(service=f"{service_name} — {price:,} сум".replace(",", " "))
    await state.set_state(Booking.time)
    await callback.message.edit_text(t("book_time", lang), parse_mode="Markdown")

@dp.message(Booking.time)
async def book_time(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    await state.clear()

    booking_text = (
        "🔔 *Yangi ariza / Новая заявка!*\n\n"
        f"👤 Ism/Имя: {data['name']}\n"
        f"📱 Tel: {data['phone']}\n"
        f"💆 Xizmat/Услуга: {data['service']}\n"
        f"🕐 Vaqt/Время: {message.text}\n"
        f"🌐 Til/Язык: {'O\'zbek' if lang == 'uz' else 'Русский'}"
    )
    try:
        await bot.send_message(815471118, booking_text, parse_mode="Markdown")
    except Exception:
        pass

    await message.answer(
        t("book_done", lang),
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardRemove()
    )
    await message.answer("👇", reply_markup=main_menu(lang))

# ─── Запуск ──────────────────────────────────────────────────────

async def main():
    print("💆 Massage Farangis Bot запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
