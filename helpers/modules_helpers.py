from concurrent.futures import ThreadPoolExecutor
from os import cpu_count
from typing import Callable, Iterator


def run_pool_executor(func: Callable, params: Iterator) -> Iterator:
    """
    Функция запуска пула потоков.

    :param func: Вызываемая функция обработки в потоках.
    :param params: Параметры функции.
    :return: Итератор результатов.
    """
    with ThreadPoolExecutor(cpu_count()) as executor:
        results = executor.map(func, params)
    return results
