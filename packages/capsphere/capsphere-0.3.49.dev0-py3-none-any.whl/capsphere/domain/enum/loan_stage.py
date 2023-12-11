from enum import Enum


class LoanStage(Enum):
    NORMAL = "NORMAL"
    DEFAULTED = "DEFAULTED"
    EXPIRED = "EXPIRED"


class PaidStatus(Enum):
    PAID = "Borrower Paid",
    MISS = "Miss"
