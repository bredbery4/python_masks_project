from src.masks import get_mask_account
from src.masks import get_mask_card_number


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


def get_date(date_raw: str) -> str:
    """
    Принимает строку с датой в формате "2024-03-11T02:26:18.671407"
    и возвращает строку с датой в формате "11.03.2024".
    """
    # Делим на части по индексам, извлекаем: день (8, 9), месяц (5, 6) и год (0, 1, 2, 3)
    day = date_raw[8:10]
    month = date_raw[5:7]
    year = date_raw[0:4]

    # Возвращаем дату в нужном формате
    return f"{day}.{month}.{year}"
