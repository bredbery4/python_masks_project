import json
from pathlib import Path
from typing import Any
from typing import Dict
from typing import List


def list_json_transactions(file_path: str | Path) -> List[Dict[str, Any]]:
    """Читает JSON-файл и возвращает список словарей с данными о транзакциях.

    Если файл пустой, содержит не список или не найден, возвращает пустой список.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except (FileNotFoundError, json.JSONDecodeError):
        return []
