# -*- coding: utf-8 -*-
"""
libdixpy - Библиотека с различными утилитами для собственных проектов.

Основные модули:
    - uuid_bigint_incr - Генератор 18-значных UUID с временнОй меткой
    - db_async_clickhouse - Асинхронный коннектор для ClickHouse
    - logging_utils - Утилиты для логирования с loguru
    - dfunc - Универсальные функции для всего на свете
"""

# Импорт функциональности:
from .uuid_bigint_incr import uuid_gen, uuid_test_performance
from .db_async_clickhouse import async_clickhouse
from .logging_utils import setup_logging, logger, log_message_secret
from .dfunc import *
from .bitrix24 import *

# Версия пакета
__version__ = "0.0.8"  # Формат: MAJOR.MINOR.PATCH

# Определяем, что будет импортировано при from libdixpy import *
__all__ = [
    '__version__',

    'uuid_gen',
    'uuid_test_performance',

    'async_clickhouse',

    'setup_logging',
    'logger',
    'log_message_secret',

    'bitrix24',

    # Все функции из dfunc
    'check_eval',
    'replace_none_to_default',
    'replace_dict_none_with_empty_str',
    'get_os_free_memory',
    'is_int',
    'is_list',
    'string2int',
    'string2list',
    'is_dict',
    'format_url',
    'get_domain',
    'string2dict',
    'get_data_from_request',
    'is_url',
    'add_utm_to_url',
    'generate_random_string',
    'unpickle_dict',
    'escape_sql_value'
]
