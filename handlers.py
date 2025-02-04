# handlers.py
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes, ConversationHandler
from calculations import calculate_panels
from dobor import calculate_all_dobor_elements, ask_for_corner_details, dobor_callback
from keyboards import *

async def wall_height(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        height = float(update.message.text)
        if height <= 0:
            await update.message.reply_text("Высота стены должна быть больше нуля. Попробуйте снова:")
            return WALL_HEIGHT
        if height > 50:
            await update.message.reply_text("Высота стены кажется слишком большой. Пожалуйста, проверьте введенное значение и попробуйте снова:")
            return WALL_HEIGHT
        context.user_data['current_wall'] = {'height': height}
        await update.message.reply_text("Теперь введи ширину стены (в метрах):")
        return WALL_WIDTH
    except ValueError:
        await update.message.reply_text("Пожалуйста, введи число. Попробуй снова:")
        return WALL_HEIGHT

async def wall_width(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        width = float(update.message.text)
        if width <= 0:
            await update.message.reply_text("Ширина стены должна быть больше нуля. Попробуйте снова:")
            return WALL_WIDTH
        if width > 100:
            await update.message.reply_text("Ширина стены кажется слишком большой. Пожалуйста, проверьте введенное значение и попробуйте снова:")
            return WALL_WIDTH
        context.user_data['current_wall']['width'] = width
        context.user_data['walls'].append(context.user_data['current_wall'])
        await update.message.reply_text("Стена добавлена. Что дальше?", reply_markup=get_wall_keyboard())
        return ADD_WALL
    except ValueError:
        await update.message.reply_text("Пожалуйста, введи число. Попробуй снова:")
        return WALL_WIDTH

async def add_wall(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text

    if text == "Добавить еще стену":
        await update.message.reply_text("Введи высоту следующей стены (в метрах):",
            reply_markup=ReplyKeyboardMarkup([[]], resize_keyboard=True, one_time_keyboard=True))
        return WALL_HEIGHT
    elif text == "Перейти к проемам":
        await update.message.reply_text("Желаете добавить окна?", reply_markup=get_yes_no_keyboard())
        return ASK_WINDOWS

async def ask_windows(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "Да":
        await update.message.reply_text("Введи высоту окна (в метрах):", reply_markup=ReplyKeyboardMarkup([[]], resize_keyboard=True, one_time_keyboard=True))
        return WINDOW_HEIGHT
    elif text == "Нет":
        await update.message.reply_text("Переходим к дверям. Желаете добавить двери?", reply_markup=get_yes_no_keyboard())
        return ASK_DOORS

async def window_height(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        height = float(update.message.text)
        if height <= 0:
            await update.message.reply_text("Высота окна должна быть больше нуля. Попробуйте снова:")
            return WINDOW_HEIGHT
        if height > 10:
            await update.message.reply_text("Высота окна кажется слишком большой. Пожалуйста, проверьте введенное значение и попробуйте снова:")
            return WINDOW_HEIGHT
        context.user_data['current_window'] = {'height': height}
        await update.message.reply_text("Теперь введи ширину окна (в метрах):")
        return WINDOW_WIDTH
    except ValueError:
        await update.message.reply_text("Пожалуйста, введи число. Попробуй снова:")
        return WINDOW_HEIGHT

async def window_width(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        width = float(update.message.text)
        if width <= 0:
            await update.message.reply_text("Ширина окна должна быть больше нуля. Попробуйте снова:")
            return WALL_WIDTH
        if width > 20:
            await update.message.reply_text("Ширина окна кажется слишком большой. Пожалуйста, проверьте введенное значение и попробуйте снова:")
            return WALL_WIDTH
        context.user_data['current_window']['width'] = width
        context.user_data['windows'].append(context.user_data['current_window'])
        await update.message.reply_text("Окно добавлено. Что дальше?", reply_markup=get_window_keyboard())
        return ADD_WINDOW
    except ValueError:
        await update.message.reply_text("Пожалуйста, введи число. Попробуй снова:")
        return WALL_WIDTH

async def add_window(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "Добавить еще окно":
        await update.message.reply_text("Введи высоту следующего окна (в метрах):",
            reply_markup=ReplyKeyboardMarkup([[]], resize_keyboard=True, one_time_keyboard=True))
        return WINDOW_HEIGHT
    elif text == "Перейти к дверям":
         await update.message.reply_text("Переходим к дверям. Желаете добавить двери?", reply_markup=get_yes_no_keyboard())
         return ASK_DOORS

async def ask_doors(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "Да":
         await update.message.reply_text("Введи высоту двери (в метрах):",
             reply_markup=ReplyKeyboardMarkup([[]], resize_keyboard=True, one_time_keyboard=True))
         return DOOR_HEIGHT
    elif text == "Нет":
        await update.message.reply_text("Выбери тип панели:", reply_markup=get_panel_type_keyboard())
        return PANEL_TYPE

async def door_height(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        height = float(update.message.text)
        if height <= 0:
            await update.message.reply_text("Высота двери должна быть больше нуля. Попробуйте снова:")
            return DOOR_HEIGHT
        if height > 5:
            await update.message.reply_text("Высота двери кажется слишком большой. Пожалуйста, проверьте введенное значение и попробуйте снова:")
            return DOOR_HEIGHT
        context.user_data['current_door'] = {'height': height}
        await update.message.reply_text("Теперь введи ширину двери (в метрах):")
        return DOOR_WIDTH
    except ValueError:
        await update.message.reply_text("Пожалуйста, введи число. Попробуй снова:")
        return DOOR_HEIGHT

async def door_width(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        width = float(update.message.text)
        if width <= 0:
            await update.message.reply_text("Ширина двери должна быть больше нуля. Попробуйте снова:")
            return DOOR_WIDTH
        if width > 3:
            await update.message.reply_text("Ширина двери кажется слишком большой. Пожалуйста, проверьте введенное значение и попробуйте снова:")
            return DOOR_WIDTH
        context.user_data['current_door']['width'] = width
        context.user_data['doors'].append(context.user_data['current_door'])
        await update.message.reply_text("Дверь добавлена. Что дальше?", reply_markup=get_door_keyboard())
        return ADD_DOOR
    except ValueError:
        await update.message.reply_text("Пожалуйста, введи число. Попробуй снова:")
        return DOOR_WIDTH

async def add_door(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "Добавить еще дверь":
       await update.message.reply_text("Введи высоту следующей двери (в метрах):",
            reply_markup=ReplyKeyboardMarkup([[]], resize_keyboard=True, one_time_keyboard=True))
       return DOOR_HEIGHT
    elif text == "Перейти к расчету":
        await update.message.reply_text("Выбери тип панели:", reply_markup=get_panel_type_keyboard())
        return PANEL_TYPE

async def panel_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
     text = update.message.text
     context.user_data['panel_type'] = text
     await update.message.reply_text("Выбери комбинацию панелей:", reply_markup=get_panel_combination_keyboard())
     return PANEL_COMBINATION

async def panel_combination(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    context.user_data['combination'] = text
    
    panels_needed = calculate_panels(
        context.user_data['walls'],
        context.user_data['windows'],
        context.user_data['doors'],
        context.user_data['combination']
    )
    if isinstance(panels_needed, str):
       await update.message.reply_text(panels_needed)
    elif isinstance(panels_needed, dict):
        message = "Тебе понадобится:\n"
        for key, value in panels_needed.items():
            message += f"- {key}: {value} панелей\n"
        await update.message.reply_text(message)
    else:
        await update.message.reply_text(f"Тебе понадобится {panels_needed} панелей.")
    
    await update.message.reply_text("Что вы хотите сделать дальше?", reply_markup=get_cost_or_extras_keyboard()) # Задаем вопрос
    return ASK_COST_OR_EXTRAS

async def ask_cost_or_extras(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text

    if text == "Рассчитать стоимость":
        # TODO: Добавить логику расчета стоимости
        await update.message.reply_text("В разработке...", reply_markup=ReplyKeyboardMarkup([[]], resize_keyboard=True, one_time_keyboard=True))
        return CALCULATE_COST # Переходим к состоянию расчета стоимости
    elif text == "Добавить доборные элементы":
        # Автоматический расчет доборных элементов
        # dobor_elements = await calculate_all_dobor_elements(context)

        # if dobor_elements:
        #     message = "Необходимые доборные элементы:\n"
        #     for element, value in dobor_elements.items():
        #         message += f"- {element}: {value}\n"
        #     await update.message.reply_text(message)
        # else:
        #     await update.message.reply_text("Не удалось рассчитать доборные элементы.")

        # TODO: Определите, к какому состоянию нужно перейти после вывода доборных элементов
        # return ConversationHandler.END  # Завершаем разговор
        
        return await ask_for_corner_details(update, context, CHOOSE_DOBOR_EXECUTION)
    else:
        await update.message.reply_text("Пожалуйста, выберите один из вариантов.")
        return ASK_COST_OR_EXTRAS # Остаемся в этом состоянии