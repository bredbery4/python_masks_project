import pytest

from src.widget import get_date
from src.widget import mask_account_card


@pytest.mark.parametrize(
    "info, expected",
    [
        ("Visa Gold 7000792289606361", "Visa Gold 7000 79** **** 6361"),
        ("Счет 73654108430135874305", "Счет **4305"),
        ("Maestro 1596837493216518", "Maestro 1596 83** **** 6518"),
        ("MasterCard 1234567812345678", "MasterCard 1234 56** **** 5678"),
    ],
)
def test_mask_account_card(info, expected):
    assert mask_account_card(info) == expected


@pytest.mark.parametrize(
    "date_str, expected",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2018-07-11T02:26:18.671407", "11.07.2018"),
        ("2025-12-31T23:59:59", "31.12.2025"),
    ],
)
def test_get_date(date_str, expected):
    assert get_date(date_str) == expected
