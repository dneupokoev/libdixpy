# -*- coding: utf-8 -*-
"""
libdixpy - Библиотека с различными утилитами для собственных проектов.

Основные модули:
    uuid_bigint_incr - Генератор 18-значных UUID с временной меткой
"""

# Импорт основной функциональности
from .uuid_bigint_incr import uuid_gen, uuid_test_performance

# Версия пакета
__version__ = "0.0.2"  # Формат: MAJOR.MINOR.PATCH

# Определяем, что будет импортировано при from libdixpy import *
__all__ = [
    '__version__',

    'uuid_gen',
    'uuid_test_performance'
]
