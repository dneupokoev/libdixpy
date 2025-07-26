# libdixpy/uuid_bigint_incr.py
# Формирование uuid.
#
# ТЗ:
# Напиши python-функцию формирования uid: uuid_bigint_incr
# Нужно чтобы можно было запускать синхронно и асинхронно. Сделай отдельным модулем без использования глобальных переменных.
# Результат = integer 18 цифр, которые формируются так: текущие unix дата-время до 1/100 секунды (12 цифр) + инкремент 6 цифр начинается с нуля, дополняется слева нулями до 6 цифр, хранится в оперативной памяти, при перезапуске скрипта или переполнении обнуляется. При сбросе инкремена сделай паузу 1/100 секунды.
#
# Использование модуля:
#
# 1. Синхронный вызов
# from libdixpy import uuid_gen
# print(uuid_gen.generate(_sync=True))
#
# 2. Асинхронный вызов
# from libdixpy import uuid_gen
# print(await uuid_gen.generate())

import time
import asyncio
import threading
from typing import Union


class UUIDGenerator:
    """
    Генератор 18-значных UUID с единым счетчиком:
    - 12 цифр: Unix timestamp в 1/100 секунды
    - 6 цифр: сквозной инкремент (000000-999999)
    """
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._init_state()
        return cls._instance

    def _init_state(self):
        self._increment = 0
        self._lock = threading.Lock()
        self._async_lock = asyncio.Lock()
        self._max_increment = 999999
        self._reset_delay = 0.01  # 1/100 секунды

    def generate(self, *, _sync: bool = False) -> Union[int, asyncio.Future]:
        """Генерация UUID
        
        Args:
            _sync (bool):
                Если True, возвращает синхронный результат.
                Если False (по умолчанию), автоматически определяет контекст.

        Returns:
            Union[int, asyncio.Future]: 18-значный UUID
        """
        if _sync or not self._is_async_context():
            with self._lock:
                return self._generate()
        return asyncio.ensure_future(self._async_generate())

    def _generate(self) -> int:
        """Общая логика генерации"""
        timestamp = int(time.time() * 100) % 10 ** 12
        increment = self._increment

        if increment >= self._max_increment:
            time.sleep(self._reset_delay)
            self._increment = 0
        else:
            self._increment += 1

        return timestamp * 10 ** 6 + increment

    async def _async_generate(self) -> int:
        """Асинхронная обертка"""
        async with self._async_lock:
            return self._generate()

    def _is_async_context(self) -> bool:
        try:
            asyncio.get_running_loop()
            return True
        except RuntimeError:
            return False

    @staticmethod
    def run_tests_sunc(count: int = 100000) -> str:
        """Тест производительности - Синхронный тест"""
        start = time.perf_counter()
        dv_uuid = uuid_gen.generate(_sync=True)
        dv_uuid_min = dv_uuid
        for _ in range(count):
            dv_uuid = uuid_gen.generate(_sync=True)
        sync_time = time.perf_counter() - start
        dv_txt = f"Синхронный тест ({count} итераций): {sync_time:.4f} сек ({count / sync_time:,.0f} UUID/сек) uuid min={dv_uuid_min} max={dv_uuid}"
        print(f"{dv_txt}")
        return dv_txt

    @staticmethod
    async def run_tests_async(count: int = 100000) -> str:
        """Тест производительности - Асинхронный тест"""
        start = time.perf_counter()
        dv_uuid = await uuid_gen.generate()
        dv_uuid_min = dv_uuid
        for _ in range(count):
            dv_uuid = await uuid_gen.generate()
        sync_time = time.perf_counter() - start
        dv_txt = f"Асинхронный тест ({count} итераций): {sync_time:.4f} сек ({count / sync_time:,.0f} UUID/сек) uuid min={dv_uuid_min} max={dv_uuid}"
        print(f"{dv_txt}")
        return dv_txt


# Синглтон для импорта
uuid_gen = UUIDGenerator()


def uuid_test_performance() -> dict:
    dv_return_dict = {}
    dv_return_dict['uuid_example'] = uuid_gen.generate(_sync=True)
    dv_return_dict['uuid_test_sync'] = UUIDGenerator.run_tests_sunc()
    dv_return_dict['uuid_test_async'] = asyncio.run(UUIDGenerator.run_tests_async())
    return dv_return_dict


if __name__ == "__main__":
    # Пример использования
    print("Пример UUID:", uuid_gen.generate(_sync=True))
    UUIDGenerator.run_tests_sunc()
    asyncio.run(UUIDGenerator.run_tests_async())
