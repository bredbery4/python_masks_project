from unittest.mock import MagicMock
from unittest.mock import patch

from src.external_api import convert_transaction_amount


def test_convert_transaction_amount_rub() -> None:
    """Проверка, что транзакции в RUB возвращаются как есть, без обращения к API."""
    transaction = {
        "operationAmount": {
            "amount": "1500.50",
            "currency": {"name": "руб.", "code": "RUB"}
        }
    }
    result = convert_transaction_amount(transaction)
    assert result == 1500.50


@patch("os.getenv")
@patch("requests.get")
def test_convert_transaction_amount_usd_success(mock_get: MagicMock, mock_getenv: MagicMock) -> None:
    """Успешный тест конвертации USD в RUB с фейковым ответом от сервера."""
    mock_getenv.return_value = "fake_api_key"

    # Имитируем успешный HTTP-ответ от сервера
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": 7500.00}
    mock_get.return_value = mock_response

    transaction = {
        "operationAmount": {
            "amount": "100.00",
            "currency": {"name": "USD", "code": "USD"}
        }
    }
    result = convert_transaction_amount(transaction)
    assert result == 7500.00


@patch("os.getenv")
@patch("requests.get")
def test_convert_transaction_amount_api_error(mock_get: MagicMock, mock_getenv: MagicMock) -> None:
    """Тест сценария, когда внешнее API вернуло ошибку."""
    mock_getenv.return_value = "fake_api_key"

    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_get.return_value = mock_response

    transaction = {
        "operationAmount": {
            "amount": "50.00",
            "currency": {"name": "EUR", "code": "EUR"}
        }
    }
    result = convert_transaction_amount(transaction)
    assert result == 0.0
