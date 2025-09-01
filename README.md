# libdixpy

Библиотека с различными утилитами для собственных проектов.

## Установка

Установка непосредственно из GitHub:

```bash
pip install git+https://github.com/dneupokoev/libdixpy.git

для pipenv:
pipenv run pip install git+https://github.com/dneupokoev/libdixpy.git
```

Обновить пакет в проекте:

```bash
pip install --upgrade git+https://github.com/dneupokoev/libdixpy.git

для pipenv:
pipenv run pip install --upgrade git+https://github.com/dneupokoev/libdixpy.git
```

## Утилиты

- uuid_bigint_incr - Генератор 18-значных UUID с временнОй меткой
- db_async_clickhouse - Асинхронный коннектор для ClickHouse
