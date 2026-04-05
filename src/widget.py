from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(card_info: str) -> str:
    """
    Принимает одну строку (тип и номер) и возвращает строку с маской.
    Использует функции из модуля masks.
    """
    # Принимаем один аргумент card_info. Внутри разделяем его на элементы списка.
    parts = card_info.split()

    # Номер всегда в конце, извлекаем его
    number = parts[-1]

    # Все слова до номера собираем обратно в название типа (Visa, Счет и т.д.)
    type_name = " ".join(parts[:-1])

    # Выбираем нужную маску в зависимости от типа
    if type_name.lower() == "счет":
        return f"{type_name} {get_mask_account(number)}"
    else:
        return f"{type_name} {get_mask_card_number(number)}"