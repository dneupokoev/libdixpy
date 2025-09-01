import re
from pathlib import Path
from setuptools import setup, find_packages

def get_version():
    # Извлечение версии
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
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

# Чтение CHANGELOG.md (предполагается, что файл существует)
changelog_path = this_directory / "CHANGELOG.md"
if changelog_path.exists():
    changelog = changelog_path.read_text(encoding="utf-8")
    long_description += "\n\n" + changelog
else:
    # Можно добавить предупреждение или оставить как есть
    pass

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
        "Changelog": "https://github.com/dneupokoev/libdixpy/blob/main/CHANGELOG.md",
        "Bug Tracker": "https://github.com/dneupokoev/libdixpy/issues",
    },
    packages=find_packages(include=["libdixpy", "libdixpy.*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12", # Добавлено, так как используется python:3.12
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=[
        # Основные зависимости
        "typing_extensions>=4.0.0; python_version < '3.8'",
        # --- Добавлены зависимости для db_async_clickhouse ---
        "aiohttp>=3.8.0",
        "pandas>=1.3.0",
        "numpy>=1.21.0",
        "chardet>=5.0.0",
        # --- Добавлены зависимости, видимые из лога установки (для полноты, если используются неявно) ---
        # Обычно они тянутся как зависимости других пакетов, но можно указать явно
        # "python-magic", # Если используется напрямую в других частях libdixpy
        # -------------------------------
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-asyncio",
            "pytest-cov",
            "black>=23.0",
            "flake8>=5.0",
            "mypy>=1.0",
            "types-python-dateutil",
            "tox>=4.0",
            "twine",
            "build",
        ],
        "async": [
            "asyncio>=3.4; python_version < '3.7'",
            # aiohttp уже в основных зависимостях
        ],
        "test": [
            "pytest-mock",
            "hypothesis",
        ],
        "docs": [
            "sphinx>=5.0",
            "sphinx-rtd-theme",
            "myst-parser",
        ],
        # --- Пример группы для ClickHouse, если решите делать её опциональной ---
        # "clickhouse": [
        #     "aiohttp>=3.8.0",
        #     "pandas>=1.3.0",
        #     "numpy>=1.21.0",
        #     "chardet>=5.0.0",
        # ],
        # -------------------------------------------------------------------------
    },
    include_package_data=True,
    keywords=[
        "uuid",
        "generator",
        "utilities",
        "async",
        "library",
        "dixpy",
        "clickhouse", # Добавлено, так как теперь есть поддержка ClickHouse
    ],
    license="MIT",
    zip_safe=False,
    # entry_points={ # Предполагается, что cli.py существует. Если нет, закомментируйте.
    #     "console_scripts": [
    #         "dixpy-uuid=libdixpy.cli:generate_uuid",
    #     ],
    # },
)
