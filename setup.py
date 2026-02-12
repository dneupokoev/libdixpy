# -*- coding: utf-8 -*-
import re
from pathlib import Path
from setuptools import setup, find_packages


def get_version():
    """Извлечение версии из libdixpy/__init__.py"""
    init_file = Path(__file__).parent / "libdixpy" / "__init__.py"
    version_match = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
        init_file.read_text(encoding="utf-8"),
        re.MULTILINE
    )
    if version_match:
        return version_match.group(1)
    else:
        raise RuntimeError("Unable to find version string in libdixpy/__init__.py")


# Чтение README.md
this_directory = Path(__file__).parent
readme_path = this_directory / "README.md"
if readme_path.exists():
    long_description = readme_path.read_text(encoding="utf-8")
else:
    long_description = "Библиотека с различными утилитами для собственных проектов"

# Чтение CHANGELOG.md
changelog_path = this_directory / "CHANGELOG.md"
if changelog_path.exists():
    changelog = changelog_path.read_text(encoding="utf-8")
    long_description += "\n\n## Changelog\n\n" + changelog

setup(
    name="libdixpy",
    version=get_version(),
    author="DNeupokoev",
    author_email="dials@mail.ru",
    description="Библиотека с различными утилитами для собственных проектов",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dneupokoev/libdixpy",
    project_urls={
        "Документация": "https://github.com/dneupokoev/libdixpy#readme",
        "Исходный код": "https://github.com/dneupokoev/libdixpy",
        "Changelog": "https://github.com/dneupokoev/libdixpy/blob/main/CHANGELOG.md",
        "Bug Tracker": "https://github.com/dneupokoev/libdixpy/issues",
    },
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Database :: Database Engines/Servers",
        "Topic :: Communications :: Chat",
        "Topic :: Internet :: WWW/HTTP",
    ],
    python_requires=">=3.8",
    install_requires=[
        # ОСНОВНЫЕ ЗАВИСИМОСТИ (для всех модулей)
        "loguru>=0.7.0",  # для логирования
        "requests>=2.31.0",  # для Bitrix24 и HTTP-запросов
        "typing_extensions>=4.0.0; python_version < '3.10'",

        # Для модуля ClickHouse
        "aiohttp>=3.8.0",
        "pandas>=1.3.0",
        "numpy>=1.21.0",
        "chardet>=5.0.0",

        # Для модуля dfunc (универсальные функции)
        "python-dateutil>=2.8.0",
    ],
    extras_require={
        # Опциональные зависимости по модулям
        "bitrix24": [
            "requests>=2.31.0",
        ],
        "clickhouse": [
            "aiohttp>=3.8.0",
            "pandas>=1.3.0",
            "numpy>=1.21.0",
        ],
        "full": [
            "requests>=2.31.0",
            "aiohttp>=3.8.0",
            "pandas>=1.3.0",
            "numpy>=1.21.0",
        ],
        # Инструменты разработчика
        "dev": [
            "pytest>=7.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.0",
            "black>=23.0",
            "flake8>=6.0",
            "mypy>=1.0",
            "types-requests>=2.31.0",
            "types-python-dateutil>=2.8.0",
            "tox>=4.0",
            "twine>=4.0",
            "build>=0.10",
        ],
        "test": [
            "pytest>=7.0",
            "pytest-asyncio>=0.21.0",
            "pytest-mock>=3.10",
            "hypothesis>=6.0",
        ],
        "docs": [
            "sphinx>=7.0",
            "sphinx-rtd-theme>=1.3",
            "myst-parser>=2.0",
        ],
    },
    include_package_data=True,
    keywords=[
        "bitrix24",
        "chat",
        "messenger",
        "disk",
        "file",
        "upload",
        "uuid",
        "generator",
        "utilities",
        "async",
        "library",
        "dixpy",
        "clickhouse",
        "logging",
        "loguru",
        "database",
        "tools",
    ],
    license="MIT",
    zip_safe=False,
)