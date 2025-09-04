# -*- coding: utf-8 -*-
# libdixpy/logging_utils.py
"""
Модуль для настройки логирования с использованием loguru.

Логика формирования имени файла:
    - Если script_name указан: app_name_script_name.log
    - Если script_name не указан: app_name.log

from libdixpy import setup_logging, logger

# Создаст файл my_application_main_script.log
setup_logging(
    log_level='DEBUG',
    path_to_log='/var/log/myapp',
    app_name='my_application',
    script_name='main_script'
)

# Использование логгера
logger.info("Запуск приложения")
logger.debug("Отладочная информация")
logger.error("Ошибка в приложении")
"""
#
dv_file_version = '250904.02'
#
import re
import sys
import datetime
from loguru import logger

# Предкомпилируем регулярное выражение для максимальной производительности
# Измененное регулярное выражение: захватываем только значения после ключей
_SECRET_PATTERN = re.compile(
    r"(['\"]?(?:atok[\w]*|token[\w]*|passw[\w]*|pswd[\w]*)['\"]?\s*[:=\s]\s*['\"])([^'\"]*)(['\"])",
    re.IGNORECASE
)


class LogRotator:
    """
    Ротация лог-файла в зависимости от двух параметров: от размера и от времени.
    """

    def __init__(self, *, size, at):
        now = datetime.datetime.now()
        self._size_limit = size
        self._time_limit = now.replace(hour=at.hour, minute=at.minute, second=at.second)

        if now >= self._time_limit:
            self._time_limit += datetime.timedelta(days=1)

    def should_rotate(self, message, file):
        file.seek(0, 2)
        if file.tell() + len(message) > self._size_limit:
            return True
        excess = message.record["time"].timestamp() - self._time_limit.timestamp()
        if excess >= 0:
            elapsed_days = datetime.timedelta(seconds=excess).days
            self._time_limit += datetime.timedelta(days=elapsed_days + 1)
            return True
        return False


def log_message_secret(message: str):
    """
    Функция скрывает конфиденциальную информацию в строке, например такую конструкцию {'my_token': '1111111'} на такую {'my_token': 'secret'}
    """
    return _SECRET_PATTERN.sub(r"\1secret\3", message)


def log_format_secret(record):
    """
    Задаем формат лога с заменой секретных данных.
    """
    record["extra"]["message_secret"] = log_message_secret(record["message"])
    return "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>#<cyan>{line}</cyan> | <level>{extra[message_secret]}</level>\n{exception}"


def setup_logging(log_level='ERROR', path_to_log='.', app_name='app', script_name=None):
    """
    Настройка логирования.

    Args:
        log_level (str): Уровень логирования (DEBUG, INFO, WARNING, ERROR)
        path_to_log (str): Путь для сохранения лог-файлов
        app_name (str): Имя приложения для именования лог-файла
        script_name (str, optional): Имя скрипта для лог-файла. Если не указано, используется app_name
    """
    # отключаем стандартное логирование в консоль
    logger.remove()

    # Включаем ротацию, если файл превышает 10 МБ или в полночь каждый день
    log_rotator = LogRotator(size=1e+7, at=datetime.time(0, 0, 0))

    # Устанавливаем уровень логирования
    if log_level not in ['DEBUG', 'INFO', 'WARNING', 'ERROR']:
        log_level = 'ERROR'

    # Логирование в консоль
    logger.add(sys.stderr, level=log_level, format=log_format_secret, colorize=True, enqueue=True)

    # Формируем имя лог-файла
    if script_name:
        # Если указано script_name, используем формат: app_name_script_name.log
        log_file = f"{path_to_log}/{app_name}_{script_name}.log"
    else:
        # Если script_name не указано, оставляем формат: app_name.log
        log_file = f"{path_to_log}/{app_name}.log"

    # Логирование в файл:
    # Параметр enqueue=True заставляет loguru использовать внутреннюю очередь и отдельный поток для записи, что практически устраняет блокировку event loop.
    logger.add(
        log_file, level=log_level, format=log_format_secret,
        rotation=log_rotator.should_rotate, retention='30 days',
        compression="gz", encoding="utf-8", enqueue=True,
        backtrace=True, diagnose=True, catch=True
    )

    return logger


# Экспорт логгера для удобного использования
logger = setup_logging()