from enum import Enum


class BankMalaysia(Enum):
    AMBANK = 'ambank'
    CIMB = 'cimb'
    CIMB_ISLAMIC = 'cimb islamic'
    RHB = 'rhb'
    ALLIANCE = 'alliance bank malaysia berhad'
    BANK_ISLAM = 'bank islam'
    MAYBANK = 'maybank'
    PUBLIC_BANK = 'public bank'
    HONG_LEONG = 'hong leong'


bank_columns_mapping = {
    BankMalaysia.AMBANK.value: 6,
    BankMalaysia.CIMB.value: 6,
    BankMalaysia.CIMB_ISLAMIC.value: 6,
    BankMalaysia.RHB.value: 6,
    BankMalaysia.ALLIANCE.value: 6,
    BankMalaysia.BANK_ISLAM.value: 6,
    BankMalaysia.MAYBANK.value: 5,
    BankMalaysia.PUBLIC_BANK.value: 5,
    BankMalaysia.HONG_LEONG.value: 5
}
