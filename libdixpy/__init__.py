# -*- coding: utf-8 -*-
"""
libdixpy - Библиотека с различными утилитами для собственных проектов.

Основные модули:
    uuid_bigint_incr - Генератор 18-значных UUID с временнОй меткой
    db_async_clickhouse - Асинхронный коннектор для ClickHouse
"""

# Импорт основной функциональности
# Импорт из uuid_bigint_incr
from .uuid_bigint_incr import uuid_gen, uuid_test_performance

# Импортируем класс коннектора async_clickhouse
from .db_async_clickhouse import async_clickhouse

# Версия пакета
__version__ = "0.0.3"  # Формат: MAJOR.MINOR.PATCH

# Определяем, что будет импортировано при from libdixpy import *
__all__ = [
    '__version__',

    'uuid_gen',
    'uuid_test_performance',

    'async_clickhouse',
]
