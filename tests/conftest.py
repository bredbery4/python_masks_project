import pytest


@pytest.fixture
def sample_operations():
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-03-11T02:26:18.671407"},
        {"id": 2, "state": "CANCELED", "date": "2023-05-20T12:00:00.000000"},
        {"id": 3, "state": "EXECUTED", "date": "2025-01-01T00:00:00.000000"},
        {"id": 4, "date": "2020-01-01T00:00:00.000000"},
    ]
