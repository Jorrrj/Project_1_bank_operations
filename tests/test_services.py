import json

from src.services import anylize_cashback


def test_anylize_cashback():
    assert json.loads(anylize_cashback("data/operations.xlsx", 2019, 4)) == {
        "Ж/д билеты": 74.0,
        "Различные товары": 4.0,
        "Транспорт": 5.0,
    }
