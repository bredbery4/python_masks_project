import os
from typing import Any
from typing import Dict

import requests
from dotenv import load_dotenv

# Загружаем переменные из .env файла
load_dotenv()


def convert_transaction_amount(transaction: Dict[str, Any]) -> float:
    """Возвращает сумму транзакции в рублях (тип float).

    Если валюта USD или EUR, запрашивает курс через Exchange Rates Data API.
    """
    operation_amount = transaction.get("operationAmount", {})
    amount_str = operation_amount.get("amount", "0")
    currency_info = operation_amount.get("currency", {})
    currency_code = currency_info.get("code", "RUB")

    try:
        amount = float(amount_str)
    except (ValueError, TypeError):
        return 0.0

    if currency_code == "RUB":
        return amount

    if currency_code in ("USD", "EUR"):
        api_key = os.getenv("API_KEY")
        if not api_key:
            return 0.0

        url = f"https://apilayer.com{currency_code}&amount={amount}"
        headers = {"apikey": api_key}

        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return float(data.get("result", 0.0))
        except requests.RequestException:
            return 0.0

    return 0.0
