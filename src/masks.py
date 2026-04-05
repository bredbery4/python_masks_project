def get_mask_card_number(card_number: int | str) -> str:
    """Функция маскировки номера банковской карты в формате XXXX XX** **** XXXX."""
    card_str = str(card_number)
    # Маскируем: первые 6 цифр (с пробелом) и последние 4
    return f"{card_str[:4]} {card_str[4:6]}** **** {card_str[-4:]}"


def get_mask_account(account_number: int | str) -> str:
    """Функция маскировки номера банковского счета в формате **XXXX."""
    account_str = str(account_number)
    # Маскируем: две звезды и последние 4 цифры
    return f"**{account_str[-4:]}"
