# import unittest
# import json
#
# from capsphere.ocr.bank_statement.domain import StatementData
# from capsphere.ocr.bank_statement.textract.converter import from_ambank, from_maybank, \
#     from_maybank_sme, from_cimb, from_rhb, from_rhb_reflex, from_hong_leong, from_public_bank, from_alliance
# from capsphere.common.utils import get_test_resource_path, read_list_from_file
# from decimal import Decimal
#
#
# class TestBankConverter(unittest.TestCase):
#
#     alliance_list = read_list_from_file(get_test_resource_path('alliance_list.json'))
#     ambank_islamic_list = read_list_from_file(get_test_resource_path('ambank_islamic_list.json'))
#     ambank_list = read_list_from_file(get_test_resource_path('ambank_list.json'))
#     cimb_islamic_list = read_list_from_file(get_test_resource_path('cimb_islamic_list.json'))
#     cimb_list = read_list_from_file(get_test_resource_path('cimb_list.json'))
#     hong_leong_bizone_list = read_list_from_file(get_test_resource_path('hong_leong_bizone_list.json'))
#     hong_leong_list = read_list_from_file(get_test_resource_path('hong_leong_list.json'))
#
#     # Maybank
#     maybank_islamic_non_sme_4col_list = read_list_from_file(get_test_resource_path('maybank_islamic_non_sme_4col_list.json'))
#     maybank_islamic_non_sme_list = read_list_from_file(get_test_resource_path('maybank_islamic_non_sme_list.json'))
#     maybank_islamic_sme_negative_list = read_list_from_file(get_test_resource_path('maybank_islamic_sme_negative_list.json'))
#     maybank_islamic_sme_positive_list = read_list_from_file(get_test_resource_path('maybank_islamic_sme_positive_list.json'))
#     maybank_non_sme_list = read_list_from_file(get_test_resource_path('maybank_non_sme_list.json'))
#
#     public_bank_negative_list = read_list_from_file(get_test_resource_path('public_bank_negative_list.json'))
#     public_bank_positive_list = read_list_from_file(get_test_resource_path('public_bank_positive_list.json'))
#     rhb_list = read_list_from_file(get_test_resource_path('rhb_list.json'))
#     rhb_reflex_negative_list = read_list_from_file(get_test_resource_path('rhb_reflex_negative_list.json'))
#     rhb_reflex_positive_list = read_list_from_file(get_test_resource_path('rhb_reflex_positive_list.json'))
#
#     def test_func_alliance(self):
#         data = from_alliance(self.alliance_list)
#         self.assertEqual(data.opening_balance, Decimal('32737.10'))
#         self.assertEqual(data.closing_balance, Decimal('21404.39'))
#         self.assertEqual(data.total_debit, Decimal('160003.55'))
#         self.assertEqual(data.total_credit, Decimal('148670.84'))
#         self.assertEqual(data.average_debit, Decimal('5161.40'))
#         self.assertEqual(data.average_credit, Decimal('16518.98'))
#
#     def test_func_ambank(self):
#         data = from_ambank(self.ambank_islamic_list)
#         self.assertEqual(data.opening_balance, Decimal('15355.96'))
#         self.assertEqual(data.closing_balance, Decimal('12312.58'))
#         self.assertEqual(data.total_debit, Decimal('12076.38'))
#         self.assertEqual(data.total_credit, Decimal('9033'))
#         self.assertEqual(data.average_debit, Decimal('1097.85'))
#         self.assertEqual(data.average_credit, Decimal('903.3'))
#
#         data = from_ambank(self.ambank_list)
#         self.assertEqual(data.opening_balance, Decimal('45903.3'))
#         self.assertEqual(data.closing_balance, Decimal('57384.42'))
#         self.assertEqual(data.total_debit, Decimal('256977.28'))
#         self.assertEqual(data.total_credit, Decimal('268458.4'))
#         self.assertEqual(data.average_debit, Decimal('6424.43'))
#         self.assertEqual(data.average_credit, Decimal('14914.36'))
#
#     def test_func_cimb(self):
#         data = from_cimb(self.cimb_islamic_list)
#         self.assertEqual(data.opening_balance, Decimal('28690.55'))
#         self.assertEqual(data.closing_balance, Decimal('9428.64'))
#         self.assertEqual(data.total_debit, Decimal('91961.68'))
#         self.assertEqual(data.total_credit, Decimal('72699.77'))
#         self.assertEqual(data.average_debit, Decimal('1672.03'))
#         self.assertEqual(data.average_credit, Decimal('559.23'))
#
#         data = from_cimb(self.cimb_list)
#         self.assertEqual(data.opening_balance, Decimal('162958.71'))
#         self.assertEqual(data.closing_balance, Decimal('140512.26'))
#         self.assertEqual(data.total_debit, Decimal('358246.45'))
#         self.assertEqual(data.total_credit, Decimal('335800'))
#         self.assertEqual(data.average_debit, Decimal('7961.03'))
#         self.assertEqual(data.average_credit, Decimal('37311.11'))
#
#     def test_func_hong_leong(self):
#         data = from_hong_leong(self.hong_leong_bizone_list)
#         self.assertEqual(data.opening_balance, Decimal('82483.84'))
#         self.assertEqual(data.closing_balance, Decimal('85583.64'))
#         self.assertEqual(data.total_debit, Decimal('79849.60'))
#         self.assertEqual(data.total_credit, Decimal('82949.40'))
#         self.assertEqual(data.average_debit, Decimal('3327.07'))
#         self.assertEqual(data.average_credit, Decimal('27649.80'))
#
#         data = from_hong_leong(self.hong_leong_list)
#         self.assertEqual(data.opening_balance, Decimal('98311.19'))
#         self.assertEqual(data.closing_balance, Decimal('140932.35'))
#         self.assertEqual(data.total_debit, Decimal('463919.24'))
#         self.assertEqual(data.total_credit, Decimal('506540.4'))
#         self.assertEqual(data.average_debit, Decimal('8921.52'))
#         self.assertEqual(data.average_credit, Decimal('84423.4'))
#
#     def test_func_maybank(self):
#         data = from_maybank(self.maybank_islamic_non_sme_4col_list)
#         self.assertEqual(data.opening_balance, Decimal('96.92'))
#         self.assertEqual(data.closing_balance, Decimal('4059.78'))
#         self.assertEqual(data.total_debit, Decimal('10346.45'))
#         self.assertEqual(data.total_credit, Decimal('14309.31'))
#         self.assertEqual(data.average_debit, Decimal('178.39'))
#         self.assertEqual(data.average_credit, Decimal('529.97'))
#
#         data = from_maybank(self.maybank_islamic_non_sme_list)
#         self.assertEqual(data.opening_balance, Decimal('1237.37'))
#         self.assertEqual(data.closing_balance, Decimal('8227.17'))
#         self.assertEqual(data.total_debit, Decimal('15971.80'))
#         self.assertEqual(data.total_credit, Decimal('22961.60'))
#         self.assertEqual(data.average_debit, Decimal('253.52'))
#         self.assertEqual(data.average_credit, Decimal('533.99'))
#
#         data = from_maybank(self.maybank_islamic_sme_negative_list)
#         self.assertEqual(data.opening_balance, Decimal('-38264.64'))
#         self.assertEqual(data.closing_balance, Decimal('-358899.78'))
#         self.assertEqual(data.total_debit, Decimal('1142420.98'))
#         self.assertEqual(data.total_credit, Decimal('821785.84'))
#         self.assertEqual(data.average_debit, Decimal('25387.13'))
#         self.assertEqual(data.average_credit, Decimal('18261.91'))
#
#         data = from_maybank(self.maybank_islamic_sme_positive_list)
#         self.assertEqual(data.opening_balance, Decimal('376997.69'))
#         self.assertEqual(data.closing_balance, Decimal('460682.91'))
#         self.assertEqual(data.total_debit, Decimal('698606.97'))
#         self.assertEqual(data.total_credit, Decimal('782292.19'))
#         self.assertEqual(data.average_debit, Decimal('11089'))
#         self.assertEqual(data.average_credit, Decimal('28973.78'))
#
#         data = from_maybank(self.maybank_non_sme_list)
#         self.assertEqual(data.opening_balance, Decimal('133363.72'))
#         self.assertEqual(data.closing_balance, Decimal('125528.16'))
#         self.assertEqual(data.total_debit, Decimal('66360.26'))
#         self.assertEqual(data.total_credit, Decimal('58524.7'))
#         self.assertEqual(data.average_debit, Decimal('2457.79'))
#         self.assertEqual(data.average_credit, Decimal('2340.99'))
#
#     def test_func_public_bank(self):
#         data = from_public_bank(self.public_bank_negative_list)
#         self.assertEqual(data.opening_balance, Decimal('-188592.74'))
#         self.assertEqual(data.closing_balance, Decimal('-231849.86'))
#         self.assertEqual(data.total_debit, Decimal('427528.21'))
#         self.assertEqual(data.total_credit, Decimal('384271.09'))
#         self.assertEqual(data.average_debit, Decimal('2095.73'))
#         self.assertEqual(data.average_credit, Decimal('4520.84'))
#
#         data = from_public_bank(self.public_bank_positive_list)
#         self.assertEqual(data.opening_balance, Decimal('10792.18'))
#         self.assertEqual(data.closing_balance, Decimal('5770.89'))
#         self.assertEqual(data.total_debit, Decimal('648972.61'))
#         self.assertEqual(data.total_credit, Decimal('643951.32'))
#         self.assertEqual(data.average_debit, Decimal('2627.42'))
#         self.assertEqual(data.average_credit, Decimal('3443.59'))
#
#     def test_func_rhb(self):
#         data = from_rhb(self.rhb_list)
#         self.assertEqual(data.opening_balance, Decimal('9024'))
#         self.assertEqual(data.closing_balance, Decimal('11005.87'))
#         self.assertEqual(data.total_debit, Decimal('23018.13'))
#         self.assertEqual(data.total_credit, Decimal('25000'))
#         self.assertEqual(data.average_debit, Decimal('561.42'))
#         self.assertEqual(data.average_credit, Decimal('6250'))
#
#         data = from_rhb_reflex(self.rhb_reflex_negative_list)
#         self.assertEqual(data.opening_balance, Decimal('-243688.90'))
#         self.assertEqual(data.closing_balance, Decimal('-245186.03'))
#         self.assertEqual(data.total_debit, Decimal('139728.63'))
#         self.assertEqual(data.total_credit, Decimal('138231.50'))
#         self.assertEqual(data.average_debit, Decimal('6351.3'))
#         self.assertEqual(data.average_credit, Decimal('17278.94'))
#
#         data = from_rhb_reflex(self.rhb_reflex_positive_list)
#         self.assertEqual(data.opening_balance, Decimal('371977.49'))
#         self.assertEqual(data.closing_balance, Decimal('252421.21'))
#         self.assertEqual(data.total_debit, Decimal('294550.50'))
#         self.assertEqual(data.total_credit, Decimal('174994.22'))
#         self.assertEqual(data.average_debit, Decimal('253.27'))
#         self.assertEqual(data.average_credit, Decimal('10293.78'))
#
#
# def _assert_statement_data(data: StatementData) -> None:
#     from unittest import TestCase
#
#     TestCase().assertEqual(data.opening_balance, Decimal('2598.60'))
#     TestCase().assertEqual(data.closing_balance, Decimal('1598.50'))
#     TestCase().assertEqual(data.total_debit, Decimal('1300.10'))
#     TestCase().assertEqual(data.total_credit, Decimal('300.00'))
#     TestCase().assertEqual(data.average_debit, Decimal('433.37'))
#     TestCase().assertEqual(data.average_credit, Decimal('100.00'))
#
