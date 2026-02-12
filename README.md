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

- uuid_bigint_incr - Генератор 18-значных UUID с временнОй меткой
- db_async_clickhouse - Асинхронный коннектор для ClickHouse
- logging_utils - Утилиты для логирования с loguru
- dfunc - Универсальные функции для всего на свете
- bitrix24 - Утилиты для работы с bitrix24

## Примеры работы с модулями:

### bitrix24

Модуль для работы с Bitrix24 REST API. Позволяет отправлять файлы и изображения
напрямую в папку чата с автоматическим управлением правами доступа.

```python
from libdixpy.bitrix24 import Bitrix24ChatSafeSender

# Инициализация
sender = Bitrix24ChatSafeSender("https://your.bitrix24.ru/rest/1/token/")

# Отправка изображения
with open("image.png", "rb") as f:
    image_bytes = BytesIO(f.read())
    sender.send_image_to_chat(
        dialog_id="chat123",
        image_bytes=image_bytes,
        filename="image.png",
        caption="Подпись к изображению"
    )

# Отправка текстового сообщения
sender.send_message("chat123", "Привет!")
```
