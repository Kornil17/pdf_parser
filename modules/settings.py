import logging
from os import path


class Settings:
    """Класс подгтовки настроек для запуска приложения."""

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, env_file: str = '.env') -> None:
        self.current_dir = path.dirname(path.realpath(__file__))
        self.load_from_env(env_file)

    def load_from_env(self, env_file: str) -> None:
        """
        Функция выгрузки параметров настроек из .env файла.

        :param env_file: Путь до .env файла
        :return: None
        """
        try:
            env_path = path.join(self.current_dir, f'../{env_file}')
            with open(file=env_path, mode='r', encoding='utf8') as f:
                for line in f:
                    key, value = line.strip().split('=')
                    setattr(self, key.lower(), value)
        except FileNotFoundError:
            logging.error('Файл {env_file} не был найден в рабочей директории проекта.'.format(env_file=env_file))


settings = Settings()
