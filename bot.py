from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)

TOKEN = "8808502475:AAHLB2S8IqEsAjqXDOqyMAWupvJrE88sLlE"

# -------------------------
# منوی اصلی
# -------------------------

def main_menu():
    keyboard = [
        [
            InlineKeyboardButton("💬 چت ناشناس", callback_data="chat"),
            InlineKeyboardButton("🔎 جستجوی افراد", callback_data="search")
        ],
        [
            InlineKeyboardButton("👥 افراد آنلاین", callback_data="online"),
            InlineKeyboardButton("❤️ لایک‌ها", callback_data="likes")
        ],
        [
            InlineKeyboardButton("📇 مخاطبین", callback_data="contacts"),
            InlineKeyboardButton("👤 پروفایل من", callback_data="profile")
        ],
        [
            InlineKeyboardButton("🪙 سکه", callback_data="coins"),
            InlineKeyboardButton("⚙️ تنظیمات", callback_data="settings")
        ]
    ]

    return InlineKeyboardMarkup(keyboard)


# -------------------------
# شروع ربات
# -------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data.clear()

    context.user_data["step"] = "age"

    await update.message.reply_text(
        "🖤 به نجوا خوش اومدی.\n\n"
        "برای ساخت پروفایل، اول سنت رو وارد کن.\n\n"
        "🎂 سن خودت رو فقط به صورت عدد بفرست."
    )


# -------------------------
# دریافت اطلاعات ثبت‌نام
# -------------------------

async def registration(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text.strip()
    step = context.user_data.get("step")

    # سن
    if step == "age":

        if not text.isdigit():
            await update.message.reply_text(
                "❌ لطفاً سن رو فقط به صورت عدد وارد کن."
            )
            return

        age = int(text)

        if age < 13:
            await update.message.reply_text(
                "❌ حداقل سن استفاده از نجوا ۱۳ ساله."
            )
            return

        if age > 100:
            await update.message.reply_text(
                "❌ لطفاً سن واقعی خودت رو وارد کن."
            )
            return

        context.user_data["age"] = age
        context.user_data["step"] = "gender"

        keyboard = [
            [
                InlineKeyboardButton("👨 پسر", callback_data="gender_male"),
                InlineKeyboardButton("👩 دختر", callback_data="gender_female")
            ]
        ]

        await update.message.reply_text(
            "⚥ جنسیتت رو انتخاب کن:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # شهر
    elif step == "city":

        context.user_data["city"] = text
        context.user_data["step"] = "username"

        await update.message.reply_text(
            "👤 حالا یک نام مستعار برای خودت انتخاب کن."
        )

    # نام مستعار
    elif step == "username":

        if len(text) < 2 or len(text) > 30:
            await update.message.reply_text(
                "❌ نام مستعار باید بین ۲ تا ۳۰ کاراکتر باشه."
            )
            return

        context.user_data["username"] = text
        context.user_data["step"] = "bio"

        await update.message.reply_text(
            "📝 حالا یک بیوی کوتاه برای پروفایلت بنویس.\n\n"
            "اگر نمی‌خوای بیو داشته باشی، بنویس: ندارم"
        )

    # بیو
    elif step == "bio":

        context.user_data["bio"] = text

        age = context.user_data["age"]
        gender = context.user_data["gender"]
        city = context.user_data["city"]
        username = context.user_data["username"]

        # گروه سنی
        if 13 <= age <= 17:
            age_group = "13-17"
        else:
            age_group = "18+"

        context.user_data["age_group"] = age_group
        context.user_data["coins"] = 0

        await update.message.reply_text(
            "✅ پروفایلت با موفقیت ساخته شد!\n\n"
            f"👤 نام: {username}\n"
            f"🎂 سن: {age}\n"
            f"⚥ جنسیت: {gender}\n"
            f"🗺️ شهر: {city}\n"
            f"🛡️ گروه سنی: {age_group}\n"
            f"🪙 سکه: 0\n\n"
            "🖤 به نجوا خوش اومدی.",
            reply_markup=main_menu()
        )

        context.user_data["step"] = "done"


# -------------------------
# انتخاب جنسیت
# -------------------------

async def gender_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if query.data == "gender_male":
        context.user_data["gender"] = "پسر"

    elif query.data == "gender_female":
        context.user_data["gender"] = "دختر"

    else:
        return

    context.user_data["step"] = "city"

    await query.edit_message_text(
        "🗺️ حالا شهرت رو وارد کن."
    )


# -------------------------
# دکمه‌های منوی اصلی
# -------------------------

async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if query.data == "chat":

        keyboard = [
            [InlineKeyboardButton("🎲 مچ تصادفی", callback_data="random_match")],
            [InlineKeyboardButton("🎯 مچ هم‌سن", callback_data="same_age")],
            [InlineKeyboardButton("⚥ مچ بر اساس جنسیت", callback_data="gender_match")],
            [InlineKeyboardButton("🗺️ مچ بر اساس شهر", callback_data="city_match")],
            [InlineKeyboardButton("🔎 جستجوی پیشرفته", callback_data="advanced_match")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="back")]
        ]

        await query.edit_message_text(
            "💬 چت ناشناس\n\n"
            "نوع مچ خودت رو انتخاب کن:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "profile":

        age = context.user_data.get("age", "ثبت نشده")
        gender = context.user_data.get("gender", "ثبت نشده")
        city = context.user_data.get("city", "ثبت نشده")
        username = context.user_data.get("username", "ثبت نشده")
        bio = context.user_data.get("bio", "ثبت نشده")

        await query.edit_message_text(
            "👤 پروفایل من\n\n"
            f"نام: {username}\n"
            f"🎂 سن: {age}\n"
            f"⚥ جنسیت: {gender}\n"
            f"🗺️ شهر: {city}\n"
            f"📝 بیو: {bio}"
        )

    elif query.data == "coins":

        coins = context.user_data.get("coins", 0)

        await query.edit_message_text(
            f"🪙 کیف پول نجوا\n\n"
            f"موجودی فعلی: {coins} سکه\n\n"
            "💳 خرید سکه و امکانات سکه‌ای در مرحله بعد اضافه میشه."
        )

    elif query.data == "search":

        await query.edit_message_text(
            "🔎 جستجوی افراد\n\n"
            "جستجوی بر اساس سن، جنسیت و شهر در مرحله بعد فعال میشه."
        )

    elif query.data == "online":

        await query.edit_message_text(
            "👥 افراد آنلاین\n\n"
            "این بخش در مرحله بعد فعال میشه."
        )

    elif query.data == "likes":

        await query.edit_message_text(
            "❤️ لایک‌ها\n\n"
            "فعلاً لایکی نداری."
        )

    elif query.data == "contacts":

        await query.edit_message_text(
            "📇 مخاطبین\n\n"
            "این بخش در مرحله بعد فعال میشه."
        )

    elif query.data == "settings":

        await query.edit_message_text(
            "⚙️ تنظیمات\n\n"
            "تنظیمات نجوا در مرحله بعد اضافه میشه."
        )

    elif query.data == "back":

        await query.edit_message_text(
            "🖤 منوی اصلی نجوا\n\n"
            "یک گزینه رو انتخاب کن:",
            reply_markup=main_menu()
        )

    else:

        await query.edit_message_text(
            "🔧 این قابلیت هنوز در حال ساختنه."
        )


# -------------------------
# اجرای ربات
# -------------------------

def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(
        CallbackQueryHandler(
            gender_handler,
            pattern="^gender_"
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            menu_handler
        )
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            registration
        )
    )

    print("🤖 Najva is running...")

    app.run_polling()


if __name__ == "__main__":
    main()
