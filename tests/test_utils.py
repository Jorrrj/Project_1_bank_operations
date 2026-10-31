from unittest.mock import MagicMock, patch

from src.utils import (get_card_with_spend, get_currency, get_data_time, get_path_and_period, get_stock,
                       get_time_for_greeting, get_top_transactions)


@patch("src.utils.datetime")
def test_get_time_for_greeting_1(mock_time):
    mock_time.now.return_value.hour = 10
    assert get_time_for_greeting() == "Доброе утро"


@patch("src.utils.datetime")
def test_get_time_for_greeting_2(mock_time):
    mock_time.now.return_value.hour = 13
    assert get_time_for_greeting() == "Добрый день"


@patch("src.utils.datetime")
def test_get_time_for_greeting_3(mock_time):
    mock_time.now.return_value.hour = 19
    assert get_time_for_greeting() == "Добрый вечер"


@patch("src.utils.datetime")
def test_get_time_for_greeting_4(mock_time):
    mock_time.now.return_value.hour = 23
    assert get_time_for_greeting() == "Доброй ночи"


def test_get_data_time():
    assert get_data_time("2019-04-10 15:30:00") == ["01.04.2019 15:30:00", "10.04.2019 15:30:00"]


@patch("pandas.read_excel")
def test_get_path_and_period(mock_pd, read_pd_1):
    mock_pd.return_value = read_pd_1
    period = ["01.03.2020 15:30:00", "20.03.2020 15:30:00"]
    assert str(get_path_and_period(", ", period).iloc[1, 1]) == "19.03.2020"


def test_get_card_with_spend(read_pd_1):
    assert get_card_with_spend(read_pd_1)[0]["last_digits"] == "1111111111111112"


def test_get_top_transactions(read_pd_1):
    assert get_top_transactions(read_pd_1, 3)[0]["amount"] == "800"


@patch("src.utils.requests.request")
@patch("src.utils.json.load")
def test_get_currency(mock_json, mock_api, currency):
    mock_response = MagicMock()
    mock_response.json.return_value = {"success": True, "base": "RUB", "rates": {"USD": 0.012415}}
    mock_api.return_value = mock_response
    mock_json.return_value = {
        "user_currencies": [
            "USD",
        ]
    }
    assert get_currency("data/user_settings.json") == currency


@patch("src.utils.finnhub.Client")
@patch("src.utils.json.load")
def test_get_stock(mock_json, mock_api):

    mock_api.return_value.quote.return_value = {"c": 253.1}
    mock_json.return_value = {
        "user_stocks": [
            "AMZN",
        ]
    }
    assert get_stock("data/user_settings.json") == [{"stock": "AMZN", "price": 253.1}]
