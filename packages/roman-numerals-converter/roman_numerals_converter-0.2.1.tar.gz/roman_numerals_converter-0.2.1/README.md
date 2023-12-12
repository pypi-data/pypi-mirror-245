[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![codecov](https://codecov.io/gh/Ceddicedced/roman-numeral-converter/graph/badge.svg?token=04M8K8SJX8)](https://codecov.io/gh/Ceddicedced/roman-numeral-converter)
# Roman Numeral Converter

I developed this python cli for my course "Moderne Softwareentwicklung", provides an easy-to-use interface for converting integers to Roman numerals and vice versa. It uses the Click library to create a user-friendly command-line tool.

## Features

- **Convert Integers to Roman Numerals**: Convert any integer between 1 and 3999 into its corresponding Roman numeral.
- **Convert Roman Numerals to Integers**: Translate valid Roman numerals back into integers.

## Installation

This project uses Poetry for dependency management. To set up the project, follow these steps:

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-repository/roman-numeral-converter.git
   cd roman-numeral-converter
   ```
2. **Install Dependencies**
    Make sure you have Poetry installed. Then run:
    ```bash
    poetry install
    ```
## Usage
After installation, you can use the CLI as follows:

1. **Converting an Integer to a Roman Numeral**

```bash
poetry run python -m roman.your_module_name to-roman [number]
```
Replace [number] with the integer you want to convert.

2. **Converting a Roman Numeral to an Integer**

```bash
poetry run python -m roman.your_module_name from-roman [roman_numeral]
```
Replace [roman_numeral] with the Roman numeral you want to translate.
