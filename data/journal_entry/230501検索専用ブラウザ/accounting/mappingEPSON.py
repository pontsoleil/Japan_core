#!/usr/bin/env python3
# coding: utf-8
#
# mapping from accounting soft CSV to Tidy data CSV
#
# designed by SAMBUICHI, Nobuyuki (Sambuichi Professional Engineers Office)
# written by SAMBUICHI, Nobuyuki (Sambuichi Professional Engineers Office)
#
# MIT License
#
# (c) 2023 SAMBUICHI Nobuyuki (Sambuichi Professional Engineers Office)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# from jsonschema import validate
from cgi import print_directory
# from distutils.debug import DEBUG
# import json
# from pyrsistent import b
import argparse
import os
# import yaml
import sys
import csv
import re
# import hashlib
# import datetime

SEP = os.sep

def file_path(pathname):
    if SEP == pathname[0:1]:
        return pathname
    else:
        pathname = pathname.replace('/',SEP)
        dir = os.path.dirname(__file__)
        new_path = os.path.join(dir, pathname)
        return new_path

in_field = ['seq','month_type','category','format','creation_method','note','slip_date','slip_number','slip_summary','branch_number','debit_department','debit_department_name','debit_account','debit_account_name','debit_subaccount','debit_subaccount_name','debit_amount','debit_tax_code','debit_tax_industry','debit_tax_rate','debit_fund_type','debit_optional_item_1','debit_optional_item_2','credit_department','credit_department_name','credit_account','credit_account_name','credit_subaccount','credit_subaccount_name','credit_amount','credit_tax_code','credit_tax_industry','credit_tax_rate','credit_fund_type','credit_optional_item_1','credit_optional_item_2','summary','due_date','voucher_number','input_machine','input_user','input_app','input_company','input_date']
in_field_ja = ['seq','月種別','種類','形式','作成方法','付箋','伝票日付','伝票番号','伝票摘要','枝番','借方部門','借方部門名','借方科目','借方科目名','借方補助','借方補助科目名'',''借方金額 ','借方消費税コード','借方消費税業種','借方消費税税率','借方資金区分','借方任意項目１','借方任意項目２','貸方部門','貸方部門名','貸方科目','貸方科目名','貸方補助','貸方補助科目名','貸方金額 ','貸方消費税コード','貸方消費税業種','貸方消費税税率','貸方資金区分','貸方任意項目１','貸方任意項目２','摘要','期日','証番号','入力マシン','入力ユーザ','入力アプリ','入力会社','入力日付']

out_field = ['JournalID','JournalNumber','FiscalYear','AccountingPeriod','EffectiveDate','JournalEntryHeaderDescription','SourceCode','JournalLineNumber','JournalEntryTypeCode','JournalEntryLineDescription','CreditDebitIndicator','GLAccountNumber','BillNumber','BillTypeCode','BillDate','Quantity','UOMCode','UnitPrice','SettlementMethodCode','ReversalIndicator','ReversalJournalID','CancellationSign','AccountSegmentEmployee','AccountSegmentProject','AccountSegmentBankAccount']
if __name__ == '__main__':
    # Create the parser
    parser = argparse.ArgumentParser(prog='mapping.py',
                                     usage='%(prog)s infile -o outfile -e encoding [options] ',
                                     description='Audit data collection CSVファイルをTidy data CSVに変換')
    # Add the arguments
    parser.add_argument('inFile', metavar='infile', type=str, help='Audit data collection 定義CSVファイル')
    parser.add_argument('-o', '--outfile')  # core.xsd
    parser.add_argument('-e', '--encoding') # 'Shift_JIS' 'cp932' 'utf_8'
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-d', '--debug', action='store_true')

    args = parser.parse_args()
    in_file = None
    if args.inFile:
        in_file = args.inFile.strip()
        in_file = in_file.replace('/', SEP)
        in_file = file_path(args.inFile)
    if not in_file or not os.path.isfile(in_file):
        print('入力ADC定義CSVファイルがありません')
        sys.exit()
    adc_file = in_file
    if args.outfile:
        out_file = args.outfile.lstrip()
        out_file = out_file.replace('/', SEP)
        out_file = file_path(out_file)
        xbrl_base = os.path.dirname(out_file)
    xbrl_base = xbrl_base.replace('/', SEP)
    if not os.path.isdir(xbrl_base):
        print('タクソノミのディレクトリがありません')
        sys.exit()

    ncdng = args.encoding
    if ncdng:
        ncdng = ncdng.lstrip()
    else:
        ncdng = 'UTF-8'
    VERBOSE = args.verbose
    DEBUG = args.debug

    records = []
    in_file = file_path(in_file)
    tidyData = []
    in_data = []
    accounting_data = []
    used_key = {}

    with open(in_file,mode='r', encoding='utf-8-sig', newline='') as file:
        # Create a CSV reader object
        csv_reader = csv.DictReader(file)
        # header = next(csv_reader)  # Read the first row as headers
        header = [col.strip() for col in csv_reader.fieldnames]  # strip whitespace from column headers
        for key in header:
            used_key[key] = False
        for row in csv_reader:
            row_dict = {}
            for i in range(1, len(header)):
                for key in row.keys():
                    stripped_key = key.strip()
                    if len(row[key]) > 0:
                        used_key[stripped_key] = True
                    row_dict[stripped_key] = row[key]
            in_data.append(row_dict)
    
    for row in in_data:
        row_dict = {}
        for key in row.keys():
            key = key.strip()
            if used_key[key]:
                row_dict[key] = row[key]
        accounting_data.append(row_dict)

    for data in accounting_data:
        # GL Header
        row = {}# [{key:''} for key,used in used_key.items() if used]
        row['GL02'] = data['seq']
        row['GL55'] = ''
        row['GL55-11'] = ''
        # GL02-01	JournalID	slip_number
        gl02_01 = data['slip_number']
        row['GL02-01'] = gl02_01
        # GL02-06	EffectiveDate	slip_date
        gl02_06 = data['slip_date']
        yy = gl02_06[:4]
        mm = gl02_06[4:6]
        dd = gl02_06[6:]
        row['GL02-06'] = f'{yy}-{mm}-{dd}'
        tidyData.append(row)

        # GL Details
        row = {}# [{key:''} for key,used in used_key.items() if used]
        row['GL02'] = data['seq']
        # GL55-01	JournalLineNumber	branch_number
        gl55_01 = data['branch_number']
        row['GL55'] = gl55_01
        row['GL55-11'] = ''
        # row['GL55-01'] = gl55_01
        # GL55-03	JournalEntryLineDescription	summary
        gl55_03 = data['summary']
        row['GL55-03'] = gl55_03
        # GL57-01	User ID	input_user
        gl57_01 = data['input_user']
        row['GL57-01'] = gl57_01
        # GL57-02	Date	input_date
        gl57_02 = data['input_date']
        yy = gl57_02[:4]
        mm = gl57_02[4:6]
        dd = gl57_02[6:]
        row['GL57-02'] = f'{yy}-{mm}-{dd}'
        tidyData.append(row)

        # debit
        row = {}
        row['GL02'] = data['seq']
        row['GL55'] = gl55_01
        # GL55-11	Credit Debit Indicator	debit
        gl55_11 = '借方'
        row['GL55-11'] = gl55_11
        # GL02-03	GL Account Number	debit_account
        gl02_03 = data['debit_account']
        row['GL02-03'] = gl02_03
        # GL04-03	GL Account Name	debit_account_name
        gl04_03 = data['debit_account_name']
        row['GL04-03'] = gl04_03
        # GL56-01	Functional Amount	debit_amount
        gl56_01 = data['debit_amount']
        row['GL56-01'] = gl56_01
        tidyData.append(row)

        # Account Segment
        row = {}
        row['GL02'] = data['seq']
        row['GL55'] = gl55_01
        # GL60-01	Account Segment Number	
        gl60_02 = data['debit_subaccount']
        if len(gl60_02) > 0:
            gl60_01 = '借方補助科目'
            row['GL60-01'] = gl60_01
            # GL60-02	Account Segment Code	debit_subaccount
            row['GL60-02'] = gl60_02
            tidyData.append(row)

        # Account Segment
        gl60_02 = data['debit_subaccount_name']
        if len(gl60_02) > 0:
            row = {}
            row['GL02'] = data['seq']
            row['GL55'] = gl55_01
            # GL60-01	Account Segment Number
            gl60_01 = '借方補助科目名'
            row['GL60-01'] = gl60_01
            # GL60-02	Account Segment Code	debit_subaccount_name
            row['GL60-02'] = gl60_02
            tidyData.append(row)

        # Account Segment '','','',''
        gl60_02 = data['debit_tax_code']
        if len(gl60_02) > 0:
            row = {}
            row['GL02'] = data['seq']
            row['GL55'] = gl55_01
            # GL60-01	Account Segment Number
            gl60_01 = '借方消費税コード'
            row['GL60-01'] = gl60_01
            # GL60-02	Account Segment Code	debit_tax_code
            row['GL60-02'] = gl60_02
            tidyData.append(row)

        # Account Segment
        gl60_02 = data['debit_tax_rate']
        if len(gl60_02) > 0:
            row = {}
            row['GL02'] = data['seq']
            row['GL55'] = gl55_01
            # GL60-01	Account Segment Number
            gl60_01 = '借方消費税税率'
            row['GL60-01'] = gl60_01
            # GL60-02	Account Segment Code	debit_tax_rate
            row['GL60-02'] = gl60_02
            tidyData.append(row)

        # Account Segment
        gl60_02 = data['debit_fund_type']
        if len(gl60_02) > 0:
            row = {}
            row['GL02'] = data['seq']
            row['GL55'] = gl55_01
            # GL60-01	Account Segment Number
            gl60_01 = '借方資金区分'
            row['GL60-01'] = gl60_01
            # GL60-02	Account Segment Code	debit_fund_type
            row['GL60-02'] = gl60_02
            tidyData.append(row)

        #credit
        row = {}
        row['GL02'] = data['seq']
        row['GL55'] = gl55_01
        # GL55-11	Credit Debit Indicator	credit
        gl55_11 = '貸方'
        row['GL55-11'] = gl55_11
        # GL02-03	GL Account Number	credit_account
        gl02_03 = data['credit_account']
        row['GL02-03'] = gl02_03
        # GL04-03	GL Account Name	credit_account_name
        gl04_03 = data['credit_account_name']
        row['GL04-03'] = gl04_03
        # GL56-01	Functional Amount	credit_amount
        gl56_01 = data['credit_amount']
        row['GL56-01'] = gl56_01
        tidyData.append(row)

        # Account Segment
        gl60_02 = data['credit_subaccount']
        if len(gl60_02) > 0:
            row = {}
            row['GL02'] = data['seq']
            row['GL55'] = gl55_01
            # GL60-01	Account Segment Number	
            gl60_01 = '貸方補助'
            row['GL60-01'] = gl60_01
            # GL60-02	Account Segment Code	credit_subaccount
            row['GL60-02'] = gl60_02
            tidyData.append(row)

        gl60_02 = data['credit_subaccount_name']
        if len(gl60_02) > 0:
            row = {}
            row['GL02'] = data['seq']
            row['GL55'] = gl55_01
            # GL60-01	Account Segment Number
            gl60_01 = '貸方補助科目名'
            row['GL60-01'] = gl60_01
            # GL60-02	Account Segment Code	credit_subaccount_name
            row['GL60-02'] = gl60_02
            tidyData.append(row)

        gl60_02 = data['credit_tax_code']
        if len(gl60_02) > 0:
            row = {}
            row['GL02'] = data['seq']
            row['GL55'] = gl55_01
            # GL60-01	Account Segment Number
            gl60_01 = '貸方消費税コード'
            row['GL60-01'] = gl60_01
            # GL60-02	Account Segment Code	credit_tax_code
            row['GL60-02'] = gl60_02
            tidyData.append(row)

        gl60_02 = data['credit_tax_rate']
        if len(gl60_02) > 0:
            row = {}
            row['GL02'] = data['seq']
            row['GL55'] = gl55_01
            # GL60-01	Account Segment Number
            gl60_01 = '貸方消費税税率'
            row['GL60-01'] = gl60_01
            # GL60-02	Account Segment Code	credit_tax_rate
            row['GL60-02'] = gl60_02
            tidyData.append(row)

        gl60_02 = data['credit_fund_type']
        if len(gl60_02) > 0:
            row = {}
            row['GL02'] = data['seq']
            row['GL55'] = gl55_01
            # GL60-01	Account Segment Number
            gl60_01 = '貸方資金区分'
            row['GL60-01'] = gl60_01
            # GL60-02	Account Segment Code	credit_fund_type
            row['GL60-02'] = gl60_02
            tidyData.append(row)

    with open(out_file, mode='w', encoding='utf-8-sig', newline='') as file:
        fieldnames = tidyData[0].keys()  # get the column headers from the first row
        fieldnames = set().union(*tidyData)  # get a set of all keys in all rows
        # sorted_fieldnames = sorted(fieldnames, key=lambda k: tidyData[0].get(k, '') if tidyData else '')  # sort the fieldnames by their value in the first row, or by an empty string if data is empty
        sorted_fieldnames = sorted(fieldnames, key=lambda k: (tidyData[0].get(k, ''), k) if tidyData else '')  # sort the fieldnames by their value in the first row, or by an empty string if data is empty
        if 'GL02-06' in sorted_fieldnames:
            sorted_fieldnames.remove('GL02-06')  # remove GL02-06 from the list of sorted fieldnames
            sorted_fieldnames.insert(0, 'GL02-06')  # add GL02-06 back at the beginning of the list
        if 'GL02-01' in sorted_fieldnames:
            sorted_fieldnames.remove('GL02-01')  # remove GL02-01 from the list of sorted fieldnames
            sorted_fieldnames.insert(0, 'GL02-01')  # add GL02-01 back at the beginning of the list
        if 'GL60-01' in sorted_fieldnames:
            sorted_fieldnames.remove('GL60-01')  # remove GL60-01 from the list of sorted fieldnames
            sorted_fieldnames.insert(0, 'GL60-01')  # add GL60-01 back at the beginning of the list
        if 'GL55-11' in sorted_fieldnames:
            sorted_fieldnames.remove('GL55-11')  # remove GL55-11 from the list of sorted fieldnames
            sorted_fieldnames.insert(0, 'GL55-11')  # add GL55-11 back at the beginning of the list
        if 'GL55' in sorted_fieldnames:
            sorted_fieldnames.remove('GL55')  # remove GL55 from the list of sorted fieldnames
            sorted_fieldnames.insert(0, 'GL55')  # add GL55 back at the beginning of the list
        if 'GL02' in sorted_fieldnames:
            sorted_fieldnames.remove('GL02')  # remove GL02 from the list of sorted fieldnames
            sorted_fieldnames.insert(0, 'GL02')  # add GL02 back at the beginning of the list
        writer = csv.DictWriter(file, fieldnames=sorted_fieldnames)
        writer.writeheader()  # write the column headers to the file
        for row in tidyData:
            writer.writerow(row)  # write each row to the file

    print('END')