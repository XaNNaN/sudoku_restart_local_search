import time
from icecream import ic


def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        exec_time = end_time - start_time
        timing = f"Время выполнения функции {func.__name__}: {exec_time:.8f} сек."
        ic(timing)
        return result
    return wrapper