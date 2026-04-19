from src.processing import filter_by_state
from src.processing import sort_by_date


def test_filter_by_state(sample_operations):
    # Тест стандартного поведения (EXECUTED)
    executed = filter_by_state(sample_operations)
    assert len(executed) == 2
    assert executed[0]["id"] == 1

    # Тест CANCELED
    canceled = filter_by_state(sample_operations, state="CANCELED")
    assert len(canceled) == 1
    assert canceled[0]["id"] == 2

    # Тест несуществующего статуса
    none_list = filter_by_state(sample_operations, state="PENDING")
    assert len(none_list) == 0


def test_sort_by_date(sample_operations):
    # Тест убывания (по умолчанию)
    sorted_list = sort_by_date(sample_operations)
    assert sorted_list[0]["id"] == 3  # 2025 год должен быть первым

    # Тест возрастания
    sorted_list_asc = sort_by_date(sample_operations, reverse=False)
    assert sorted_list_asc[0]["id"] == 4  # 2020 год должен быть первым
