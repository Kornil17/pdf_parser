import logging
from os import path
from argparse import ArgumentParser
from sys import argv

from utils.logger import setup_logger

from modules.executor import Executor

def main() -> None:
    """
    Функция запуска работы скрипта.

    :return: None
    """
    try:
        setup_logger()
        if len(argv) < 2:
            logging.error('Необходимо передавать обязательные параметры для работы скрипта.\n')
        parser = ArgumentParser()
        parser.add_argument('--file', type=str, required=True, help='Путь до PDF файла/файлов.')
        args = parser.parse_args()
        executor = Executor(input_path=args.file)
        executor.process_files()
    except Exception as ex:
        logging.error(f'Работа скрипта завершилась с ошибкой.', exc_info=ex)


if __name__ == '__main__':
    main()



