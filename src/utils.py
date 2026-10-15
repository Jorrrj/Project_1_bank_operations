from datetime import  datetime

def get_time_for_greeting():
    """
        Функция возвращает «Доброе утро» / «Добрый день» / «Добрый вечер»
        / «Доброй ночи» в зависимости от текущего времени.
    """
    user_datetime_hour = datetime.now().hour
    if 5 <= user_datetime_hour < 12:
        return "Доброе утро"
    elif 12 <= user_datetime_hour < 18:
        return "Добрый день"
    elif 18 <= user_datetime_hour < 22:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def get_data_time(date_time: str, date_format: str = "%Y-%m-%d %H:%M:%S") -> list[str]:
    dt = datetime.strptime(date_time, date_format)
    start_of_month = dt.replace(day=1)

    return [
        start_of_month.strftime("%d.%m.%Y %H:%M:%S"),
        dt.strftime("%d.%m.%Y %H:%M:%S")
    ]
