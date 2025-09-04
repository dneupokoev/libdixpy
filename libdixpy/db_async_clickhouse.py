# -*- coding: utf-8 -*-
# libdixpy/db_async_clickhouse.py
"""
Асинхронный коннектор для ClickHouse

Использование модуля:
from libdixpy import async_clickhouse
или
import libdixpy
connector = libdixpy.async_clickhouse(config)
"""
#
dv_file_version = '250904.01'
#
import aiohttp
import numpy as np
import pandas as pd
from io import StringIO
from typing import Dict, Optional, Tuple
import json
import csv
import chardet  # для автоопределения кодировки


class async_clickhouse:
    def __init__(self, config: Dict[str, str]):
        """
        Инициализация коннектора к ClickHouse

        :param config: {
            'url': 'http://clickhouse-server:8123',
            'user': 'default',
            'password': '',
            'force_post': True  # всегда использовать POST
        }
        """
        self.url = config['url'].rstrip('/') + '/'
        self.user = config.get('user', 'default')
        self.password = config.get('password', '')
        self.force_post = config.get('force_post', True)  # Всегда POST для записи
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.session:
            await self.session.close()
            self.session = None

    async def _make_request(self, sql: str, data: Optional[str] = None,
                            format: Optional[str] = None) -> Dict:
        """
        Универсальный метод выполнения запроса
        """
        result = {'status': 'FAIL', 'message': ''}

        if not self.session:
            result['message'] = 'Сессия не инициализирована'
            return result

        try:
            # ВСЕГДА используем POST для любых запросов
            method = self.session.post
            method_name = "POST"

            params = {}  # Убираем user/password из параметров

            # Передаем учетные данные через заголовки
            headers = {
                'X-ClickHouse-User': self.user,
                'X-ClickHouse-Key': self.password
            }

            request_data = ''

            # Если есть данные - это точно INSERT
            if data:
                params['query'] = sql
                request_data = data
                headers['Content-Type'] = 'text/plain; charset=utf-8'  # Явно указываем UTF-8 для отправляемых данных
            else:
                # Для SELECT с форматом
                if format and sql.strip().upper().startswith('SELECT'):
                    # Явно указываем, что ожидаем JSON в UTF-8
                    params['query'] = f"{sql} FORMAT {format}"
                    headers['Accept'] = 'application/json; charset=utf-8'
                    headers['Accept-Charset'] = 'utf-8'
                else:
                    params['query'] = sql
            async with method(
                    url=self.url,
                    params=params,
                    headers=headers,
                    data=request_data
            ) as response:
                # Вместо response.text(), получаем байты
                response_bytes = await response.read()
                if response.status != 200:
                    # Пытаемся декодировать текст ошибки, игнорируя ошибки или используя замену
                    try:
                        # Попробуем сначала UTF-8
                        response_text_for_error = response_bytes.decode('utf-8')
                    except UnicodeDecodeError:
                        # Если UTF-8 не работает, попробуем автоопределение
                        try:
                            detected_encoding = chardet.detect(response_bytes)['encoding']
                            response_text_for_error = response_bytes.decode(detected_encoding or 'utf-8', errors='replace')
                        except Exception:
                            # Если и автоопределение не помогло, используем 'replace'
                            response_text_for_error = response_bytes.decode('utf-8', errors='replace')

                    result['message'] = f"HTTP {response.status}: {response_text_for_error}"
                    return result
                result['status'] = 'SUCCESS'
                #
                # Обработка успешного ответа
                if format == 'JSON' and response_bytes and not data and sql.strip().upper().startswith('SELECT'):
                    # Пытаемся декодировать JSON-ответ
                    try:
                        # Предполагаем UTF-8
                        response_text = response_bytes.decode('utf-8')
                    except UnicodeDecodeError:
                        # Если UTF-8 не работает, пробуем автоопределение
                        try:
                            detected_encoding = chardet.detect(response_bytes)['encoding']
                            response_text = response_bytes.decode(detected_encoding or 'utf-8', errors='replace')
                            # После замены 'replace' данные могут быть повреждены, но мы попробуем
                        except Exception as e:
                            result['status'] = 'ERROR'
                            result['message'] = f"_make_request - Ошибка декодирования JSON-ответа: {e}"
                            return result
                    #
                    try:
                        result['data'] = json.loads(response_text).get('data', [])
                    except json.JSONDecodeError as e:
                        result['status'] = 'ERROR'
                        result['message'] = f"_make_request - Ошибка JSON: {str(e)}, response_text[:200]: {response_text[:200]}"
                #
                return result  # Возвращаем результат
        #
        except Exception as e:
            result['message'] = f"Ошибка запроса: {str(e)}"
            return result

    def _is_modifying_query(self, sql: str) -> bool:
        """Определяет, изменяет ли запрос данные"""
        sql_upper = sql.strip().upper()
        modifying = [
            'INSERT', 'UPDATE', 'DELETE',
            'ALTER', 'CREATE', 'DROP',
            'TRUNCATE', 'RENAME', 'REPLACE',
            'OPTIMIZE', 'ATTACH', 'DETACH'
        ]
        return any(sql_upper.startswith(cmd) for cmd in modifying)

    async def insert_data(self, table_name: str, data: str, format: str = 'CSV') -> Dict:
        """
        Гарантированная вставка данных в таблицу

        :param table_name: db.table
        :param data: данные для вставки
        :param format: CSV или JSONEachRow
        :return: {'status': 'SUCCESS/ERROR', 'message': '', 'rows': N}
        """
        sql = f"INSERT INTO {table_name} FORMAT {format}"
        result = await self._make_request(sql, data=data)
        if result['status'] == 'SUCCESS':
            result['rows'] = len(data.strip().split('\n')) if data else 0
        return result

    async def truncate_table(self, table_name: str) -> Dict:
        """
        Очистка таблицы (TRUNCATE TABLE)

        :param table_name: db.table
        :return: {'status': 'SUCCESS/ERROR', 'message': ''}
        """
        sql = f"TRUNCATE TABLE {table_name}"
        return await self._make_request(sql)

    async def insert_df(self, table_name: str, df: pd.DataFrame,
                        truncate_first: bool = False, format: str = 'JSONEachRow') -> Dict:
        """
        Вставка DataFrame

        :param table_name: db.table
        :param df: DataFrame
        :param truncate_first: Если True, перед вставкой выполнит TRUNCATE TABLE
        :param format: CSV или JSONEachRow (по умолчанию JSONEachRow - более безопасный)
        :return: {'status': 'SUCCESS/ERROR', 'message': '', 'rows': N}
        """
        if df.empty:
            return {'status': 'ERROR', 'message': 'Пустой DataFrame', 'rows': 0}

        try:
            if truncate_first:
                truncate_result = await self.truncate_table(table_name)
                if truncate_result['status'] != 'SUCCESS':
                    return {
                        'status': 'ERROR',
                        'message': f"Ошибка TRUNCATE перед вставкой: {truncate_result['message']}",
                        'rows': 0
                    }

            # Подготовка данных - заменяем все NaN/NaT на None
            df_clean = df.replace({np.nan: None, pd.NaT: None})
            format_upper = format.upper()

            if format_upper == 'CSV':
                # Для CSV используем безопасное экранирование
                with StringIO() as buffer:
                    df_clean.to_csv(
                        buffer,
                        index=False,
                        header=False,
                        date_format='%Y-%m-%d %H:%M:%S',
                        quoting=csv.QUOTE_ALL,  # Экранируем все значения в кавычки
                        escapechar='\\',  # Экранирующий символ
                        doublequote=False  # Не удваивать кавычки
                    )
                    data = buffer.getvalue()

            elif format_upper == 'JSONEACHROW':
                # Безопасное формирование JSONEachRow
                records = []
                for record in df_clean.to_dict('records'):
                    # Очищаем значения от None и преобразуем специальные типы
                    cleaned_record = {}
                    for key, value in record.items():
                        if value is None:
                            cleaned_record[key] = None
                        elif isinstance(value, (pd.Timestamp, np.datetime64)):
                            cleaned_record[key] = value.isoformat()
                        elif isinstance(value, (pd.DataFrame, pd.Series)):
                            # Сложные объекты преобразуем в строку
                            cleaned_record[key] = str(value)
                        else:
                            cleaned_record[key] = value

                    records.append(json.dumps(cleaned_record, ensure_ascii=False))

                data = '\n'.join(records)

            else:
                return {
                    'status': 'ERROR',
                    'message': f'Неподдерживаемый формат: {format}. Используйте CSV или JSONEachRow',
                    'rows': 0
                }

            return await self.insert_data(table_name, data, format)

        except Exception as e:
            error_msg = f"insert_df - Ошибка подготовки данных: {str(e)}"
            print(f"ERROR: {error_msg}")
            return {
                'status': 'ERROR',
                'message': error_msg,
                'rows': 0
            }

    async def execute_query(self, sql: str) -> Tuple[Dict, Optional[pd.DataFrame]]:
        """
        Выполнение SELECT запроса

        :param sql: SQL запрос
        :return: (результат, DataFrame)
        """
        result = await self._make_request(sql, format='JSON')
        df = pd.DataFrame(result['data']) if result.get('data') else None
        return result, df

    async def execute_command(self, sql: str) -> Dict:
        """
        Выполнение DDL команды

        :param sql: SQL команда
        :return: {'status': 'SUCCESS/ERROR', 'message': ''}
        """
        return await self._make_request(sql)
