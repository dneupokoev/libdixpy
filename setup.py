import re
from pathlib import Path
from setuptools import setup, find_packages


def get_version():
    # Извлечение версии
    init_file = Path(__file__).parent / "libdixpy" / "__init__.py"
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
        init_file.read_text(),
        re.MULTILINE
    ).group(1)
    return version


# Чтение README.md
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

# Чтение CHANGELOG.md
changelog = (this_directory / "CHANGELOG.md").read_text(encoding="utf-8")

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
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=[
        "typing_extensions>=4.0.0; python_version < '3.8'",
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
    },
    include_package_data=True,
    keywords=[
        "uuid",
        "generator",
        "utilities",
        "async",
        "library",
        "dixpy",
    ],
    license="MIT",
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "dixpy-uuid=libdixpy.cli:generate_uuid",
        ],
    },
)
