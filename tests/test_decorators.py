import pytest

from src.decorators import log


def test_log_console_success(capsys):
    """Проверка успешного выполнения функции с выводом лога в консоль."""

    @log()
    def my_sum(a, b):
        return a + b

    result = my_sum(4, 5)

    # 1. Проверяем, что сама функция вернула верный результат
    assert result == 9

    # 2. Перехватываем print() через capsys и проверяем сообщение
    captured = capsys.readouterr()
    assert captured.out.strip() == "my_sum ok"


def test_log_console_error(capsys):
    """Проверка перехвата ошибки с выводом деталей в консоль."""

    @log()
    def my_div(a, b):
        return a / b

    # 1. Проверяем, что декоратор НЕ проглотил ошибку, а выбросил её наружу (raise e)
    with pytest.raises(ZeroDivisionError):
        my_div(10, 0)

    # 2. Проверяем точный формат вывода ошибки в консоль
    captured = capsys.readouterr()
    expected_message = "my_div error: ZeroDivisionError. Inputs: (10, 0), {}"
    assert captured.out.strip() == expected_message


def test_log_file_success(tmp_path):
    """Проверка успешного выполнения функции с записью лога в файл."""
    # tmp_path — это встроенная фикстура pytest для создания временных файлов
    test_file = tmp_path / "success.log"

    @log(filename=str(test_file))
    def greet(name):
        return f"Hello, {name}"

    result = greet("Masha")

    assert result == "Hello, Masha"
    # Проверяем, что файл физически создался
    assert test_file.exists()

    # Читаем лог и сверяем строку
    file_content = test_file.read_text(encoding='utf-8').strip()
    assert file_content == "greet ok"


def test_log_file_error(tmp_path):
    """Проверка перехвата ошибки с записью детального лога в файл."""
    test_file = tmp_path / "error.log"

    @log(filename=str(test_file))
    def process_data(x, mode="fast"):
        raise ValueError(f"Invalid data for {x} with mode {mode}")

    with pytest.raises(ValueError):
        process_data(100, mode="slow")

    assert test_file.exists()
    file_content = test_file.read_text(encoding='utf-8').strip()

    # Проверяем, что в файл записались имя, тип ошибки и переданные args/kwargs
    assert "process_data error" in file_content
    assert "ValueError" in file_content
    assert "(100,)" in file_content
    assert "{'mode': 'slow'}" in file_content
