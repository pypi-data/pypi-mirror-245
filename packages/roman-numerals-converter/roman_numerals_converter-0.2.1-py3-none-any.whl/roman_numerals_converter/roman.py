"""Roman numerals converter.
This script provides a command-line interface to convert numbers to Roman numerals and vice versa.
"""  # noqa: E501

import re

# Regular expression for validating Roman numerals
ROMAN_REGEX = r"^(?=.)M{0,3}(C[MD]|D?C{0,3})(X[CL]|L?X{0,3})(I[XV]|V?I{0,3})$"


class RomanError(Exception):
    """Base class for exceptions in this module."""

    pass


class RomanNumeral:
    """Class for converting Roman numerals to decimal numbers and vice versa.
    This class provides a constructor for creating a RomanNumeral object from a
    Roman numeral or a decimal number. It also provides methods for converting
    a Roman numeral to a decimal number and vice versa.
    """

    def __init__(self, value: str) -> None:
        """Constructor for RomanNumeral class.
        Args:
            value (str): A Roman numeral or a decimal number.
        """
        # Validate input
        if not isinstance(value, str):
            raise RomanError("Please enter a string.")

        # Check if the input is a Roman numeral
        if not self.is_valid_roman(value):
            raise RomanError("Please enter a valid Roman numeral.")

        self._value = value

    def to_decimal(self) -> int:
        """Convert a Roman numeral to a decimal number.
        Returns:
            int: The decimal representation of the Roman numeral.
        """

        # Mapping of Roman numerals to decimal numbers
        roman_numerals = [
            ("M", 1000),
            ("CM", 900),
            ("D", 500),
            ("CD", 400),
            ("C", 100),
            ("XC", 90),
            ("L", 50),
            ("XL", 40),
            ("X", 10),
            ("IX", 9),
            ("V", 5),
            ("IV", 4),
            ("I", 1),
        ]

        # Conversion process
        decimal = 0
        for numeral, value in roman_numerals:
            while self._value.startswith(numeral):
                decimal += value
                self._value = self._value[len(numeral) :]

        return decimal

    def __str__(self) -> str:
        """Convert a Roman numeral to a string.
        Returns:
            str: The Roman numeral representation of the object.
        """
        return self._value

    @staticmethod
    def is_valid_roman(value: str) -> bool:
        """Check if a string is a valid Roman numeral.
        Args:
            value (str): A string to be checked.
        Returns:
            bool: True if the string is a valid Roman numeral, False otherwise.
        """
        return bool(re.search(ROMAN_REGEX, value) is not None)

    @classmethod
    def from_decimal(cls, number: int) -> "RomanNumeral":
        """Convert a decimal number to a Roman numeral.
        Args:
            number (int): A decimal number.
        Returns:
            str: The Roman numeral representation of the decimal number.
        """
        if not isinstance(number, int):
            raise RomanError("Please enter an integer.")

        # Check that the number is within the valid range
        if not 0 < number < 4000:
            raise RomanError("Please enter a number between 1 and 3999.")

        # Mapping of decimal numbers to Roman numerals
        roman_numerals = [
            (1000, "M"),
            (900, "CM"),
            (500, "D"),
            (400, "CD"),
            (100, "C"),
            (90, "XC"),
            (50, "L"),
            (40, "XL"),
            (10, "X"),
            (9, "IX"),
            (5, "V"),
            (4, "IV"),
            (1, "I"),
        ]

        # Conversion process
        roman = ""
        for value, numeral in roman_numerals:
            while number >= value:
                roman += numeral
                number -= value

        return cls(roman)
