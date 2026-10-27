import json
import os
from datetime import datetime

import finnhub
import pandas as pd
import requests
from dotenv import load_dotenv
from pandas import DataFrame

load_dotenv()
API_KEY = os.getenv("API_KEY")


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
    """
    Функция принимает конечную дату, переводит в нужный формат и определяет начальную дату.
    """
    dt = datetime.strptime(date_time, date_format)
    start_of_month = dt.replace(day=1)

    return [start_of_month.strftime("%d.%m.%Y %H:%M:%S"), dt.strftime("%d.%m.%Y %H:%M:%S")]


def get_path_and_period(path_fo_file: str, period_date: list) -> DataFrame:
    """
    Функция принимает путь к Excel файлу, и список дат, и возвращает
    таблицу в указанном периоде.
    """
    df = pd.read_excel(path_fo_file, sheet_name="Отчет по операциям")

    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)

    start_date = datetime.strptime(period_date[0], "%d.%m.%Y %H:%M:%S")
    end_date = datetime.strptime(period_date[1], "%d.%m.%Y %H:%M:%S")

    filtered_df = df[(df["Дата операции"] >= start_date) & (df["Дата операции"] <= end_date)]

    sorted_df = filtered_df.sort_values(by="Дата операции", ascending=True)
    return sorted_df


def get_card_with_spend(sorted_df: DataFrame) -> list[dict]:
    """
    Функия принимает DataFrame и возвращает список карт с расходами
    """
    card_spent_transactions = []
    card_sorted = sorted_df[["Номер карты", "Сумма операции", "Кэшбэк", "Сумма операции с округлением"]]
    for index, row in card_sorted.iterrows():
        if row["Сумма операции"] < 0:
            last_digits = str(row["Номер карты"]).replace("*", "")
            total_spent = row["Сумма операции с округлением"]
            cashback = total_spent // 100
            row = {"last_digits": last_digits, "total_spent": total_spent, "cashback": cashback}
            card_spent_transactions.append(row)
    return card_spent_transactions


def get_top_transactions(sorted_df: DataFrame, get_top):
    """
    Функция принимает DataFrame и возвращает get_top топ-транзакций по сумме платежа
    """
    top_pay_transactions = []
    sorted_pay_df = sorted_df.sort_values(by="Сумма операции", ascending=False)
    top_transactions = sorted_pay_df.head(get_top)
    top_transactions_sorted = top_transactions[["Дата платежа", "Сумма операции", "Категория", "Описание"]]

    for index, row in top_transactions_sorted.iterrows():
        transaction = {
            "date": f"{row['Дата платежа']}",
            "amount": f"{row['Сумма операции']}",
            "category": f"{row['Категория']}",
            "description": f"{row['Описание']}",
        }
        top_pay_transactions.append(transaction)

    return top_pay_transactions


def get_currency(path_to_json: str) -> list[dict]:
    """
    Функция принимает на вход path_to_json и возвращает курс валют
    """

    currency_rates = []
    with open(path_to_json, "r", encoding="utf-8") as file:
        data = json.load(file)
        print(data)
        currences = data["user_currencies"]

        for symbols in currences:
            params = {}
            base = "RUB"
            url = f"https://api.apilayer.com/exchangerates_data/latest?symbols={symbols}&base={base}"
            headers = {"apikey": f"{API_KEY}"}
            response = requests.request("GET", url, headers=headers, data=params)

            result = response.json()
            print(result)
            currency_code_response = round(result["rates"][f"{symbols}"], 2)
            currency_rates.append({"currency": f"{symbols}", "rate": f"{currency_code_response}"})

        return currency_rates


def get_stock(path_to_json: str) -> list[dict]:
    stock_rates = []
    finnhub_client = finnhub.Client(api_key=os.getenv("API_KEY_2"))

    with open(path_to_json, "r", encoding="utf-8") as file:
        data = json.load(file)
        stocks = data["user_stocks"]

        for stock in stocks:
            price = finnhub_client.quote(stock)
            stock_rates.append({"stock": stock, "price": round(price["c"], 2)})
    return stock_rates
