import pytest

from src.masks import get_mask_account
from src.masks import get_mask_card_number


@pytest.mark.parametrize(
    "card, expected",
    [
        ("7000792289606361", "7000 79** **** 6361"),
        (1234567812345678, "1234 56** **** 5678"),
        ("12345678", "1234 56** **** 5678"),
    ],
)
def test_get_mask_card_number(card, expected):
    assert get_mask_card_number(card) == expected


@pytest.mark.parametrize(
    "account, expected",
    [
        ("73654108430135874305", "**4305"),
        (73654108430135874305, "**4305"),
        ("123", "**123"),  # Очень короткий номер
    ],
)
def test_get_mask_account(account, expected):
    assert get_mask_account(account) == expected
