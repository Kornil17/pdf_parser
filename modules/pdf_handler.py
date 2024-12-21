import logging
from typing import List

import fitz
from os import makedirs, path

from helpers.modules_helpers import run_pool_executor
from modules.ocr_processor import OCRProcessor

class PDFHandler:
    def __init__(self, pdf_file):
        self.pdf_file = pdf_file
        self.output_dir = self.create_output_dir()

    def create_output_dir(self) -> str:
        """
        Создание папки результатов для записи результатов обработки PDF.

        :return: Путь до папки результатов.
        """
        base_name = path.splitext(path.basename(self.pdf_file))[0]
        output_dir = path.join('results', base_name)
        makedirs(output_dir, exist_ok=True)
        return output_dir

    def extract_pages(self) -> List[str]:
        """
        Функция извлечения и обработки данных по страницам.

        :return: Список путей до файлов с результатами.
        """
        results_path = []
        try:
            with fitz.open(self.pdf_file) as doc:
                ocr_processor = OCRProcessor()
                results = run_pool_executor(func=ocr_processor.extract_text,
                                  params=map(lambda x: doc.load_page(x), range(len(doc))),
                                  )
            for page_number, (page, text) in enumerate(results):
                if text:
                    file_name = self.sanitize_filename(text) + '.pdf'
                else:
                    file_name = f'page_{page_number + 1}.pdf'

                output_path = path.join(self.output_dir, file_name)
                page.save(output_path)
                logging.info(f"Сохранили результат по пути: {output_path}")
                results_path.append(output_path)
            return results_path
        except FileNotFoundError:
            logging.error(f"Файл не найден по пути: {self.pdf_file}.\n"
                          f"Проверьте корректность пути до файла.")
        except Exception as ex:
            logging.error(f"Ошибка обработки файла {self.pdf_file}", exc_info=ex)

    @staticmethod
    def sanitize_filename(text: str) -> str:
        """
        Удаление запрещенных символов из имени файла.

        :param text: Исходный текст для очистки спец символов.
        :return: Текст без спец символов.
        """
        return ''.join(c for c in text if c.isalnum() or c in (' ', '_')).rstrip()
