import json
from unittest.mock import mock_open
from unittest.mock import patch

from src.utils import list_json_transactions


def test_list_json_transactions_success() -> None:
    """Тест успешного чтения корректного JSON-файла."""
    mock_data = [{"id": 1, "description": "Перевод"}]
    mock_json = json.dumps(mock_data)

    with patch("builtins.open", mock_open(read_data=mock_json)):
        result = list_json_transactions("fake_path.json")
        assert result == mock_data


def test_list_json_transactions_file_not_found() -> None:
    """Тест сценария, когда файл физически отсутствует."""
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = list_json_transactions("missing.json")
        assert result == []


def test_list_json_transactions_invalid_json() -> None:
    """Тест сценария, когда JSON-файл сломан или пуст."""
    with patch("builtins.open", mock_open(read_data="invalid json data")):
        result = list_json_transactions("bad.json")
        assert result == []


def test_list_json_transactions_not_a_list() -> None:
    """Тест сценария, когда в JSON лежит словарь вместо списка транзакций."""
    mock_dict = {"status": "error"}
    with patch("builtins.open", mock_open(read_data=json.dumps(mock_dict))):
        result = list_json_transactions("dict.json")
        assert result == []
