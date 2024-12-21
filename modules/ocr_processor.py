import logging
from typing import Tuple

import pytesseract
from PIL import Image
from pymupdf import Page
from pdf2image import convert_from_path

from modules.settings import settings


class OCRProcessor:
    """Класс обработки текста с помощью Tesseract."""

    # @staticmethod
    # def extract_text(page: Page) -> Tuple[Page, str]:
    #     """
    #     Метод извлечения данных из текста PDF файла.
    #
    #     :param page: PDF страница.
    #     :return: Кортеж PDF страница + текст страницы
    #     """
    #     pytesseract.pytesseract.tesseract_cmd = settings.tesseract_path
    #     tessdata_dir_config = settings.tesseract_language_path
    #
    #     # Конвертация страницы в изображение для OCR.
    #     pix = page.get_pixmap()
    #     img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    #     # Использование Tesseract для распознавания текста.
    #     text = pytesseract.image_to_string(img, lang='rus+eng', config=tessdata_dir_config)
    #     # text = pytesseract.image_to_string(img, lang='rus+eng')
    #     return page, text.strip()
    @staticmethod
    def extract_text(page: Page) -> Tuple[Page, str]:
        """
        Метод извлечения данных из текста PDF файла.

        :param page: PDF страница.
        :return: Кортеж PDF страница + текст страницы
        """
        pytesseract.pytesseract.tesseract_cmd = settings.tesseract_path
        tessdata_dir_config = settings.tesseract_language_path

        # Конвертация страницы PDF в изображение
        images = convert_from_path(page.parent._name, first_page=page.number + 1, last_page=page.number + 1)
        logging.debug('Конвертация страницы в изображение')
        if not images:
            return page, ""

        img = images[0]  # Получаем первое (и единственное) изображение

        # Использование Tesseract для распознавания текста.
        text = pytesseract.image_to_string(img, lang='rus+eng', config=tessdata_dir_config)

        return page, text.strip()
