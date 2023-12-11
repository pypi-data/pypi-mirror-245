import logging
import pandas as pd
import re

from decimal import Decimal

from capsphere.ocr.bank_statement.domain import StatementData
from capsphere.ocr.bank_statement.utils import __format_column
from capsphere.common.utils import generate_statement_data

TWO_PLACES = Decimal(10) ** -2

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.ERROR)
logging.getLogger(__name__).setLevel(logging.DEBUG)


def from_ambank(transactions: list) -> StatementData:
    df = pd.DataFrame(transactions)

    # filter if contains number
    filtered_df = df[df[1].str.contains(r'\d', na=False)]
    filtered_df = filtered_df.reset_index(drop=True)

    transformed_df = filtered_df.groupby((~df[1].isnull()).cumsum()).agg({1: 'first',
                                                                          2: lambda x: '\n'.join(x),
                                                                          3: 'first',
                                                                          4: 'first',
                                                                          5: 'first',
                                                                          6: 'first'}).fillna('')

    transformed_df['date'] = transformed_df[1]
    transformed_df['transaction'] = transformed_df[2]
    transformed_df['cheque'] = transformed_df[3]
    transformed_df['debit'] = __format_column(transformed_df[4])
    transformed_df['credit'] = __format_column(transformed_df[5])
    transformed_df['balance'] = __format_column(transformed_df[6])

    total_debit = pd.to_numeric(transformed_df['debit']).sum()
    total_credit = pd.to_numeric(transformed_df['credit']).sum()
    # this is important to get count on debit & credit transactions only if rows have values
    total_deb_transactions = len(transformed_df[transformed_df[4].str.contains(r'\d', na=False)])
    total_cred_transactions = len(transformed_df[transformed_df[5].str.contains(r'\d', na=False)])

    # opening balance
    if transformed_df['debit'].iloc[0] != '0.00':
        opening_balance = pd.to_numeric(transformed_df['balance'].iloc[0]) + pd.to_numeric(
            transformed_df['debit'].iloc[0])
    else:
        opening_balance = pd.to_numeric(transformed_df['balance'].iloc[0]) - pd.to_numeric(
            transformed_df['credit'].iloc[0])

    date = transformed_df['date'].iloc[-1]
    closing_balance = transformed_df['balance'].iloc[-1]
    average_debit = total_debit / total_deb_transactions
    average_credit = total_credit / total_cred_transactions

    return generate_statement_data(date, opening_balance, closing_balance,
                         total_debit, total_credit, average_debit, average_credit)


def from_maybank(transactions: list) -> StatementData:
    df = pd.DataFrame(transactions)

    # SME Maybank statement, it will shows the END OF STATEMENT in the third column. Use another function.
    contains_end_of_statement = (df[3].str.contains('END OF STATEMENT')).any()
    if contains_end_of_statement:
        LOGGER.info("Change of Maybank function to the SME one.")
        return from_maybank_sme(transactions)

    # Maybank with 4 columns statement.
    if df.shape[1] == 4:
        LOGGER.info("Maybank with four columns.")
        # filter out if contains string
        filtered_df = df[~df[1].str.contains('[a-zA-Z]')]
        # filter the first column if contains number
        filtered_df = filtered_df[filtered_df[1].str.contains(r'\d', na=False)]

    else:
        # Maybank with 5 columns statement.
        LOGGER.info("Maybank with five columns.")
        # filter the 4th column if contains number
        filtered_df = df[df[4].str.contains(r'\d', na=False)]

        # For 4 & 5 column to be working using same function, need to remove the 2nd column not in use for 5 column dataframe
        column_to_remove = 2
        filtered_df = filtered_df.drop(column_to_remove, axis=1)

        new_column_names = [1,2,3,4]
        filtered_df.columns = new_column_names
    
    # If no transactions at all
    if len(filtered_df) == 0:
        return 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 'N/A'

    # For combined transactions, most probably happen to 5 column dataframe
    filtered_df_copy = filtered_df.copy()
    deleted_index = []
    for index, value in enumerate(filtered_df[1]):
        new_list = [
            ['', '', '', ''],
            ['', '', '', '']
        ]
        if len(value.split(' ')[1]) > 1:
            new_list[0][0] = value.split(' ')[0]
            new_list[1][0] = value.split(' ')[1]
            if len(filtered_df.iloc[index][3]) != 0:
                new_list[0][2] = filtered_df.iloc[index][3].split(' ')[0]
                new_list[1][2] = filtered_df.iloc[index][3].split(' ')[1]
            if len(filtered_df.iloc[index][4]) != 0:
                new_list[0][3] = filtered_df.iloc[index][4].split(' ')[0]
                new_list[1][3] = filtered_df.iloc[index][4].split(' ')[1]

            new_df = pd.DataFrame(new_list, columns=[1, 2, 3, 4])
            deleted_index.append(index)
            filtered_df_copy = pd.concat([filtered_df, new_df], ignore_index=True)
    
    # Delete index for rows with combined transactions
    for index in deleted_index:
        filtered_df_copy = filtered_df_copy.drop(index)


    transformed_df = filtered_df_copy.groupby((~df[1].isnull()).cumsum()).agg({1: 'first',
                                                                          2: lambda x: '\n'.join(x),
                                                                          3: 'first',
                                                                          4: 'first'}).fillna('')

    transformed_df['date'] = transformed_df[1]
    transformed_df['transaction'] = transformed_df[2]
    transformed_df['debit'] = __format_column(
        transformed_df[~transformed_df[3].str.contains('\+')][3].str.replace('-', '', regex=False))
    transformed_df['credit'] = __format_column(
        transformed_df[transformed_df[3].str.contains('\+')][3].str.replace('+', '', regex=False))
    transformed_df['balance'] = __format_column(transformed_df[4])

    total_debit = pd.to_numeric(transformed_df['debit']).sum()
    total_credit = pd.to_numeric(transformed_df['credit']).sum()
    # this is important to get count on debit & credit transactions only if rows have values
    total_deb_transactions = len(transformed_df[transformed_df[3].str.contains('\-')])
    total_cred_transactions = len(transformed_df[transformed_df[3].str.contains('\+')])

    # check if first row of balance is combined together with beginning balance
    split_value = (transformed_df['balance'].iloc[0]).split(' ')
    if len(split_value[1]) > 1:
        opening_balance = split_value[1]
    else:
        opening_balance = split_value[0]

    # opening balance
    if '-' in transformed_df.iloc[0][3]:
        opening_balance = pd.to_numeric(opening_balance) + pd.to_numeric(
            transformed_df['debit'].iloc[0])
    else:
        opening_balance = pd.to_numeric(opening_balance) - pd.to_numeric(
            transformed_df['credit'].iloc[0])

    closing_balance = __format_column(filtered_df[filtered_df[4].str.contains(r'\d', na=False)][4])
    closing_balance = closing_balance.iloc[-1]

    date = filtered_df[filtered_df[1].str.contains(r'\d', na=False)][1]
    date = date.iloc[-1]
    average_debit = total_debit / total_deb_transactions
    average_credit = total_credit / total_cred_transactions

    return generate_statement_data(date, opening_balance, closing_balance,
                         total_debit, total_credit, average_debit, average_credit)


def from_maybank_sme(transactions: list) -> StatementData:

    # SME Banks has spacing between number and credit/debit icon (+/-)
    df = pd.DataFrame(transactions)

    filtered_df_one = df[df[4].str.contains(r'\d', na=False) | df[5].str.contains(r'\d', na=False)]
    opening_balance = filtered_df_one.iloc[0][4].replace(',', '')
    opening_balance = opening_balance.replace('(', '-')
    opening_balance = opening_balance.replace(')', '')

    filtered_df_two = filtered_df_one[filtered_df_one[1] != '']
    filtered_df_two = filtered_df_two.reset_index(drop=True)

    # For any combined transactions, need to split
    # 1st check for balance column, due to last transaction row combined with summary of balances
    # 2nd check for date column, if date column has two combined transactions so it's not the last row
    deleted_index = []
    for index, value in enumerate(filtered_df_two[1]):
        new_list = [
            ['', '', '', '', ''],
            ['', '', '', '', '']
        ]

        combined_value = filtered_df_two.iloc[index][4]
        # Use regular expression to split the string into numbers and plus signs
        split_value = re.findall(r'\d{1,3}(?:,?\d{3})*(?:\.\d+)?(?:\s*\+\s*)?', combined_value)   
        if len(split_value) > 1:

            # Define a pattern where two dates combine together in a row (15 Aug 2022 16 Aug 2022)
            pattern = r'(?<=\d)\s(?=\d)'
            # Split the input string using the pattern
            split_date = re.split(pattern, value)
            
            if len(split_date) > 1:
                # If two transaction rows combined

                new_list[0][0] = split_date[0]
                new_list[1][0] = split_date[1]
                new_list[0][3] = split_value[0]
                new_list[1][3] = split_value[1]
                new_df = pd.DataFrame(new_list, columns=[1, 2, 3, 4, 5])
                deleted_index.append(index)
                filtered_df_two = pd.concat([filtered_df_two, new_df], ignore_index=True)

            elif len(split_date) == 1:
                # If the last transaction row combined with summary of balances

                combined_balance = filtered_df_two.iloc[index][5]
                # Use regular expression to split the string into numbers and plus signs
                split_balance = re.findall(r'\d{1,3}(?:,?\d{3})*(?:\.\d+)?(?:\s*\+\s*)?', combined_balance)

                new_list[0][0] = split_date[0]
                new_list[0][3] = split_value[0]
                new_list[0][4] = split_balance[0]
                new_df = pd.DataFrame(new_list, columns=[1, 2, 3, 4, 5])
                deleted_index.append(index)
                filtered_df_two = pd.concat([filtered_df_two, new_df], ignore_index=True)
    
    # Delete index for rows with combined transactions
    for index in deleted_index:
        filtered_df_two = filtered_df_two.drop(index)

    transformed_df = filtered_df_two.groupby((~df[1].isnull()).cumsum()).agg({1: 'first',
                                                                          2: lambda x: '\n'.join(x),
                                                                          3: 'first',
                                                                          4: 'first',
                                                                          5: 'first'}).fillna('')

    transformed_df['date'] = transformed_df[1]
    transformed_df['transaction'] = transformed_df[3]
    transformed_df['debit'] = __format_column(transformed_df[~transformed_df[4].str.contains('\+')][4].str.replace('-', '', regex=False))
    transformed_df['credit'] = __format_column(transformed_df[transformed_df[4].str.contains('\+')][4].str.replace('+', '', regex=False))
    transformed_df['balance'] = __format_column(transformed_df[transformed_df[5] != ''][5])

    total_debit = pd.to_numeric(transformed_df['debit']).sum()
    total_credit = pd.to_numeric(transformed_df['credit']).sum()
    total_deb_transactions = len(transformed_df[~transformed_df[4].str.contains('\+')])
    total_cred_transactions = len(transformed_df[transformed_df[4].str.contains('\+')])

    closing_balance = __format_column(transformed_df[transformed_df['balance'].str.contains(r'\d', na=False)][5])
    closing_balance = closing_balance.iloc[-1]

    # Due to closing balance with negative undetected by Textract, we have to do it manually.
    if Decimal(total_debit - total_credit) > Decimal(opening_balance):
        if '-' not in closing_balance:
            closing_balance = '-' + closing_balance

    date = transformed_df['date'].iloc[0]
    average_debit = total_debit / total_deb_transactions
    average_credit = total_credit / total_cred_transactions

    return generate_statement_data(date, opening_balance, closing_balance,
                         total_debit, total_credit, average_debit, average_credit)


def from_cimb(transactions: list) -> StatementData:
    df = pd.DataFrame(transactions)

    # filter if contains number
    filtered_df = df[df[1].str.contains(r'\d', na=False)]
    filtered_df = filtered_df.reset_index(drop=True)

    transformed_df = filtered_df.groupby((~df[1].isnull()).cumsum()).agg({1: 'first',
                                                                          2: lambda x: '\n'.join(x),
                                                                          3: 'first',
                                                                          4: 'first',
                                                                          5: 'first',
                                                                          6: 'first'}).fillna('')

    transformed_df['date'] = transformed_df[1]
    transformed_df['transaction'] = transformed_df[2]
    transformed_df['cheque'] = transformed_df[3]
    transformed_df['debit'] = __format_column(transformed_df[4])
    transformed_df['credit'] = __format_column(transformed_df[5])
    transformed_df['balance'] = __format_column(transformed_df[6])

    total_debit = pd.to_numeric(transformed_df['debit']).sum()
    total_credit = pd.to_numeric(transformed_df['credit']).sum()
    # this is important to get count on debit & credit transactions only if rows have values
    total_deb_transactions = len(transformed_df[transformed_df[4].str.contains(r'\d', na=False)])
    total_cred_transactions = len(transformed_df[transformed_df[5].str.contains(r'\d', na=False)])

    # opening balance
    if transformed_df['debit'].iloc[-1] != '0.00':
        opening_balance = pd.to_numeric(transformed_df['balance'].iloc[-1]) + pd.to_numeric(
            transformed_df['debit'].iloc[-1])
    else:
        opening_balance = pd.to_numeric(transformed_df['balance'].iloc[-1]) - pd.to_numeric(
            transformed_df['credit'].iloc[-1])

    date = transformed_df['date'].iloc[-1]
    closing_balance = transformed_df['balance'].iloc[0]
    average_debit = total_debit / total_deb_transactions
    average_credit = total_credit / total_cred_transactions

    return generate_statement_data(date, opening_balance, closing_balance,
                         total_debit, total_credit, average_debit, average_credit)


def from_rhb(transactions: list) -> StatementData:
    # Custom function for RHB - when the textract detects as 7 columns instead of 6 columns
    for index, transaction in enumerate(transactions):
        if (len(transaction) == 7):
            new_dict = {}
            new_dict[1] = transaction[1]
            new_dict[2] = transaction[2]
            new_dict[3] = transaction[4]
            new_dict[4] = transaction[5]
            new_dict[5] = transaction[6]
            new_dict[6] = transaction[7]

            transactions[index] = new_dict

    df = pd.DataFrame(transactions)

    # filter if contains number
    filtered_df = df[df[1].str.contains(r'\d', na=False)]
    filtered_df = filtered_df.reset_index(drop=True)

    transformed_df = filtered_df.groupby((~df[1].isnull()).cumsum()).agg({1: 'first',
                                                                          2: lambda x: '\n'.join(x),
                                                                          3: 'first',
                                                                          4: 'first',
                                                                          5: 'first',
                                                                          6: 'first'}).fillna('')

    transformed_df['date'] = transformed_df[1]
    transformed_df['transaction'] = transformed_df[2]
    transformed_df['cheque'] = transformed_df[3]
    transformed_df['debit'] = __format_column(transformed_df[4])
    transformed_df['credit'] = __format_column(transformed_df[5])
    transformed_df['balance'] = __format_column(transformed_df[6])

    total_debit = pd.to_numeric(transformed_df['debit']).sum()
    total_credit = pd.to_numeric(transformed_df['credit']).sum()
    # this is important to get count on debit & credit transactions only if rows have values
    total_deb_transactions = len(transformed_df[transformed_df[4].str.contains(r'\d', na=False)])
    total_cred_transactions = len(transformed_df[transformed_df[5].str.contains(r'\d', na=False)])

    date = transformed_df['date'].iloc[-1]
    opening_balance = transformed_df['balance'].iloc[0]
    closing_balance = transformed_df['balance'].iloc[-1]
    average_debit = total_debit / total_deb_transactions
    average_credit = total_credit / total_cred_transactions

    return generate_statement_data(date, opening_balance, closing_balance,
                         total_debit, total_credit, average_debit, average_credit)


def from_rhb_reflex(transactions: list) -> StatementData:
    # Custom function for RHB Reflex - when the textract detects as 9 columns instead of 10 columns
    for index, transaction in enumerate(transactions):
        if (len(transaction) == 9):
            new_dict = {}
            new_dict[1] = transaction[1]
            new_dict[2] = transaction[2]
            new_dict[3] = transaction[3]
            new_dict[4] = ''
            new_dict[5] = ''
            new_dict[6] = ''
            new_dict[7] = ''
            new_dict[8] = transaction[7]
            new_dict[9] = transaction[8]
            new_dict[10] = transaction[9]

            transactions[index] = new_dict

    df = pd.DataFrame(transactions)

    # filter if contains number
    filtered_df = df[df[10].str.contains(r'\d', na=False)]
    filtered_df = filtered_df.reset_index(drop=True)

    transformed_df = filtered_df.groupby((~df[1].isnull()).cumsum()).agg({1: 'first',
                                                                          2: 'first',
                                                                          3: 'first',
                                                                          8: 'first',
                                                                          9: 'first',
                                                                          10: 'first'}).fillna('')

    transformed_df['date'] = transformed_df[1]
    transformed_df['branch'] = transformed_df[2]
    transformed_df['description'] = transformed_df[3]
    transformed_df['debit'] = __format_column(transformed_df[8].str.replace('-', '', regex=False))
    transformed_df['credit'] = __format_column(transformed_df[9].str.replace('-', '', regex=False))
    transformed_df['balance'] = __format_column(transformed_df[10])

    total_debit = pd.to_numeric(transformed_df['debit'].str.strip()).sum()
    total_credit = pd.to_numeric(transformed_df['credit'].str.strip()).sum()
    # this is important to get count on debit & credit transactions only if rows have values
    total_deb_transactions = len(transformed_df[transformed_df[8].str.contains(r'\d', na=False)])
    total_cred_transactions = len(transformed_df[transformed_df[9].str.contains(r'\d', na=False)])

    # opening balance
    opening_balance = transformed_df['balance'].iloc[0]
    if '-' in opening_balance:
        opening_balance = opening_balance.replace('-', '')
        opening_balance = '-' + opening_balance

    if '+' in opening_balance:
        opening_balance = opening_balance.replace('+', '')

    if transformed_df['debit'].iloc[0] != " ":
        opening_balance = pd.to_numeric(opening_balance) + pd.to_numeric(
            transformed_df['debit'].iloc[0])
    else:
        opening_balance = pd.to_numeric(opening_balance) - pd.to_numeric(
            transformed_df['credit'].iloc[0])

    # closing balance
    closing_balance = transformed_df['balance'].iloc[-1]
    if '-' in closing_balance:
        closing_balance = closing_balance.replace('-', '')
        closing_balance = '-' + closing_balance

    if '+' in closing_balance:
        closing_balance = closing_balance.replace('+', '')

    date = transformed_df['date'].iloc[-1]
    average_debit = total_debit / total_deb_transactions
    average_credit = total_credit / total_cred_transactions

    return generate_statement_data(date, opening_balance, closing_balance,
                         total_debit, total_credit, average_debit, average_credit)


def from_hong_leong(transactions: list) -> StatementData:
    df = pd.DataFrame(transactions)

    # filter if contains number
    filtered_df = df[df[1].str.contains(r'\d', na=False)]
    filtered_df = filtered_df.reset_index(drop=True)

    # if two rows get combined, separate into two new rows
    deleted_index = []
    for index, value in enumerate(filtered_df[1]):
        new_list = [
            ['', '', '', '', ''],
            ['', '', '', '', '']
        ]
        if len(value.split(' ')[1]) > 1:
            new_list[0][0] = value.split(' ')[0]
            new_list[1][0] = value.split(' ')[1]
            if len(filtered_df.iloc[index][3]) != 0:
                new_list[0][2] = filtered_df.iloc[index][3].split(' ')[0]
                new_list[1][2] = filtered_df.iloc[index][3].split(' ')[1]
            if len(filtered_df.iloc[index][4]) != 0:
                new_list[0][3] = filtered_df.iloc[index][4].split(' ')[0]
                new_list[1][3] = filtered_df.iloc[index][4].split(' ')[1]

            new_df = pd.DataFrame(new_list, columns=[1, 2, 3, 4, 5])
            deleted_index.append(index)
            # combine new row with the DataFrame
            filtered_df = pd.concat([filtered_df, new_df], ignore_index=True)

    # Delete index for rows with combined transactions
    for index in deleted_index:
        filtered_df = filtered_df.drop(index)

    transformed_df = filtered_df.groupby((~df[1].isnull()).cumsum()).agg({1: 'first',
                                                                          2: lambda x: '\n'.join(x),
                                                                          3: 'first',
                                                                          4: 'first',
                                                                          5: 'first'}).fillna('')

    transformed_df['date'] = transformed_df[1]
    transformed_df['transaction'] = transformed_df[2]
    transformed_df['credit'] = __format_column(transformed_df[3])
    transformed_df['debit'] = __format_column(transformed_df[4])
    transformed_df['balance'] = __format_column(transformed_df[5])

    total_credit = pd.to_numeric(transformed_df['credit']).sum()
    total_debit = pd.to_numeric(transformed_df['debit']).sum()
    # this is important to get count on debit & credit transactions only if rows have values
    total_cred_transactions = len(transformed_df[transformed_df[3].str.contains(r'\d', na=False)])
    total_deb_transactions = len(transformed_df[transformed_df[4].str.contains(r'\d', na=False)])

    # opening balance
    opening_balance = df.iloc[1][5].replace(',', '')
    # closing balance
    other_filtered_df = df[df[1].str.contains(r'\d', na=False)]
    last_row_with_number = other_filtered_df[other_filtered_df[5].str.contains('\d', na=False)].tail(1)
    closing_balance = __format_column(last_row_with_number[5])
    closing_balance = pd.to_numeric(closing_balance).sum()

    date = other_filtered_df[1].iloc[-1]
    average_debit = total_debit / total_deb_transactions
    average_credit = total_credit / total_cred_transactions

    return generate_statement_data(date, opening_balance, closing_balance,
                         total_debit, total_credit, average_debit, average_credit)


def from_public_bank(transactions: list) -> StatementData:
    # Custom function PUBLIC BANK - with only credit transactions, it will get as 4 columns instead of 5
    for index, transaction in enumerate(transactions):
        if len(transaction) == 4:
            new_dict = {}
            new_dict[1] = transaction[1]
            new_dict[2] = transaction[2]
            new_dict[3] = ''
            # if comma(,) detected as (.)
            if transaction[3].count(".") > 1:
                transaction[3] = transaction[3].replace(".", "", transaction[3].count(".") - 1)
            new_dict[4] = transaction[3]
            new_dict[5] = transaction[4]
            transactions[index] = new_dict

    df = pd.DataFrame(transactions)

    # filter if contains number
    filtered_df = df[df[5].str.contains(r'\d', na=False)]
    filtered_df = filtered_df.reset_index(drop=True)

    # if two columns (transaction and debit) get combined, need to break that string apart for debit column
    def extract_and_sum_prices(text):
        prices = re.findall(r'(\d{1,3}(?:,\d{3})*\.\d{2})', text)
        numeric_prices = [float(price.replace(',', '')) for price in prices]
        return sum(numeric_prices)

    # if two rows (debit and debit) get combined, need to break it and find sum
    filtered_df[3] = filtered_df[3].apply(extract_and_sum_prices)
    filtered_df[3] = filtered_df[3].apply(lambda x: f"{x:.2f}")

    # if two rows get combined, separate into two rows
    deleted_index = []
    for index, value in enumerate(filtered_df[4]):
        if value != '':
            if len(value.split(' ')[1]) > 1:
                new_list = [
                    ['', '', '', '', ''],
                    ['', '', '', '', '']
                ]
                new_list[0][3] = filtered_df.iloc[index][4].split(' ')[0]
                new_list[0][1] = filtered_df.iloc[index][2]
                new_list[1][3] = filtered_df.iloc[index][4].split(' ')[1]
                new_list[1][1] = filtered_df.iloc[index][2]

                new_df = pd.DataFrame(new_list, columns=[1, 2, 3, 4, 5])
                deleted_index.append(index)
                # combine new row with the DataFrame
                filtered_df = pd.concat([filtered_df, new_df], ignore_index=True)

    # Delete index for rows with combined transactions
    for index in deleted_index:
        filtered_df = filtered_df.drop(index)

    transformed_df = filtered_df.groupby((~df[1].isnull()).cumsum()).agg({1: 'first',
                                                                          2: lambda x: '\n'.join(x),
                                                                          3: 'first',
                                                                          4: 'first',
                                                                          5: 'first'}).fillna('')

    transformed_df['date'] = transformed_df[1]
    transformed_df['transaction'] = transformed_df[2]
    transformed_df['debit'] = __format_column(transformed_df[3])
    transformed_df['credit'] = __format_column(transformed_df[4])
    transformed_df['balance'] = __format_column(transformed_df[5])

    total_debit = pd.to_numeric(transformed_df['debit']).sum()
    total_credit = pd.to_numeric(transformed_df['credit']).sum()
    # this is important to get count on debit & credit transactions only if rows have values
    total_deb_transactions = len(transformed_df[transformed_df[3].str.contains(r'\d', na=False)])
    total_cred_transactions = len(transformed_df[transformed_df[4].str.contains(r'\d', na=False)])

    # last date
    last_row_with_date = filtered_df[filtered_df[1].str.contains('\d', na=False)].tail(1)
    date = last_row_with_date[1].to_string(index=False)

    # opening balance
    opening_balance = transformed_df['balance'].iloc[0]
    if 'OD' in opening_balance:
        opening_balance = opening_balance.replace('OD', '')
        opening_balance = '-' + opening_balance

    # closing balance
    last_row_with_balance = filtered_df[filtered_df[5].str.contains('\d', na=False)]
    closing_balance = __format_column(last_row_with_balance.iloc[-1])
    closing_balance = closing_balance[5]
    if 'OD' in closing_balance:
        closing_balance = closing_balance.replace('OD', '')
        closing_balance = '-' + closing_balance

    average_debit = total_debit / total_deb_transactions
    average_credit = total_credit / total_cred_transactions

    return generate_statement_data(date, opening_balance, closing_balance,
                         total_debit, total_credit, average_debit, average_credit)


def from_alliance(transactions: list) -> StatementData:
    # Tested for scanned docs, if period (.) detected as comma (,)
    for index, transaction in enumerate(transactions):
        if transaction[4].count(".") == 0 and transaction[4].count(",") == 1:
            transaction[4] = transaction[4].replace(",", ".")

    df = pd.DataFrame(transactions)

    # filter if contains number
    filtered_df = df[df[1].str.contains(r'\d', na=False)]
    filtered_df = filtered_df.reset_index(drop=True)

    transformed_df = filtered_df.groupby((~df[1].isnull()).cumsum()).agg({1: 'first',
                                                                          2: lambda x: '\n'.join(x),
                                                                          3: 'first',
                                                                          4: 'first',
                                                                          5: 'first',
                                                                          6: 'first'}).fillna('')

    transformed_df['date'] = transformed_df[1]
    transformed_df['transaction'] = transformed_df[2]
    transformed_df['cheque'] = transformed_df[3]
    transformed_df['debit'] = __format_column(transformed_df[4])
    transformed_df['credit'] = __format_column(transformed_df[5])
    transformed_df['balance'] = __format_column(transformed_df[6].str.replace('CR', '').str.replace('DR', '-'))

    total_debit = pd.to_numeric(transformed_df['debit']).sum()
    total_credit = pd.to_numeric(transformed_df['credit']).sum()
    # this is important to get count on debit & credit transactions only if rows have values
    total_deb_transactions = len(transformed_df[transformed_df[4].str.contains(r'\d', na=False)])
    total_cred_transactions = len(transformed_df[transformed_df[5].str.contains(r'\d', na=False)])

    # opening balance
    if transformed_df['debit'].iloc[0] != '0.00':
        opening_balance = pd.to_numeric(transformed_df['balance'].iloc[0]) + pd.to_numeric(
            transformed_df['debit'].iloc[0])
    else:
        opening_balance = pd.to_numeric(transformed_df['balance'].iloc[0]) - pd.to_numeric(
            transformed_df['credit'].iloc[0])

    date = transformed_df['date'].iloc[-1]
    closing_balance = transformed_df['balance'].iloc[-1]
    average_debit = total_debit / total_deb_transactions
    average_credit = total_credit / total_cred_transactions

    return generate_statement_data(date, opening_balance, closing_balance,
                         total_debit, total_credit, average_debit, average_credit)


def from_maybank_islamic(transactions: list) -> StatementData:
    raise NotImplementedError('Maybank Islamic function not implemented')
