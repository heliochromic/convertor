import logging

from telegram import ReplyKeyboardMarkup, Update, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton, \
    InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters

from conversions import *
from silpo_scrapper import get_random_product

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
    await update.message.reply_text(f"Hello, {user_name}💕💕💕💕\nTo look at all available functions click on /help",
                                    reply_markup=ReplyKeyboardRemove())


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Call /convert to start you conversion from base to target currency\n"
                                    "Call /get_useful_info to get really useful information for today\n"
                                    "")


async def get_useful_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    product = get_random_product()
    await update.message.reply_photo(product['link'])
    await update.message.reply_text(
        f"Today at Silpo, you can buy {product['name']} for {product['after']} (previously priced at {product['before']})."
    )
    await update.message.reply_text(
        "You can also convert the price and see how much you should pay in EUR and USD\nJust call /convert.")
    await update.message.reply_text(
        "To pre-order and confirm your purchase, please send the amount to the following link Once the payment is received, your order will be processed."
    )
    # Create an inline button with a link
    keyboard = [[InlineKeyboardButton("Pre-order link", url="https://send.monobank.ua/KytxdrYEK")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the inline button with the link
    await update.message.reply_text(
        "Click the button below to pre-order:",
        reply_markup=reply_markup
    )


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

    result = convert(base_currency, target_currency, amount)

    print(type(result))

    await update.message.reply_text(
        f"The result of converting {amount} {base_currency} to {target_currency} is: {result}")

    return ConversationHandler.END


async def cancel(update, context):
    await update.message.reply_text('Conversion canceled.',
                                    reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def main() -> None:
    application = Application.builder().token("6630982386:AAHaWWm-ScANbcdPWjsDmCmznPdckvdi764").build()
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
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("get_useful_info", get_useful_info))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
