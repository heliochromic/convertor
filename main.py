import logging

from telegram import ReplyKeyboardMarkup, Update, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters

from conversions import *

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.INFO)

logger = logging.getLogger(__name__)

currencies = get_currencies_list()
currency_buttons = []

for currency in currencies:
    currency_code = currency.split('-')[0].strip()[:3]
    currency_buttons.append([currency_code])

reply_keyboard = ReplyKeyboardMarkup(currency_buttons, one_time_keyboard=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_name = update.effective_user.full_name
    await update.message.reply_text(f"Hello, {user_name}\n To look at all available functions click on /help",
                                    reply_markup=ReplyKeyboardRemove())


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Call /convert to start you conversion from base to target currency")


# Constants to represent states
BASE_CURRENCY, TARGET_CURRENCY, AMOUNT = range(3)


async def convert_start(update, context):
    await update.message.reply_text("Let's start the currency conversion!\nPlease enter the base currency:",
                                    reply_markup=reply_keyboard)
    return BASE_CURRENCY


async def get_base_currency(update, context):
    context.user_data['base_currency'] = update.message.text
    await update.message.reply_text("Great! Now, please enter the target currency:",
                                    reply_markup=reply_keyboard)
    return TARGET_CURRENCY


async def get_target_currency(update, context):
    context.user_data['target_currency'] = update.message.text
    await update.message.reply_text("Awesome! Please enter the amount to convert:",
                                    reply_markup=ReplyKeyboardRemove())
    return AMOUNT


async def get_amount(update, context):
    context.user_data['amount'] = float(update.message.text)
    base_currency = context.user_data['base_currency']
    target_currency = context.user_data['target_currency']
    amount = context.user_data['amount']

    # Perform the conversion using your conversions module
    result = convert(base_currency, target_currency, amount)

    await update.message.reply_text(
        f"The result of converting {amount} {base_currency} to {target_currency} is: {result}")

    return ConversationHandler.END


async def cancel(update, context):
    await update.message.reply_text('Conversion canceled.',
                                    reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def main() -> None:
    application = Application.builder().token("6630982386:AAGoyuOgak9o11tEJjPRRi2BOF7fbKudrgM").build()
    application.add_handler(CommandHandler("start", start))
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('convert', convert_start)],
        states={
            BASE_CURRENCY: [MessageHandler(filters.TEXT, get_base_currency)],
            TARGET_CURRENCY: [MessageHandler(filters.TEXT, get_target_currency)],
            AMOUNT: [MessageHandler(filters.TEXT, get_amount)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    # Add the conversation handler to the application
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("help", help))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
