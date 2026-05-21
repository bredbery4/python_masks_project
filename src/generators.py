from typing import Any
from typing import Iterator


def filter_by_currency(transactions: list[dict[str, Any]], currency: str) -> Iterator[dict[str, Any]]:
    """Фильтрует транзакции по заданной валюте и возвращает итератор."""
    for transaction in transactions:
        if (
            "operationAmount" in transaction
            and "currency" in transaction["operationAmount"]
            and transaction["operationAmount"]["currency"].get("code") == currency
        ):
            yield transaction


def transaction_descriptions(transactions: list[dict]) -> Iterator[str]:
    """Принимает список словарей с транзакциями и возвращает описание каждой операции по очереди."""
    for transaction in transactions:
        yield transaction.get("description", "")


def card_number_generator(start: int, end: int) -> Iterator[str]:
    """Генератор, который выдает номера карт в формате XXXX XXXX XXXX XXXX."""
    for number in range(start, end + 1):
        # Переводим число в строку (например, число 1 становится строкой "1")
        num_str = str(number)

        # Считаем, сколько нулей не хватает до 16 символов
        needed_zeros = 16 - len(num_str)

        # Создаем нужную цепочку нулей и прибавляем к ней наше число
        # Если число "1", то (16 - 1) = 15 нулей. Плюсуем "1" и получаем "0000000000000001"
        card_str = ("0" * needed_zeros) + num_str

        # Нарезаем готовую 16-значную строку по 4 символа через пробел
        formatted_card = (
            f"{card_str[0:4]} {card_str[4:8]} {card_str[8:12]} {card_str[12:16]}"
        )

        yield formatted_card
