import functools


def log(filename=None):
    """Декоратор верхнего уровня. Принимает имя файла для логирования.

       Args:
           filename (str, optional): Путь к файлу логирования. Если None, вывод идет в консоль.
       """
    def decorator(func):
        """Промежуточный декоратор, принимающий саму декорируемую функцию."""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """Обертка функции. Выполняет логирование результата или перехваченной ошибки."""
            try:
                result = func(*args, **kwargs)
                message = f"{func.__name__} ok"

                # Пишем в файл или в консоль
                if filename:
                    with open(filename, 'a', encoding='utf-8') as f:
                        f.write(message + '\n')
                else:
                    print(message)
                return result

            except Exception as e:
                message = f"{func.__name__} error: {type(e).__name__}. Inputs: {args}, {kwargs}"

                # Пишем в файл или в консоль
                if filename:
                    with open(filename, 'a', encoding='utf-8') as f:
                        f.write(message + '\n')
                else:
                    print(message)
                raise e

        return wrapper

    return decorator
