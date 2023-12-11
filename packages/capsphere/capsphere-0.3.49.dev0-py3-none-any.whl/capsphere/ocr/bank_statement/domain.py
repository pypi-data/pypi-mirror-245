from dataclasses import dataclass
from decimal import Decimal


@dataclass
class StatementData:
    date: str
    opening_balance: Decimal
    closing_balance: Decimal
    total_debit: Decimal
    total_credit: Decimal
    average_debit: Decimal
    average_credit: Decimal

    def __post_init__(self):
        for field_name, field_type in self.__annotations__.items():
            field_value = getattr(self, field_name)
            if not isinstance(field_value, field_type):
                raise TypeError(f"{field_name} must be of type {field_type.__name__}, "
                                f"got {type(field_value).__name__} instead")
