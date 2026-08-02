# -*- coding: utf-8 -*-
"""
Bitrix24 Chat-Safe Sender Module
Отправка изображений напрямую в папку чата
Использует метод im.disk.folder.get
⚠️ Модуль работает только в синхронном режиме и останется таким.
"""
#
dv_file_version = '260212.01'
#
import requests
import json
from typing import Optional, Dict, Any
from pathlib import Path
from io import BytesIO
from loguru import logger


class Bitrix24ChatSafeSender:
    """
    Отправка изображений напрямую в папку чата
    Файлы автоматически доступны всем участникам чата
    """

    def __init__(self, webhook_url: str):
        """
        :param webhook_url: URL вебхука Bitrix24
        """
        self.webhook_url = webhook_url.rstrip('/')
        self.session = requests.Session()
        self.session.timeout = 15

        if not self.webhook_url.startswith(('http://', 'https://')):
            raise ValueError("Некорректный формат вебхука Bitrix24")

        logger.info(f"bitrix24_sender - ✅ Bitrix24ChatSafeSender инициализирован")

    def _call_api(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Универсальный метод вызова REST API Bitrix24"""
        url = f"{self.webhook_url}/{method}.json"

        try:
            response = self.session.post(url, json=params, timeout=15)
            response.raise_for_status()
            result = response.json()

            if not result.get('result'):
                error_msg = result.get('error_description', result.get('error', 'Unknown error'))
                logger.error(f"bitrix24_sender - ❌ Bitrix24 API error ({method}): {error_msg}")
                return {}

            logger.debug(f"bitrix24_sender - ✓ API {method} успешно")
            return result

        except requests.exceptions.RequestException as e:
            logger.error(f"bitrix24_sender - ❌ Сеть ({method}): {e}")
            return {}
        except json.JSONDecodeError as e:
            logger.error(f"bitrix24_sender - ❌ JSON ({method}): {e}")
            return {}

    def send_message(self, dialog_id: str, message: str) -> bool:
        """Отправка текстового сообщения в диалог"""
        params = {'DIALOG_ID': dialog_id, 'MESSAGE': message}
        result = self._call_api('im.message.add', params)
        success = bool(result.get('result'))

        if success:
            logger.info(f"bitrix24_sender - ✅ Текст отправлен в {dialog_id}, ID: {result['result']}")
        else:
            logger.warning(f"bitrix24_sender - ❌ Не удалось отправить текст в {dialog_id}")
        return success

    def get_chat_folder_id(self, dialog_id: str) -> Optional[int]:
        """Получение ID папки чата через im.disk.folder.get"""
        result = self._call_api('im.disk.folder.get', {'DIALOG_ID': dialog_id})

        if result and result.get('result'):
            folder_id = result['result'].get('ID')
            if folder_id:
                logger.info(f"bitrix24_sender - 📁 Папка чата: ID={folder_id}")
                return int(folder_id)

        logger.error(f"bitrix24_sender - ❌ Не удалось получить папку чата {dialog_id}")
        return None

    def upload_file_to_folder(self, folder_id: int, file_bytes: BytesIO, filename: str) -> Optional[int]:
        """Загрузка файла в указанную папку на Диске"""
        file_content = file_bytes.getvalue()
        content_size = len(file_content)

        logger.debug(f"bitrix24_sender - 📤 Загрузка '{filename}' ({content_size} байт) в папку {folder_id}")

        # --- Этап 1: Получение uploadUrl ---
        try:
            response = self.session.post(
                f"{self.webhook_url}/disk.folder.uploadfile.json",
                data={'id': folder_id, 'data': json.dumps({'NAME': filename, 'SIZE': content_size})},
                timeout=15
            )
            result = response.json()
            upload_url = result['result']['uploadUrl']
            logger.debug("bitrix24_sender - ✓ uploadUrl получен")
        except Exception as e:
            logger.error(f"bitrix24_sender - ❌ Ошибка получения uploadUrl: {e}")
            return None

        # --- Этап 2: Отправка файла ---
        try:
            ext = Path(filename).suffix.lower()
            mime_type = {
                '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
                '.png': 'image/png', '.gif': 'image/gif',
                '.bmp': 'image/bmp', '.webp': 'image/webp',
                '.pdf': 'application/pdf', '.txt': 'text/plain'
            }.get(ext, 'application/octet-stream')

            response = self.session.post(
                upload_url,
                files={'file': (filename, file_content, mime_type)},
                timeout=30
            )
            result = response.json()

            if response.status_code == 200 and isinstance(result.get('result'), dict):
                upload_id = result['result'].get('ID')
                if upload_id:
                    logger.info(f"bitrix24_sender - ✅ Файл загружен, UPLOAD_ID: {upload_id}")
                    return int(upload_id)

            logger.error(f"bitrix24_sender - ❌ Ошибка загрузки файла")
            return None
        except Exception as e:
            logger.error(f"bitrix24_sender - ❌ Ошибка загрузки: {e}")
            return None

    def send_file_to_chat(self, dialog_id: str, file_bytes: BytesIO, filename: str, caption: str = '') -> bool:
        """Отправка файла в чат с использованием папки чата"""
        logger.info(f"bitrix24_sender - 📎 Отправка файла в {dialog_id}")

        # Шаг 1: Получаем ID папки чата
        chat_folder_id = self.get_chat_folder_id(dialog_id)
        if not chat_folder_id:
            logger.error("bitrix24_sender - ❌ Папка чата не получена")
            self.send_message(dialog_id, f"{caption}\n⚠️ Ошибка папки чата")
            return False

        # Шаг 2: Загружаем файл в папку чата
        upload_id = self.upload_file_to_folder(chat_folder_id, file_bytes, filename)
        if not upload_id:
            logger.error("bitrix24_sender - ❌ Загрузка файла не удалась")
            self.send_message(dialog_id, f"{caption}\n⚠️ Ошибка загрузки")
            return False

        # Шаг 3: Отправляем файл в чат
        result = self._call_api('im.disk.file.commit', {
            'DIALOG_ID': dialog_id,
            'MESSAGE': caption,
            'UPLOAD_ID': upload_id
        })

        if result.get('result'):
            logger.info(f"bitrix24_sender - ✅✅✅ Файл отправлен в {dialog_id}, ID: {result['result']}")
            return True
        else:
            logger.error(f"bitrix24_sender - ❌ Ошибка прикрепления файла")
            self.send_message(dialog_id, f"{caption}\n⚠️ Ошибка прикрепления")
            return False

    def send_image_to_chat(self, dialog_id: str, image_bytes: BytesIO, filename: str, caption: str = '') -> bool:
        """Отправка изображения в чат"""
        return self.send_file_to_chat(dialog_id, image_bytes, filename, caption)
