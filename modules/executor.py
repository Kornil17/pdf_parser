import logging
import os
import glob

from helpers.modules_helpers import run_pool_executor
from modules.pdf_handler import PDFHandler

class Executor:
    def __init__(self, input_path):
        self.input_path = input_path

    def process_files(self) -> str:
        """
        Функция обработки PDF файла и создания файлов страниц.

        :return: Путь до папки с результатами обработки.
        """
        results = ''
        if os.path.isfile(self.input_path):
            logging.info(f"Файл {self.input_path} успешно получен.")
            results = self.extract_data(self.input_path)
        elif os.path.isdir(self.input_path):
            logging.info(f"Папка {self.input_path} с PDF файлами для обработки успешно получена.")
            pdf_files = glob.glob(os.path.join(self.input_path, '*.pdf'))
            results = list(run_pool_executor(func=self.extract_data,
                              params=iter(pdf_files)))
        else:
            logging.error(f"Некорректный путь: {self.input_path}\n"
                          f"Проверьте правильность указанного пути.")
        return results

    @staticmethod
    def extract_data(pdf_file: str) -> list:
        """
        Обработка PDF.

        :param pdf_file: Путь до PDF файла.
        :return: Список путей до файлов с результатами.
        """
        handler = PDFHandler(pdf_file)
        results = handler.extract_pages()
        return results
