# dobor.py
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
import math

# Размеры откосов (глубина)
OPENING_DEPTHS = [50, 100, 150, 200, 250, 300, 400] #в мм
# Размеры рамок
FRAME_WIDTHS = [40, 60, 80, 100, 120] #в мм

# Размеры угловых элементов
FLAT_CORNER_SIZES = ["80x80", "100x100", "120x120", "150x150"]
VOLUME_CORNER_SIZES = ["150x150", "200x200"]

def get_opening_depth_keyboard():
    keyboard = [[InlineKeyboardButton(str(depth), callback_data=f"depth:{depth}")] for depth in OPENING_DEPTHS]
    return InlineKeyboardMarkup(keyboard)

def get_frame_width_keyboard():
    keyboard = [[InlineKeyboardButton(str(width), callback_data=f"width:{width}")] for width in FRAME_WIDTHS]
    return InlineKeyboardMarkup(keyboard)

# Клавиатура для выбора исполнения доборных элементов (плоские или объемные)
def get_dobor_execution_keyboard():
    keyboard = [
        [InlineKeyboardButton("Плоские", callback_data="execution:Плоские")],
        [InlineKeyboardButton("Объемные", callback_data="execution:Объемные")],
    ]
    return InlineKeyboardMarkup(keyboard)

# Клавиатура для выбора размера углового элемента
def get_corner_size_keyboard(execution):
    keyboard = []
    sizes = FLAT_CORNER_SIZES if execution == "Плоские" else VOLUME_CORNER_SIZES
    for size in sizes:
        keyboard.append([InlineKeyboardButton(size, callback_data=f"corner_size:{size}")])
    return InlineKeyboardMarkup(keyboard)

async def calculate_all_dobor_elements(context: ContextTypes.DEFAULT_TYPE) -> dict:
   execution = context.user_data.get('dobor_execution')

   if execution == "Плоские":
      return await calculate_flat_openings(context)
   elif execution == "Объемные":
       return await calculate_volume_openings(context)
   else:
       return {} #TODO: Обработать ошибку

# Функции расчета для плоских откосов
async def calculate_flat_openings(context: ContextTypes.DEFAULT_TYPE) -> dict:
    dobor_elements = {}
    windows = context.user_data.get('windows', [])
    opening_depth = context.user_data.get('opening_depth')
    frame_width = context.user_data.get('frame_width')
    otkos_length = 2500

    for window in windows:
        window_height = window['height']
        window_width = window['width']

        # Боковые откосы
        side_otkos_needed = math.ceil((2 * window_height) / otkos_length)
        # Верхний откос
        top_otkos_needed = math.ceil(window_width / otkos_length)
        # Отлив
        otliv_needed = math.ceil(window_width / otkos_length)

        dobor_elements["Откосы"] = f"{side_otkos_needed + top_otkos_needed } шт."
        dobor_elements["Отливы"] = f"{otliv_needed} шт."
    return dobor_elements

# Функции расчета для объемных откосов
async def calculate_volume_openings(context: ContextTypes.DEFAULT_TYPE) -> dict:
    dobor_elements = {}
    windows = context.user_data.get('windows', [])
    opening_depth = context.user_data.get('opening_depth')
    frame_width = context.user_data.get('frame_width')
    otkos_length = 2500

    for window in windows:
        window_height = window['height']
        window_width = window['width']

        # Боковые откосы
        side_otkos_needed = math.ceil((2 * window_height) / otkos_length)
        # Верхний откос
        top_otkos_needed = math.ceil(window_width / otkos_length)

        dobor_elements["Откосы"] = f"{side_otkos_needed + top_otkos_needed } шт."
    return dobor_elements

async def ask_for_corner_details(update: Update, context: ContextTypes.DEFAULT_TYPE, CHOOSE_DOBOR_EXECUTION) -> int:
     await update.callback_query.message.reply_text(
        "Выберите исполнение для углов:",
        reply_markup=get_dobor_execution_keyboard(),
    )
     return CHOOSE_DOBOR_EXECUTION

async def dobor_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    data = query.data
    if data.startswith("execution:"):
        execution = data[len("execution:"):]
        context.user_data['dobor_execution'] = execution
        # if(context.user_data['current_dobor_element'] == "Угол"):
        #     await query.edit_message_text(text=f"Вы выбрали исполнение '{execution}'.", reply_markup=get_corner_size_keyboard(execution))
        #     return CHOOSE_CORNER_SIZE
        # else:
        await query.edit_message_text(text=f"Вы выбрали исполнение '{execution}'.", reply_markup=get_opening_depth_keyboard())
        return CHOOSE_OPENING_DEPTH
    if data.startswith("depth:"):
       depth = int(data[len("depth:"):])
       context.user_data['opening_depth'] = depth
       await query.edit_message_text(text="Выберите ширину рамки (мм):", reply_markup=get_frame_width_keyboard())
       return CHOOSE_FRAME_WIDTH
    elif data.startswith("width:"):
         width = int(data[len("width:"):])
         context.user_data['frame_width'] = width
         if context.user_data['dobor_execution'] == "Плоские":
            dobor_elements = await calculate_flat_otkosi_otlivi(context)
         elif  context.user_data['dobor_execution'] == "Объемные":
             dobor_elements = await calculate_volume_otkosi_otlivi(context)
         message = "Необходимые доборные элементы:\n"
         for element, value in dobor_elements.items(): # Выводим информацию об остальных элементов
           message += f"- {element}: {value}\n"
         await query.edit_message_text(text=message)
         return ConversationHandler.END
