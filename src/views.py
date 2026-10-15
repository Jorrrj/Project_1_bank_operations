import json
from pkgutil import get_data
from typing import Dict, Any

from src.utils import get_time_for_greeting, get_data_time


def main_info(date_time: str) -> Dict[str, Any]:
    """
        Главная функция, принимающая на вход строку с датой и временем
        в формате YYYY-MM-DD HH:MM:SS и возвращает JSON-ответ
        2018-05-20 15:30:00
    """

    greeting = get_time_for_greeting() # Определяет текущее время пользователя и выдает какое сейчас время
    time_period = get_data_time(date_time)
    print(time_period)

    data = {
        "greeting": greeting
    }

    json_data = json.dumps(data, ensure_ascii=False, indent=4)

    return json_data



