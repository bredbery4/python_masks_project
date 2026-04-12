def filter_by_state(operations: list[dict], state: str = "EXECUTED") -> list[dict]:
    """
        Функция возвращает новый список словарей, содержащий только те словари, у которых ключ
    state соответствует указанному значению
    """
    filtered_list = []

    # Идем циклом по каждой операции (словарю) в исходном списке
    for op in operations:
        # Если у операции есть ключ 'state' и он равен нашему статусу
        if op.get("state") == state:
            # Добавляем эту операцию в наш новый список
            filtered_list.append(op)
    return filtered_list
