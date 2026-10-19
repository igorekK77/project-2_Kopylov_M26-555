import time
from functools import wraps


def handle_db_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError as e:
            print(f"Ошибка: не найден ключ {e}")
        except (ValueError, TypeError) as e:
            print(f"Ошибка: {e}")
        except FileNotFoundError as e:
            print(f"Ошибка: файл не найден. {e}")
    return wrapper

def confirm_action(action_name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"Вы уверены, что хотите выполнить \"{action_name}\"? [y/n]:")
            answer_user = input("Введите ответ: ")
            if answer_user == "y":
                return func(*args, **kwargs)
            else:
                print(f"Операция {action_name} не выполнена")
                return None
        return wrapper
    return decorator

def log_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.monotonic()
        result = func(*args, **kwargs)
        finish = time.monotonic()
        result_time = finish - start
        print(f"Функция {func.__name__} выполнилась за {result_time:.3f} секунд")
        return result
    return wrapper

def create_cacher():
    cash = {}
    def cache_result(key, value_func):
        if key in cash:
            return cash[key]
        else:
            result = value_func()
            cash[key] = result
            return result
    return cache_result