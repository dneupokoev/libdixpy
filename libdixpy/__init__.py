# -*- coding: utf-8 -*-
"""
libdixpy - Библиотека с различными утилитами для собственных проектов.

Основные модули:
    uuid_bigint_incr - Генератор 18-значных UUID с временнОй меткой
    db_async_clickhouse - Асинхронный коннектор для ClickHouse
    logging_utils - Утилиты для логирования с loguru
"""

# Импорт функциональности:
from .uuid_bigint_incr import uuid_gen, uuid_test_performance
from .db_async_clickhouse import async_clickhouse
from .logging_utils import setup_logging, logger, log_message_secret

# Версия пакета
__version__ = "0.0.6"  # Формат: MAJOR.MINOR.PATCH

# Определяем, что будет импортировано при from libdixpy import *
__all__ = [
    '__version__',

    'uuid_gen',
    'uuid_test_performance',

    'async_clickhouse',

    'setup_logging',
    'logger',
    'log_message_secret',
]
