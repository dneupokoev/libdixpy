# libdixpy

Библиотека с различными утилитами для собственных проектов.

## Установка

Установка непосредственно из GitHub:

```bash
pip install git+https://github.com/dneupokoev/libdixpy.git

для pipenv:
pipenv install git+https://github.com/dneupokoev/libdixpy.git

если не надо, чтобы появился в Pipfile: 
pipenv run pip install git+https://github.com/dneupokoev/libdixpy.git
```

Обновить пакет в проекте:

```bash
pip install --upgrade git+https://github.com/dneupokoev/libdixpy.git

для pipenv:
pipenv run pip install --upgrade git+https://github.com/dneupokoev/libdixpy.git
```

## Модули

- `uuid_bigint_incr` — Генератор 18-значных UUID с временной меткой и инкрементом
- `db_async_clickhouse` — Асинхронный коннектор для ClickHouse (вставка, запросы, DataFrame)
- `logging_utils` — Утилиты для логирования с ротацией и маскировкой секретов
- `dfunc` — Набор вспомогательных функций (парсинг, валидация, работа с URL, утилиты)
- `bitrix24` — Отправка сообщений и файлов в Bitrix24 чаты

## Примеры работы с модулями:

### bitrix24

Модуль для работы с Bitrix24 REST API. Позволяет отправлять файлы и изображения
напрямую в папку чата с автоматическим управлением правами доступа.

```python
from io import BytesIO
from libdixpy.bitrix24 import Bitrix24ChatSafeSender

# Инициализация
sender = Bitrix24ChatSafeSender("https://your.bitrix24.ru/rest/1/token/")

# Отправка текстового сообщения:
sender.send_message("chat123", "Привет!")

# Отправка отформатированного текстового сообщения:
sender.send_message(
    dialog_id="chat123",
    message="""
    [B]ВАЖНОЕ УВЕДОМЛЕНИЕ[/B]

    [U]Детали:[/U]
    • Проект завершён
    • [COLOR=#00aa00]Статус: выполнено[/COLOR]

    [I]С уважением, команда[/I]
    """
)

# Отправка изображения:
with open("image.png", "rb") as f:
    image_bytes = BytesIO(f.read())
    sender.send_image_to_chat(
        dialog_id="chat123",
        image_bytes=image_bytes,
        filename="image.png",
        caption="Подпись к изображению"
    )
```

### uuid_bigint_incr

Генератор уникальных 18-значных идентификаторов на основе Unix timestamp и инкремента.
Поддерживает как синхронный, так и асинхронный режимы работы.

```python
from libdixpy.uuid_bigint_incr import UUIDGenerator

gen = UUIDGenerator()

# Синхронная генерация
uid_sync = gen.generate(_sync=True)

# Асинхронная генерация (внутри async-функции)
# uid_async = await gen.generate()
```

### db_async_clickhouse

Асинхронный клиент для взаимодействия с ClickHouse. Поддерживает вставку данных,
выполнение запросов и работу с `pandas.DataFrame`.

```python
import pandas as pd
from libdixpy.db_async_clickhouse import async_clickhouse

config = {
    'url': 'http://localhost:8123',
    'user': 'default',
    'password': '',
    'force_post': True
}

async with async_clickhouse(config) as ch:
    # Выполнение SELECT запроса
    result, df = await ch.execute_query("SELECT * FROM my_table LIMIT 10")
    
    # Вставка CSV данных
    csv_data = "col1,col2\nval1,val2"
    await ch.insert_data('my_table', csv_data, format='CSV')
    
    # Вставка pandas DataFrame
    df = pd.DataFrame({'a': [1, 2], 'b': ['x', 'y']})
    await ch.insert_df('my_table', df)
    
    # Выполнение команд (CREATE, DROP и т.д.)
    await ch.execute_command("TRUNCATE TABLE my_table")
```

### logging_utils

Утилиты для настройки логирования, ротации файлов по размеру/времени и маскировки секретов.

```python
from libdixpy.logging_utils import setup_logging, LogRotator

# Базовая настройка логирования
logger = setup_logging(log_level='INFO', app_name='my_app', path_to_log='./logs')

# Ротация логов (по размеру 10MB или по времени)
rotator = LogRotator(size=10 * 1024 * 1024, at='00:00')
```

### dfunc

Набор универсальных вспомогательных функций для парсинга, валидации, работы с URL и другими задачами.

```python
from libdixpy.dfunc import (
    string2int, string2list, string2dict,
    is_url, format_url, add_utm_to_url,
    generate_random_string, escape_sql_value,
    replace_none_to_default
)

# Парсинг строк в типы
val = string2int("123", default=0)
lst = string2list("[1, 2, 3]")
dct = string2dict('{"key": "value"}')

# Работа с URL
url = format_url("https://example.com")
url_with_utm = add_utm_to_url(url, utm_name="source", utm_val="github")
is_valid = is_url("https://google.com")

# Утилиты
rand_str = generate_random_string(length=16)
safe_val = escape_sql_value("user's input")
cleaned = replace_none_to_default(None, default="empty")
```
