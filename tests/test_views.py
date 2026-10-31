import json
from unittest.mock import patch

from src.views import main_info


@patch("src.views.get_currency")
@patch("src.views.get_stock")
def test_main_info(mock_currency, mock_stock, currency, main_result):

    mock_currency.return_value = currency
    mock_stock.return_value = [{"stock": "AMZN", "price": 253.1}]

    assert json.loads(main_info("2019-12-20 15:30:00")) == main_result
