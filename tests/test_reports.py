from src.reports import spending_by_category


def test_spending_by_category():
    assert (
        str(spending_by_category("data/operations.xlsx", "Супермаркеты", "2019-04-10").iloc[1, 1])
        == "2019-04-08 00:00:00"
    )
