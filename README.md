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

- **bitrix24** — Асинхронные утилиты для работы с Bitrix24 REST API (отправка сообщений, файлов, изображений в чаты).
- **db_async_clickhouse** — Асинхронный коннектор для ClickHouse с поддержкой вставки DataFrame и выполнения SQL-запросов.
- **uuid_bigint_incr** — Генератор 18-значных UUID на основе Unix timestamp с инкрементальным счетчиком (синхронный и асинхронный режимы).
- **logging_utils** — Утилиты для логирования: ротация логов, маскировка секретов, настройка логгера.
- **dfunc** — Набор синхронных вспомогательных функций: парсинг строк, работа с URL, утилиты для типов данных и т.д.

## Примеры использования

### bitrix24

Асинхронная и синхронная отправка сообщений и файлов в чаты Bitrix24.
Поддерживает полную обратную совместимость: старый код продолжит работать без изменений.

**Асинхронное использование (рекомендуется):**
```python
import asyncio
from io import BytesIO
from libdixpy.bitrix24 import Bitrix24ChatSafeSender

async def main():
    webhook_url = "https://your.bitrix24.ru/rest/1/token/"
    
    async with Bitrix24ChatSafeSender(webhook_url) as sender:
        await sender.send_message("chat123", "Привет!")
        
        with open("image.png", "rb") as f:
            image_bytes = BytesIO(f.read())
            await sender.send_image_to_chat(
                dialog_id="chat123",
                image_bytes=image_bytes,
                filename="image.png",
                caption="Подпись к изображению"
            )

asyncio.run(main())
```

**Синхронное использование (обратная совместимость):**
```python
from io import BytesIO
from libdixpy.bitrix24 import Bitrix24ChatSafeSender

webhook_url = "https://your.bitrix24.ru/rest/1/token/"

# Работает как обычный контекстный менеджер
with Bitrix24ChatSafeSender(webhook_url) as sender:
    # Методы с суффиксом _sync выполняют запросы синхронно
    sender.send_message_sync("chat123", "Привет!")
    
    with open("image.png", "rb") as f:
        image_bytes = BytesIO(f.read())
        sender.send_image_to_chat_sync(
            dialog_id="chat123",
            image_bytes=image_bytes,
            filename="image.png",
            caption="Подпись к изображению"
        )
```

### db_async_clickhouse

Асинхронная работа с ClickHouse: выполнение запросов и вставка данных.

```python
import asyncio
import pandas as pd
from libdixpy.db_async_clickhouse import async_clickhouse

async def main():
    config = {
        'url': 'http://clickhouse-server:8123',
        'user': 'default',
        'password': '',
        'force_post': True
    }

    async with async_clickhouse(config) as ch:
        # Выполнение запроса с возвратом DataFrame
        result_meta, df = await ch.execute_query("SELECT * FROM my_table LIMIT 10")
        
        # Вставка данных из DataFrame
        new_df = pd.DataFrame({'id': [1, 2], 'value': ['a', 'b']})
        await ch.insert_df('my_table', new_df)

asyncio.run(main())
```

### uuid_bigint_incr

Генерация уникальных 18-значных идентификаторов.

```python
from libdixpy.uuid_bigint_incr import UUIDGenerator

# Синхронное использование (Singleton)
uuid_gen = UUIDGenerator()
uid1 = uuid_gen.generate(_sync=True)
uid2 = uuid_gen.generate(_sync=True)

print(uid1, uid2)  # 18-значные целые числа
```

### logging_utils

Настройка логирования с ротацией и маскировкой чувствительных данных.

```python
from libdixpy.logging_utils import setup_logging

# Инициализация логгера
logger = setup_logging(
    log_level='INFO',
    path_to_log='./logs',
    app_name='my_app',
    script_name='main'
)

logger.info("Приложение запущено")
```

### dfunc

Вспомогательные функции для работы со строками, URL и типами данных.

```python
from libdixpy.dfunc import string2int, format_url, generate_random_string, is_dict

# Преобразование строк в числа
val = string2int("123abc", default=0)  # 123

# Форматирование URL
url = format_url("example.com/path")  # "http://example.com/path"

# Генерация случайной строки
rand_str = generate_random_string(length=16)

# Проверка на JSON-строку
is_dict('{"key": "value"}')  # True
```
