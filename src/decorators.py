import time
from functools import wraps

from src.constants import CONFIRMATION_POSITIVE_ANSWER


def handle_db_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            print("Ошибка: Файл данных не найден. Возможно, база данных не инициализирована.")
        except KeyError as error:
            print(f"Ошибка: Таблица или столбец {error} не найден.")
        except ValueError as error:
            print(f"Ошибка валидации: {error}")
        except Exception as error:
            print(f"Произошла непредвиденная ошибка: {error}")

    return wrapper


def confirm_action(action_name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            answer = input(f'Вы уверены, что хотите выполнить "{action_name}"? [y/n]: ').strip().lower()
            if answer != CONFIRMATION_POSITIVE_ANSWER:
                print("Операция отменена.")
                return args[0] if args else None
            return func(*args, **kwargs)

        return wrapper

    return decorator


def log_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.monotonic()
        try:
            return func(*args, **kwargs)
        finally:
            duration = time.monotonic() - start
            print(f"Функция {func.__name__} выполнилась за {duration:.3f} секунд.")

    return wrapper


def create_cacher():
    cache = {}

    def cache_result(key, value_func):
        if key in cache:
            return cache[key]
        value = value_func()
        cache[key] = value
        return value

    def clear():
        cache.clear()

    cache_result.clear = clear
    return cache_result


