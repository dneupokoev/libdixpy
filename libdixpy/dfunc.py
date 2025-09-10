# -*- coding: utf-8 -*-
# libdixpy/dfunc.py
"""
Универсальные функции для всего на свете.

Использование модуля:
from libdixpy import dfunc

print(dfunc.is_int("123"))          # True
print(dfunc.string2int("abc", -1))  # -1
print(dfunc.get_domain("https://www.example.com/path"))  # example.com
"""
dv_file_version = '250910.01'

import re
import pickle
import ast
import random
import string
from urllib.parse import urlencode, urlparse, urlunparse, parse_qs
from typing import Any, Dict, List, Union, Optional


def check_eval(str4eval: Optional[str] = None) -> bool:
    """
    Функция проверяет можно ли такой eval выполнять. Чтобы не было инъекций.
    True - можно выполнять.
    """
    # Здесь надо написать проверку. Пока без всяких проверок работаем!
    return True


def replace_none_to_default(var: Any = None, default: Any = None) -> Any:
    """
    Функция заменяет значение переменной None на указанное значение.
    """
    return default if var is None else var


def replace_dict_none_with_empty_str(input_dict: Dict[str, Any]) -> Dict[str, Any]:
    """
    Функция заменяет в словаре все None на пустоту.
    """
    return {k: ('' if v is None else v) for k, v in input_dict.items()}


def get_os_free_memory() -> int:
    """
    Функция возвращает сколько в системе свободной памяти ОЗУ в МБ.
    Использует /proc/meminfo для кроссплатформенной совместимости.
    Возвращает -999 в случае ошибки.
    """
    try:
        with open('/proc/meminfo', 'r') as f:
            meminfo = f.read()

        # Приоритет MemAvailable, fallback на MemFree
        patterns = [r'MemAvailable:\s+(\d+)', r'MemFree:\s+(\d+)']
        for pattern in patterns:
            match = re.search(pattern, meminfo)
            if match:
                mem_kb = int(match.group(1))
                return mem_kb // 1024

    except (FileNotFoundError, PermissionError, ValueError) as e:
        print(f"Ошибка при чтении /proc/meminfo: {e}")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")

    return -999


def is_int(string: str) -> bool:
    """
    Функция проверяет тип: является ли переданный string целым числом (int).
    """
    try:
        int(string)
        return True
    except (ValueError, TypeError):
        return False


def is_list(string: str) -> bool:
    """
    Функция проверяет тип: является ли переданный string списком (list).
    """
    if not isinstance(string, str):
        return False

    try:
        result = ast.literal_eval(string)
        return isinstance(result, list)
    except (ValueError, SyntaxError):
        return False


def string2int(string: str = '', default: int = 0) -> int:
    """
    Функция конвертирует string в int и возвращает его (если это не int, то вернёт default).
    """
    try:
        return int(string)
    except (ValueError, TypeError):
        return default


def string2list(string: str) -> List[Any]:
    """
    Функция конвертирует string в list и возвращает его (если это не list, то вернёт пустой list).
    """
    if not isinstance(string, str):
        return []

    try:
        result = ast.literal_eval(string)
        return result if isinstance(result, list) else []
    except (ValueError, SyntaxError):
        return []


def is_dict(string: str) -> bool:
    """
    Функция проверяет тип: является ли переданный string словарем (dict).
    """
    if not isinstance(string, str):
        return False

    try:
        result = ast.literal_eval(string)
        return isinstance(result, dict)
    except (ValueError, SyntaxError):
        return False


def format_url(url: str = '') -> str:
    """
    Функция дополняет url в начало http://, если url начинается сразу с домена.
    Это нужно для того, чтобы корректно распарсить домен.
    """
    if not url:
        return url

    if not re.match(r'(?:http|https)://', url):
        return f'http://{url}'
    return url


def get_domain(url: str = '') -> str:
    """
    Функция из полного url возвращает только ДОМЕН без www и прочего.
    """
    if not url:
        return url

    try:
        formatted_url = format_url(url)
        parsed = urlparse(formatted_url)
        domain = parsed.netloc

        # Убираем www. если есть
        if domain.startswith('www.'):
            domain = domain[4:]

        return domain
    except Exception:
        return url


def string2dict(string: str) -> Dict[str, Any]:
    """
    Функция конвертирует string в dict (если это не dict, то вернёт пустой dict).
    """
    if not isinstance(string, str):
        return {}

    try:
        result = ast.literal_eval(string)
        return result if isinstance(result, dict) else {}
    except (ValueError, SyntaxError):
        return {}


def get_data_from_request(request=None) -> Dict[str, str]:
    """
    Функция извлекает из запроса нужные данные и возвращает в виде словаря dict.
    """
    if request is None:
        return {}

    try:
        referer = request.headers.get('referer', '')
        origin = request.headers.get('origin', '')

        result = {
            'request_referer': get_domain(referer),
            'request_origin': get_domain(origin),
            'user_agent': request.headers.get('user-agent', ''),
            'accept_language': request.headers.get('accept-language', ''),
        }

        # Если origin пустой, используем referer
        if not result['request_origin']:
            result['request_origin'] = result['request_referer']

        # Получаем IP адрес
        x_forwarded_for = request.headers.get('x-forwarded-for', '')
        x_real_ip = request.headers.get('x-real-ip', '')

        if x_forwarded_for:
            result['user_ip'] = x_forwarded_for.split(',')[0].strip()
        elif x_real_ip:
            result['user_ip'] = x_real_ip
        else:
            result['user_ip'] = ''

        return result
    except Exception:
        return {}


def is_url(url: str = '') -> bool:
    """
    Проверяет, является ли текст валидным URL.
    """
    if not url or not isinstance(url, str):
        return False

    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])  # Обязательно наличие схемы и домена
    except Exception:
        return False


def add_utm_to_url(url: str = '', utm_name: str = '', utm_val: str = '') -> str:
    """
    Добавляет (или обновляет) UTM-метки в URL.
    """
    if not url or not is_url(url):
        return url

    try:
        parsed = urlparse(url)
        query_params = parse_qs(parsed.query)
        # Обновляем UTM-параметры
        query_params[utm_name] = [utm_val]
        # Собираем URL обратно
        new_query = urlencode(query_params, doseq=True)
        return urlunparse(parsed._replace(query=new_query))
    except Exception:
        return url  # Возвращаем оригинальный URL в случае ошибки


def generate_random_string(length: int = 8) -> str:
    """
    Generate a random string of specified length.
    """
    if length <= 0:
        return ''

    # Убедимся, что length не превышает доступные символы
    available_chars = string.ascii_letters
    actual_length = min(length, len(available_chars))

    return ''.join(random.sample(available_chars, actual_length))


def unpickle_dict(pickled_dict: Dict[Any, Any]) -> Dict[Any, Any]:
    """
    Преобразует словарь с pickled ключами и значениями в обычный словарь.
    """
    if not isinstance(pickled_dict, dict):
        return {}

    result = {}
    for key, value in pickled_dict.items():
        try:
            # Обрабатываем ключ
            unpickled_key = key
            if isinstance(key, bytes):
                try:
                    unpickled_key = pickle.loads(key)
                except (pickle.UnpicklingError, Exception):
                    try:
                        unpickled_key = key.decode('utf-8')
                    except UnicodeDecodeError:
                        unpickled_key = key

            # Обрабатываем значение
            unpickled_value = value
            if isinstance(value, bytes):
                try:
                    unpickled_value = pickle.loads(value)
                except (pickle.UnpicklingError, Exception):
                    try:
                        unpickled_value = value.decode('utf-8')
                    except UnicodeDecodeError:
                        unpickled_value = value

            result[unpickled_key] = unpickled_value

        except Exception:
            # Если не получается распаковать, оставляем как есть
            result[key] = value

    return result


def escape_sql_value(value: Any) -> str:
    """
    Экранируем кавычки перед записью в БД.
    """
    if value is None:
        return "NULL"

    if isinstance(value, str):
        # Экранируем одинарные и двойные кавычки
        escaped = value.replace("'", "''").replace('"', '""')
        return f"'{escaped}'"

    return str(value)