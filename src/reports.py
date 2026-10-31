from datetime import datetime

import pandas as pd


def spending_by_category(path_fo_file: str, category: str, date: str = None) -> dict:
    """
    Функция возвращает траты по заданной категории за
    последние три месяца (от переданной даты)
    """

    df = pd.read_excel(path_fo_file)
    if date is None:
        today = datetime.today()
        date = today.strftime("%Y-%m-%d")
        year = int(today.strftime("%Y"))
        month = int(today.strftime("%m"))
        day = int(today.strftime("%d"))
    else:
        date = datetime.strptime(date, "%Y-%m-%d")
        year = date.year
        month = date.month
        day = date.day
    for i in range(3):
        month = month - 1
        if month == 0:
            month = 12
            year -= 1
    start_day = datetime(year, month, day)

    df["Дата платежа"] = pd.to_datetime(df["Дата платежа"], dayfirst=True)
    transaction = df.loc[start_day <= df["Дата платежа"]].loc[df["Дата платежа"] <= date]
    transaction = transaction[transaction["Категория"] == category]
    return transaction
