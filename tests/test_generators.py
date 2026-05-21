import pytest

from src.generators import card_number_generator
from src.generators import filter_by_currency
from src.generators import transaction_descriptions


def test_filter_by_currency_standard():
    """Проверка корректной фильтрации транзакций по заданной валюте."""
    transactions = [
        {
            "id": 939719570,
            "operationAmount": {"currency": {"code": "USD"}}
        },
        {
            "id": 142264268,
            "operationAmount": {"currency": {"code": "USD"}}
        },
        {
            "id": 111111111,
            "operationAmount": {"currency": {"code": "RUB"}}
        }
    ]

    # Вызываем генератор для USD
    usd_transactions = filter_by_currency(transactions, "USD")
    result = list(usd_transactions)

    # Проверяем, что вернулось ровно 2 транзакции
    assert len(result) == 2
    # Проверяем, что отфильтровались именно нужные транзакции по их id
    assert result[0]["id"] == 939719570
    assert result[1]["id"] == 142264268


def test_filter_by_currency_no_match():
    """Проверка, когда транзакции в заданной валюте отсутствуют."""
    transactions = [
        {"operationAmount": {"currency": {"code": "RUB"}}},
        {"operationAmount": {"currency": {"code": "EUR"}}}
    ]

    # Ищем USD, которых в списке нет
    usd_transactions = filter_by_currency(transactions, "USD")
    result = list(usd_transactions)

    # Должен вернуться пустой список
    assert result == []


def test_filter_by_currency_empty_list():
    """Проверка, что генератор не завершается ошибкой при обработке пустого списка."""
    transactions = []

    usd_transactions = filter_by_currency(transactions, "USD")
    result = list(usd_transactions)

    # Пустой список на входе — пустой список на выходе, без ошибок выполнения
    assert result == []


def test_filter_by_currency_missing_keys():
    """Проверка, что генератор не падает, если в данных нет валютных операций или ключей."""
    transactions = [
        {"operationAmount": {}},                 # Нет ключа 'currency'
        {"id": 12345},                           # Вообще нет 'operationAmount'
        {"operationAmount": {"currency": {}}}    # Нет ключа 'code'
    ]

    usd_transactions = filter_by_currency(transactions, "USD")
    result = list(usd_transactions)

    # Генератор должен безопасно пропустить некорректные словари
    assert result == []


def test_transaction_descriptions_correct_values():
    """Проверяет, что функция возвращает корректные описания для каждой транзакции."""
    transactions = [
        {"id": 1, "description": "Перевод организации"},
        {"id": 2, "description": "Перевод со счета на счет"},
    ]

    result = list(transaction_descriptions(transactions))

    # Просто проверяем, что описания вытащились правильно
    assert result == ["Перевод организации", "Перевод со счета на счет"]


def test_transaction_descriptions_empty_list():
    """Проверяет работу функции с пустым списком."""
    transactions = []

    result = list(transaction_descriptions(transactions))

    # Если список пустой, то и результат должен быть пустым
    assert result == []


def test_transaction_descriptions_one_element():
    """Проверяет работу функции с одной транзакцией."""
    transactions = [{"id": 1, "description": "Перевод с карты на карту"}]

    result = list(transaction_descriptions(transactions))

    # Проверяем, что с одним элементом тоже всё работает
    assert result == ["Перевод с карты на карту"]


def test_transaction_descriptions_five_elements():
    """Проверяет работу функции с пятью транзакциями (как в примере)."""
    transactions = [
        {"description": "Перевод организации"},
        {"description": "Перевод со счета на счет"},
        {"description": "Перевод со счета на счет"},
        {"description": "Перевод с карты на карту"},
        {"description": "Перевод организации"},
    ]

    result = list(transaction_descriptions(transactions))

    # Проверяем, что вернулось ровно 5 описаний
    assert len(result) == 5
    assert result[0] == "Перевод организации"
    assert result[4] == "Перевод организации"


@pytest.fixture
def expected_five_cards():
    """Фикстура, которая возвращает правильный список из 5 карт для теста (от 1 до 5)."""
    return [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003",
        "0000 0000 0000 0004",
        "0000 0000 0000 0005",
    ]


def test_card_number_generator_standard(expected_five_cards):
    """Проверяет правильный диапазон и формат номеров карт (использует фикстуру)."""
    gen = card_number_generator(1, 5)
    result = list(gen)

    # Проверяем, что карты в точности совпадают с нашей фикстурой
    assert result == expected_five_cards


@pytest.mark.parametrize(
    "start, end, expected_len, first_card, last_card",
    [
        # Тест 1: Крайнее нижнее значение (карта №1)
        (1, 1, 1, "0000 0000 0000 0001", "0000 0000 0000 0001"),
        # Тест 2: Диапазон побольше (с 10 по 12)
        (10, 12, 3, "0000 0000 0000 0010", "0000 0000 0000 0012"),
        # Тест 3: Проверка смены разрядов (с 99 по 101)
        (99, 101, 3, "0000 0000 0000 0099", "0000 0000 0000 0101"),
    ],
)
def test_card_number_generator_ranges(
    start, end, expected_len, first_card, last_card
):
    """Параметризованный тест: проверяет разные диапазоны, длины и крайние значения."""
    gen = card_number_generator(start, end)
    result = list(gen)

    # 1. Проверяем, что сгенерировалось правильное количество карт
    assert len(result) == expected_len

    # 2. Проверяем, что первая карта в диапазоне правильная
    assert result[0] == first_card

    # 3. Проверяем, что генератор правильно завершился на последней карте
    assert result[-1] == last_card
