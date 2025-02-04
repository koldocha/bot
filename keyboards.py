# keyboards.py
from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

def get_contact_keyboard():
    return ReplyKeyboardMarkup(
        [[KeyboardButton("Поделиться контактом", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )

def get_wall_keyboard():
    return ReplyKeyboardMarkup(
        [[KeyboardButton("Добавить еще стену"), KeyboardButton("Перейти к проемам")]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )

def get_window_keyboard():
    return ReplyKeyboardMarkup(
        [[KeyboardButton("Добавить еще окно"), KeyboardButton("Перейти к дверям")]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )

def get_door_keyboard():
    return ReplyKeyboardMarkup(
        [[KeyboardButton("Добавить еще дверь"), KeyboardButton("Перейти к расчету")]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )

def get_panel_type_keyboard():
    return ReplyKeyboardMarkup(
        [[KeyboardButton("ПЭП (Глянец)"), KeyboardButton("Шагрень (Матовый)"), KeyboardButton("Под дерево")]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )

def get_panel_combination_keyboard():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("Только узкая"), KeyboardButton("Только средняя")],
            [KeyboardButton("Только широкая"), KeyboardButton("Классическая")],
            [KeyboardButton("Сложная")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    
def get_yes_no_keyboard():
     return ReplyKeyboardMarkup(
         [[KeyboardButton("Да"), KeyboardButton("Нет")]],
         resize_keyboard=True,
         one_time_keyboard=True
     )

def get_cost_or_extras_keyboard():
    return ReplyKeyboardMarkup(
        [[KeyboardButton("Рассчитать стоимость"), KeyboardButton("Добавить доборные элементы")]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )

def get_opening_depth_keyboard():
    OPENING_DEPTHS = [50, 100, 150, 200, 250, 300, 400] #в мм
    keyboard = [[InlineKeyboardButton(str(depth), callback_data=f"depth:{depth}")] for depth in OPENING_DEPTHS]
    return InlineKeyboardMarkup(keyboard)

def get_frame_width_keyboard():
    FRAME_WIDTHS = [40, 60, 80, 100, 120] #в мм
    keyboard = [[InlineKeyboardButton(str(width), callback_data=f"width:{width}")] for width in FRAME_WIDTHS]
    return InlineKeyboardMarkup(keyboard)

def get_dobor_execution_keyboard():
    keyboard = [
        [InlineKeyboardButton("Плоские", callback_data="execution:Плоские")],
        [InlineKeyboardButton("Объемные", callback_data="execution:Объемные")],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_corner_size_keyboard(execution):
    FLAT_CORNER_SIZES = ["80x80", "100x100", "120x120", "150x150"]
    VOLUME_CORNER_SIZES = ["150x150", "200x200"]
    keyboard = []
    sizes = FLAT_CORNER_SIZES if execution == "Плоские" else VOLUME_CORNER_SIZES
    for size in sizes:
        keyboard.append([InlineKeyboardButton(size, callback_data=f"corner_size:{size}")])
    return InlineKeyboardMarkup(keyboard)