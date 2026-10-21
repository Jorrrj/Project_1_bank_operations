import pandas as pd


def spending_by_category(transactions: pd.DataFrame, category: str, date: str) -> dict:
    """
        Функция возвращает траты по заданной категории за
        последние три месяца (от переданной даты)
    """
    print(transactions)

