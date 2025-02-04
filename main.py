# main.py
from config import TOKEN
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    ContextTypes,
    CallbackQueryHandler
)
from calculations import calculate_panels
from handlers import *  # Import all handlers
from dobor import calculate_all_dobor_elements, get_dobor_execution_keyboard, get_corner_size_keyboard, ask_for_corner_details, dobor_callback, enter_corner_quantity, enter_corner_height, enter_quantity, enter_length

# Состояния для ConversationHandler
REQUEST_CONTACT, WALL_HEIGHT, WALL_WIDTH, ADD_WALL, ASK_WINDOWS, WINDOW_HEIGHT, WINDOW_WIDTH, ADD_WINDOW, ASK_DOORS, DOOR_HEIGHT, DOOR_WIDTH, ADD_DOOR, PANEL_TYPE,  PANEL_COMBINATION, CALCULATION, ASK_COST_OR_EXTRAS, CALCULATE_COST, CALCULATE_EXTRAS, CHOOSE_DOBOR_EXECUTION, CHOOSE_CORNER_SIZE, ENTER_CORNER_QUANTITY, ENTER_CORNER_HEIGHT, ENTER_QUANTITY, ENTER_LENGTH, CHOOSE_OPENING_DEPTH, CHOOSE_FRAME_WIDTH = range(26)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['walls'] = []
    context.user_data['windows'] = []
    context.user_data['doors'] = []
    context.user_data['chat_id'] = update.message.chat_id

    await update.message.reply_text(
        "Привет! Я помогу рассчитать количество фасадных панелей. "
        "Пожалуйста, поделись своим контактом, чтобы продолжить:",
        reply_markup=get_contact_keyboard(),
    )
    return REQUEST_CONTACT

async def request_contact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    contact = update.message.contact
    context.user_data['contact'] = contact
    await update.message.reply_text(
        "Спасибо! Теперь введи высоту стены (в метрах):",
         reply_markup=ReplyKeyboardMarkup([[]], resize_keyboard=True, one_time_keyboard=True),
    )
    return WALL_HEIGHT

def main():
    application = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            REQUEST_CONTACT: [MessageHandler(filters.CONTACT, request_contact)],
            WALL_HEIGHT: [MessageHandler(filters.TEXT & ~filters.COMMAND, wall_height)],
            WALL_WIDTH: [MessageHandler(filters.TEXT & ~filters.COMMAND, wall_width)],
            ADD_WALL: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_wall)],
            ASK_WINDOWS: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_windows)],
            WINDOW_HEIGHT: [MessageHandler(filters.TEXT & ~filters.COMMAND, window_height)],
            WINDOW_WIDTH: [MessageHandler(filters.TEXT & ~filters.COMMAND, window_width)],
            ADD_WINDOW: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_window)],
            ASK_DOORS: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_doors)],
            DOOR_HEIGHT: [MessageHandler(filters.TEXT & ~filters.COMMAND, door_height)],
            DOOR_WIDTH: [MessageHandler(filters.TEXT & ~filters.COMMAND, door_width)],
            ADD_DOOR: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_door)],
            PANEL_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, panel_type)],
            PANEL_COMBINATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, panel_combination)],
            ASK_COST_OR_EXTRAS: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_cost_or_extras)],
            CALCULATE_COST: [],
            CALCULATE_EXTRAS: [],
            CHOOSE_DOBOR_EXECUTION: [CallbackQueryHandler(lambda update, context: dobor_callback(update, context, CHOOSE_DOBOR_EXECUTION, CHOOSE_CORNER_SIZE, CHOOSE_OPENING_DEPTH, CHOOSE_FRAME_WIDTH, ENTER_CORNER_QUANTITY, ENTER_CORNER_HEIGHT, ENTER_QUANTITY, ENTER_LENGTH))],
            CHOOSE_CORNER_SIZE: [CallbackQueryHandler(lambda update, context: dobor_callback(update, context, CHOOSE_DOBOR_EXECUTION, CHOOSE_CORNER_SIZE, CHOOSE_OPENING_DEPTH, CHOOSE_FRAME_WIDTH, ENTER_CORNER_QUANTITY, ENTER_CORNER_HEIGHT, ENTER_QUANTITY, ENTER_LENGTH))],
            ENTER_CORNER_QUANTITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_corner_quantity)],
            ENTER_CORNER_HEIGHT: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_corner_height)],
            ENTER_QUANTITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_quantity)],
            ENTER_LENGTH: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_length)],
            CHOOSE_OPENING_DEPTH: [CallbackQueryHandler(lambda update, context: dobor_callback(update, context, CHOOSE_DOBOR_EXECUTION, CHOOSE_CORNER_SIZE, CHOOSE_OPENING_DEPTH, CHOOSE_FRAME_WIDTH, ENTER_CORNER_QUANTITY, ENTER_CORNER_HEIGHT, ENTER_QUANTITY, ENTER_LENGTH))],
            CHOOSE_FRAME_WIDTH: [CallbackQueryHandler(lambda update, context: dobor_callback(update, context, CHOOSE_DOBOR_EXECUTION, CHOOSE_CORNER_SIZE, CHOOSE_OPENING_DEPTH, CHOOSE_FRAME_WIDTH, ENTER_CORNER_QUANTITY, ENTER_CORNER_HEIGHT, ENTER_QUANTITY, ENTER_LENGTH))],
        },
        fallbacks=[],
    )

    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == '__main__':
    main()