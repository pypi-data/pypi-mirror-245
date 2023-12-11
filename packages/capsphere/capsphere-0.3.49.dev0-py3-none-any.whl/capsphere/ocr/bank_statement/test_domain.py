# import unittest
#
# from capsphere.ocr.bank_statement.domain import StatementData
# from decimal import Decimal
#
#
# class TestDomain(unittest.TestCase):
#
#     def test_valid_statement_data(self):
#         # Valid data
#         statement = StatementData(
#             date="2023-07-15",
#             opening_balance=Decimal("1000.00"),
#             closing_balance=Decimal("1500.00"),
#             total_debit=Decimal("500.00"),
#             total_credit=Decimal("800.00"),
#             average_debit=Decimal("50.00"),
#             average_credit=Decimal("80.00")
#         )
#         self.assertIsInstance(statement, StatementData)
#
#     def test_invalid_statement_data(self):
#         # Invalid data (opening_balance is not a Decimal)
#         with self.assertRaises(TypeError):
#             StatementData(
#                 date="2023-07-15",
#                 opening_balance=1000.00,
#                 closing_balance=Decimal("1500.00"),
#                 total_debit=Decimal("500.00"),
#                 total_credit=Decimal("800.00"),
#                 average_debit=Decimal("50.00"),
#                 average_credit=Decimal("80.00")
#             )
#
#         # Invalid data (date is not a str)
#         with self.assertRaises(TypeError):
#             StatementData(
#                 date=2023,  # Should be "2023-07-15"
#                 opening_balance=Decimal("1000.00"),
#                 closing_balance=Decimal("1500.00"),
#                 total_debit=Decimal("500.00"),
#                 total_credit=Decimal("800.00"),
#                 average_debit=Decimal("50.00"),
#                 average_credit=Decimal("80.00")
#             )
