from datetime import datetime

import pandas as pd

from src.reports import spending_by_category
from src.services import anylize_cashback
from src.views import main_info

def main():
    user_1 = input("Вас приветствует программа банковских операций,\n"
    "укажите дату окончания периода для вывода транзакций.\n например 2019-04-10 15:30:00\n")
    # home = main_info(user_1)
    # print(home)
    while True:
        user_2 = input("Доступный функционал:\n"
                       "1. Выгодные категории повышенного кешбэка\n"
                       "2. Траты по категории\n"
                       "3. Выход\n")
        if user_2 == "1":
            year = int(input("Укажите год за который ищем повышенный кешбэк\n"))
            month = int(input("Укажите месяц за который ищем повышенный кешбэк\n"))
            print(anylize_cashback("data/operations.xlsx", year, month))
        elif user_2 == "2":
            category = input("Укажите категорию для фильтрации\n").capitalize()
            date = input("Укажите дату окончания периода для вывода транзакций\n например 2019-04-10 15:30:00\n")
            print(spending_by_category("data/operations.xlsx", category, date))
        elif user_2 == "3":
            print("Спасибо что пользуетесь нашим сервисом")
            break
        else:
            print("Не верно введенные данные")


if __name__ == '__main__':
    main()
