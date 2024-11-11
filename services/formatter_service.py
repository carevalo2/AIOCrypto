import locale
from decimal import Decimal


class FormatterService:
    def __init__(self, locale_str: str = 'en_US.UTF-8'):
        locale.setlocale(locale.LC_ALL, locale_str)

    @staticmethod
    def format_currency(value: Decimal) -> str:
        """Formats a Decimal value as currency using locale settings."""
        if value is None:
            return "N/A"
        return locale.currency(value, grouping=True)

    @staticmethod
    def format_percentage(value: float) -> str:
        """Formats a float value as percentage."""
        if value is None:
            return "N/A"
        return f"{value:.2f}%"

    @staticmethod
    def format_time(last_updated: int) -> str:
        if last_updated is None:
            return "N/A"
        return f"<t:{last_updated}:R>"
