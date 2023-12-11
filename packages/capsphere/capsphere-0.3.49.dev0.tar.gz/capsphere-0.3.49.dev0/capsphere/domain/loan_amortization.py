from pydantic.dataclasses import dataclass
from typing import Optional
from decimal import Decimal


@dataclass
class LoanAmortization:
    loan_id: int = 0
    month: int = 0
    created_by: str = ''
    updated_by: str = ''
    monthly_payment: Decimal = Decimal(0.00)
    total_amount_paid: Decimal = Decimal(0.00)
    principal_paid: Decimal = Decimal(0.00)
    amount_remaining: Decimal = Decimal(0.00)
    interest_amount: Decimal = Decimal(0.00)
    id: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    due_date: Optional[str] = None
    paid_status: Optional[str] = None
