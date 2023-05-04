import logging
import datetime
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    ApplicationBuilder, 
    ContextTypes, 
    CommandHandler, 
    MessageHandler, 
    filters,
    ConversationHandler
)
from insert_user import insert_employee

NAME, BIRTH_DATE, LOCATION, PROFESSION, VALIDATION = range(5)

user = {
    'id': None,
    'name': None,
    'birth': None,
    'location': None,
    'profession': None
}

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def validate_date(date_text, update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        datetime.date.fromisoformat(date_text)
        return True
    except ValueError:
        await update.message.reply_text("Incorrect date, please use format (YYYY-MM-DD)")
        return False
        
    
async def validate_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "Yes":
        print("Operation successful!")
        await update.message.reply_text("Thank you for using our bot. The information is going to be saved")
        insert_employee(user["id"], user["name"], user["birth"], user["location"], user["profession"])
        return ConversationHandler.END
    else:
        await update.message.reply_text("Let's try again")
        await update.message.reply_text("Tell me your name")
        return NAME


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! I'm telegram jobs bot. I'm here to help you finding a job." )
    await update.message.reply_text("Tell me your name")


    # getting user's id
    user["id"] = update.message.from_user.id

    return NAME

async def name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # getting user's name
    user["name"] = update.message.text

    await update.message.reply_text("Now tell me your birth date (YYYY-MM-DD)")
    return BIRTH_DATE

async def birth(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # getting user's birth date
    user["birth"] = update.message.text
    if await validate_date(user["birth"], update, context):
        await update.message.reply_text("Now tell me your City, Country")
        return LOCATION
    else:
        return BIRTH_DATE


async def location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # getting user's city and country
    user["location"] = update.message.text

    await update.message.reply_text("Now tell me your profession")
    return PROFESSION


async def profession(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # getting user's name
    user["profession"] = update.message.text

    reply_keyboard = [["Yes", "No"]]

    await update.message.reply_text("Is everything correct?")
    await update.message.reply_text(
        "Your name: {0}\nYour birth date: {1}\nYour location: {2}\nYour profession: {3}".format(user["name"], user["birth"], user["location"], user["profession"]), 
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Yes or No?"
        ),
    )

    return VALIDATION


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Bye! I hope I helped you.", reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

if __name__ == '__main__':
    application = ApplicationBuilder().token('6180809343:AAGT_sdjyFaivaoLkG21zISRyk46Y_7MhXc').build()
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, name)],
            BIRTH_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, birth)],
            LOCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, location)],
            PROFESSION: [MessageHandler(filters.TEXT & ~filters.COMMAND, profession)],
            VALIDATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, validate_info)]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )
    
    application.add_handler(conv_handler)
    
    application.run_polling()