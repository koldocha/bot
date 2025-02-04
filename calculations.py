# calculations.py
import math
from config import NARROW_PANEL_AREA, MEDIUM_PANEL_AREA, WIDE_PANEL_AREA, WASTE_PERCENTAGE

def calculate_panels(walls, windows, doors, combination):
    # Вычисляем общую площадь стен
    total_area = sum(wall['height'] * wall['width'] for wall in walls)
    total_area -= sum(window['height'] * window['width'] for window in windows)
    total_area -= sum(door['height'] * door['width'] for door in doors)

    if total_area <= 0:
        return "Неверно указаны размеры стен и проёмов"

    # Добавляем процент запаса
    total_area *= (1 + WASTE_PERCENTAGE)

    if combination == "Только узкая":
        panels_needed = total_area / NARROW_PANEL_AREA
        return math.ceil(panels_needed)

    elif combination == "Только средняя":
        panels_needed = total_area / MEDIUM_PANEL_AREA
        return math.ceil(panels_needed)

    elif combination == "Только широкая":
        panels_needed = total_area / WIDE_PANEL_AREA
        return math.ceil(panels_needed)

    elif combination == "Классическая":
        medium_area = total_area * 0.7
        narrow_area = total_area * 0.3

        medium_needed = medium_area / MEDIUM_PANEL_AREA
        narrow_needed = narrow_area / NARROW_PANEL_AREA
        return {
            "узкая": math.ceil(narrow_needed),
            "средняя": math.ceil(medium_needed)
        }

    elif combination == "Сложная":
        # Делим площадь на три равные части
        narrow_area = total_area / 3
        medium_area = total_area / 3
        wide_area = total_area / 3

        narrow_needed = narrow_area / NARROW_PANEL_AREA
        medium_needed = medium_area / MEDIUM_PANEL_AREA
        wide_needed = wide_area / WIDE_PANEL_AREA

        return {
            "узкая": math.ceil(narrow_needed),
            "средняя": math.ceil(medium_needed),
            "широкая": math.ceil(wide_needed)
        }

    # По умолчанию возвращаем расчет для узких панелей (это можно убрать, если всегда ожидается выбор комбинации)
    return math.ceil(total_area / NARROW_PANEL_AREA)