from decimal import Decimal
from typing import Optional

from pydantic.dataclasses import dataclass


@dataclass
class LoanDefault:
    bo_id: int = 0
    loan_id: int = 0
    amount_due: Decimal = Decimal(0.00)
    outstanding_principal: Decimal = Decimal(0.00)
    outstanding_interest: Decimal = Decimal(0.00)
    outstanding_late_fee: Decimal = Decimal(0.00)
    amount_recovered: Decimal = Decimal(0.00)
    legal_fee: Decimal = Decimal(0.00)
    status: str = ''
    id: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
