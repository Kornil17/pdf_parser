import logging
from datetime import datetime
from os import makedirs, path

from modules.settings import settings


class ColoredFormatter(logging.Formatter):
    """Форматирование логов с цветом."""

    RESET = "\033[0m"
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"

    def format(self, record):
        if record.levelno == logging.INFO:
            record.msg = f"{self.GREEN}{record.msg}{self.RESET}"
        elif record.levelno == logging.ERROR:
            record.msg = f"{self.RED}{record.msg}{self.RESET}"
        return super().format(record)


def setup_logger() -> str:
    """Настройка логирования."""
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Создание папки для логов, если она не существует
    log_dir = path.join(path.abspath('.'), './logs_pdf_parser')
    if not path.exists(log_dir):
        makedirs(log_dir)

    # Формирование имени файла с логами
    log_file_name = f'logs_pdf_parser_service_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.log'
    log_file_path = path.join(log_dir, log_file_name)

    # Создание обработчика для записи логов в файл
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(getattr(logging, settings.file_handler_level.upper()))

    # Форматирование логов
    formatter = ColoredFormatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Создание обработчика для вывода логов в консоль
    ch = logging.StreamHandler()
    ch.setLevel(getattr(logging, settings.console_handler_level.upper()))
    ch.setFormatter(formatter)

    # Добавление обработчиков к логгеру
    logger.addHandler(file_handler)
    logger.addHandler(ch)

    logging.info("Логирование настроено. Логи будут записываться в: %s", log_file_path)
    return log_file_path
