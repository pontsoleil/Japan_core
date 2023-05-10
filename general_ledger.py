#!/usr/bin/env python3
# coding: utf-8
#
# generate general ledger CSV from horizontal ledger CSV
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

import csv
import os

DEBUG = False

lines       = []
postedMonth = None
monthDebit  = 0
monthCredit = 0
totalDebit  = 0
totalCredit = 0
netAmount   = 0

horizontalDict = {
    'GL00': 'num',
    'GL02': 'GL',
    'GL02-GL55': 'GL詳細',
    'GL55-GL60d': '借方勘定科目セグメント',
    'GL55-GL60c': '貸方勘定科目セグメント',
    'GL55-GL61': '事業セグメント',

    'GL02-01': '仕訳ID',
    'GL64-01': 'ソースコード',
    'GL64-02': 'ソース説明',
    'GL64-03': 'ERPサブレジャーモジュール',
    'GL64-04': 'システムマニュアル識別子',
    'GL57-01': '作成者ユーザーID',
    'GL57-02': '作成日',
    'GL55-03': '仕訳エントリタイプコード',
    'GL55-04': '仕訳エントリ行説明',

    'GL69-02': '記帳日',
    'GL56-02': '通貨コード',

    'GL63-01d': '借方勘定科目番号',
    'GL63-02d': '借方勘定科目名',
    'GL63-03d': '借方財務諸表キャプション',

    'GL56-01d': '借方金額',

    'GL60-01d': '借方勘定科目セグメント番号',
    'GL60-02d': '借方勘定科目セグメントコード',
    'GL60-03d': '借方勘定科目セグメント名',

    'GL63-01c': '貸方勘定科目番号',
    'GL63-02c': '貸方勘定科目名',
    'GL63-03c': '貸方財務諸表キャプション',

    'GL56-01c': '貸方金額',

    'GL60-01c': '貸方勘定科目セグメント番号',
    'GL60-02c': '貸方勘定科目セグメントコード',
    'GL60-03c': '貸方勘定科目セグメント名',

    'GL61-01': '事業セグメント順序番号',
    'GL61-02': '事業セグメントコード',
    'GL61-03': '組織タイプ名'
}

generalDict = {
    '検索ＮＯ','伝票ＮＯ','伝票日付','相手科目コード','相手科目名称','摘要','消費税コード','消費税率','借方金額','貸方金額','差引金額'}

glDict = {
    'GL00': 'num',
    'GL02': 'GL',
    'GL02-GL55': 'GL詳細',

    'GL02-01': '仕訳ID',
    'GL55-04': '仕訳エントリ行説明',
    'GL69-02': '記帳日',

    'GL63-01': '勘定科目番号',
    'GL63-02': '勘定科目名',
    'GL63-01cn': '相手勘定科目番号',
    'GL63-02cn': '相手勘定科目名',

    'GL56-01d': '借方金額',
    'GL56-01c': '貸方金額',
    'GL56-01net': '差引金額'
}

outDict = {
    'GL00': 'num',

    'GL63-01': '勘定科目番号',
    'GL63-02': '勘定科目名',

    'GL02': 'GL',
    'GL02-GL55': 'GL詳細',

    'GL55-04': '仕訳エントリ行説明',
    'GL69-02': '記帳日',

    'GL63-01cn': '相手勘定科目番号',
    'GL63-02cn': '相手勘定科目名',

    'GL56-01d': '借方金額',
    'GL56-01c': '貸方金額',
    'GL56-01net': '差引金額'    
}

header = ['GL02','GL02-GL55','GL55-04','GL69-02','GL63-01cn','GL63-02cn','GL56-01d','GL56-01c','GL56-01net']

def record_entry(accountNumber,entry):
    global lines
    global postedMonth
    global monthDebit
    global monthCredit
    global totalDebit
    global totalCredit
    global netAmount
    postedMonth  = entry['GL69-02'][:7]
    debitAmount  = ''!=entry['GL56-01d'] and entry['GL56-01d'] or 0
    creditAmount = ''!=entry['GL56-01c'] and entry['GL56-01c'] or 0
    monthDebit  += debitAmount
    monthCredit += creditAmount
    totalDebit  += debitAmount
    totalCredit += creditAmount
    netAmount   += debitAmount - creditAmount
    line = {}
    line['GL02']      = entry['GL02']
    line['GL02-GL55'] = entry['GL02-GL55']
    line['GL55-04']   = entry['GL55-04']
    line['GL69-02']   = entry['GL69-02']
    line['GL63-01cn'] = entry['GL63-01cn']
    line['GL63-02cn'] = entry['GL63-02cn']
    line['GL56-01d']  = entry['GL56-01d']
    line['GL56-01c']  = entry['GL56-01c']
    line['GL56-01net']= netAmount
    lines[accountNumber].append(line)
    return line

def main():
    in_file = 'data/journal_entry/horizontal_ledger.csv'

    global lines
    global postedMonth
    global monthDebit
    global monthCredit
    global totalDebit
    global totalCredit
    global netAmount

    with open(in_file, 'r', encoding='utf-8-sig') as f:
        horizontal_header = list(horizontalDict.keys())
        reader = csv.DictReader(f, fieldnames=horizontal_header)
        next(reader)
        records = []
        for row in reader:
            if ''==row['GL02-GL55'] or ''!=row['GL55-GL60d']or ''!=row['GL55-GL60c']or ''!=row['GL55-GL61']:
                continue
            records.append(row)

    accounts = {}
    for row in records:
        account_code = row['GL63-01d']
        account_name = row['GL63-02d']
        if ''!=account_code:
            accounts[account_code] = account_name
        account_code = row['GL63-01c']
        account_name = row['GL63-02c']
        if ''!=account_code:
            accounts[account_code] = account_name
    accounts = {k: accounts[k] for k in sorted(accounts)}

    # 2. 総勘定元帳を初期化する
    general_ledger = {}
    # journal_entry = []
    for i in range(len(records)):
        row = records[i]
        if len(row['GL02-GL55'])>0:
            num = row['GL00']
            GL02 = row['GL02']
            GL02_GL55 = row['GL02-GL55']
            debit_account = row['GL63-01d']
            credit_account = row['GL63-01c']
            debit_account_name = row['GL63-02d']
            credit_account_name = row['GL63-02c']
            debit_amount = row['GL56-01d'].isdigit() and int(row['GL56-01d']) or 0
            credit_amount = row['GL56-01c'].isdigit() and int(row['GL56-01c']) or 0
            date = row['GL69-02']
            note = row['GL55-04']
            # 借方勘定ごとに総勘定元帳を更新する
            if debit_account in general_ledger:
                general_ledger[debit_account]['debit'] += debit_amount
                general_ledger[debit_account]['balance'] += debit_amount
            else:
                general_ledger[debit_account] = {'account_name': debit_account_name, 'debit': debit_amount, 'credit': 0, 'balance': debit_amount}
            # 貸方勘定ごとに総勘定元帳を更新する
            if credit_account in general_ledger:
                general_ledger[credit_account]['credit'] += credit_amount
                general_ledger[credit_account]['balance'] -= credit_amount
            else:
                general_ledger[credit_account] = {'account_name': credit_account_name, 'debit': 0, 'credit': credit_amount, 'balance': -credit_amount}
            # 取引データを総勘定元帳に追加する
            if 'transactions' not in general_ledger[debit_account]:
                general_ledger[debit_account]['transactions'] = []
            debit_transaction_data = {'num': num, 'GL02':GL02, 'GL02-GL55':GL02_GL55,
                                'date': date, 'contra_account': credit_account, 'contra_account_name': credit_account_name,
                                'debit_amount': debit_amount, 'credit_amount': 0, 'balance': general_ledger[debit_account]["balance"], 'note': note}
            general_ledger[debit_account]['transactions'].append(debit_transaction_data)
            if 'transactions' not in general_ledger[credit_account]:
                general_ledger[credit_account]['transactions'] = []
            credit_transaction_data = {'num': num, 'GL02':GL02, 'GL02-GL55':GL02_GL55,
                                'date': date, 'contra_account': debit_account, 'contra_account_name': debit_account_name,
                                'debit_amount': 0, 'credit_amount': credit_amount, 'balance': general_ledger[credit_account]["balance"], 'note': note}
            general_ledger[credit_account]['transactions'].append(credit_transaction_data)

    # 4. 総勘定元帳を勘定コード順にソートする
    sorted_general_ledger = sorted(general_ledger.items(), key=lambda x: x[0])

    # 5. 総勘定元帳を出力する
    for account_code, account_data in sorted_general_ledger:
        account_name = account_data['account_name']
        debit_amount = account_data['debit']
        credit_amount = account_data['credit']
        balance = account_data['balance']
        if DEBUG: print(f'Account Code: {account_code} ({account_name})')
        record = {
            'num': '',
            'GL02': '',
            'GL02-GL55': '',
            'date': '',
            'contra_account': account_code,
            'contra_account_name': account_name,
            'debit_amount': debit_amount,
            'credit_amount': credit_amount,
            'balance':balance,
            'note': ''
        }
        if 'record' not in general_ledger[account_code]:
            general_ledger[account_code]['record'] = []
        general_ledger[account_code]['record'].append(record)
        # transaction data
        debit_total = credit_total = 0
        month = None
        for transaction_data in account_data.get('transactions', []):
            if month and month!=transaction_data['date'][:7]:
                record = {
                    'num': '',
                    'GL02': '',
                    'GL02-GL55': '',
                    'date': month,
                    'contra_account': '',
                    'contra_account_name': '※※月計※※',
                    'debit_amount': debit_total,
                    'credit_amount': credit_total,
                    'balance':'',
                    'note': ''
                }
                general_ledger[account_code]['record'].append(record)
                if 'TB' not in general_ledger:
                    general_ledger['TB'] = {}
                if month not in general_ledger['TB']:
                    general_ledger['TB'][month] = {}
                general_ledger['TB'][month][account_code] = {
                    'month': month,
                    'account_code': account_code,
                    'debit_amount': debit_total,
                    'credit_amount': credit_total,
                    'balance':balance
                }
                debit_total = credit_total = 0
            num = transaction_data['num']
            GL02 = transaction_data['GL02']
            GL02_GL55 = transaction_data['GL02-GL55']
            date = transaction_data['date']
            month = date[:7]
            contra_account = transaction_data['contra_account']
            contra_account_name = transaction_data['contra_account_name']
            debit_amount = transaction_data['debit_amount']
            debit_total += debit_amount
            credit_amount = transaction_data['credit_amount']
            credit_total += credit_amount
            balance = transaction_data['balance']
            note = transaction_data['note']
            if DEBUG: print(f'{num} {GL02} {GL02_GL55} {date} {contra_account} {contra_account_name} {debit_amount} {credit_amount} {balance} {note}')
            record = {
                'num': num,
                'GL02': GL02,
                'GL02-GL55': GL02_GL55,
                'date': date,
                'contra_account': contra_account,
                'contra_account_name': contra_account_name,
                'note': note,
                'debit_amount': debit_amount,
                'credit_amount': credit_amount,
                'balance':balance
            }
            if 'record' not in general_ledger[account_code]:
                general_ledger[account_code]['record'] = []
            general_ledger[account_code]['record'].append(record)
        record = {
            'num': '',
            'GL02': '',
            'GL02-GL55': '',
            'date': month,
            'contra_account': '',
            'contra_account_name': '※※月計※※',
            'note': note,
            'debit_amount': debit_total,
            'credit_amount': credit_total,
            'balance':balance
        }
        general_ledger[account_code]['record'].append(record)

        dir_path = 'data/journal_entry/GL'
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        with open(f'{dir_path}/{account_code}{account_name}.csv', 'w', newline='', encoding='utf-8-sig') as file:
            header = list(record.keys())
            writer = csv.DictWriter(file, fieldnames=header)
            writer.writeheader()
            for row in general_ledger[account_code]['record']:
                writer.writerow(row)

    dir_path = 'data/journal_entry'
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    with open(f'{dir_path}/general_ledger.csv', 'w', newline='', encoding='utf-8-sig') as file:
        header = list(record.keys())
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        for row in general_ledger[account_code]['record']:
            writer.writerow(row)

    # 試算表
    beginning_balance = {}
    for account_code in accounts.keys():
        beginning_balance[account_code] = [0]*13

    monthly_balance = {}
    debit_month_total = {}
    credit_month_total = {}
    m = 0
    for month in general_ledger['TB']:
        m += 1
        for account_code in general_ledger['TB'][month]:
            record = general_ledger['TB'][month][account_code]
            if account_code not in debit_month_total:
                debit_month_total[account_code] = 0
            debit_month_total[account_code]  += record['debit_amount']
            if account_code not in credit_month_total:
                credit_month_total[account_code] = 0
            credit_month_total[account_code] += record['credit_amount']
            beginning_balance[account_code][m] = beginning_balance[account_code][m-1] + record['balance']
            if m not in monthly_balance:
                monthly_balance[m] = {}
            monthly_balance[m][account_code] = {
                'month':month,
                'account_code':account_code,
                'account_name':accounts[account_code],
                'beginning_balance':beginning_balance[account_code][m-1],
                'debit_amount':debit_month_total[account_code],
                'credit_amount':credit_month_total[account_code],
                'ending_balance':beginning_balance[account_code][m]
            }
            print(f"{monthly_balance[m][account_code]['month']} | {monthly_balance[m][account_code]['account_code']}:{ monthly_balance[m][account_code]['account_name']} | {monthly_balance[m][account_code]['beginning_balance']} | {monthly_balance[m][account_code]['debit_amount']} | {monthly_balance[m][account_code]['credit_amount']} | {monthly_balance[m][account_code]['ending_balance']}")
        monthly_balance[m][''] = {
            'month':'',
            'account_code':'',
            'account_name':'',
            'beginning_balance':'',
            'debit_amount':sum(debit_month_total.values()),
            'credit_amount':sum(credit_month_total.values()),
            'ending_balance':''
        }
        # records.append(monthly_balance[m][''])
        print(f"{monthly_balance[m]['']['month']} | {monthly_balance[m]['']['account_code']}:{ monthly_balance[m]['']['account_name']} | {monthly_balance[m]['']['beginning_balance']} | {monthly_balance[m]['']['debit_amount']} | {monthly_balance[m]['']['credit_amount']} | {monthly_balance[m]['']['ending_balance']}")

        dir_path = f'data/journal_entry/TB/{month}'
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        with open(f'{dir_path}/trial_balance.csv', 'w', newline='', encoding='utf-8-sig') as file:
            header = list(monthly_balance[m][''].keys())
            writer = csv.DictWriter(file, fieldnames=header)
            writer.writeheader()
            for row in list(monthly_balance[m].values()):
                writer.writerow(row)

    print('END')

if __name__ == '__main__':
    main()
