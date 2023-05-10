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

def print_entry(msg,journal_entry):
    print(f"{msg} {journal_entry['GL00']} | {journal_entry['GL02-GL55']} | {journal_entry['GL55-04']} | {journal_entry['GL63-02d'] or '-'} JPY {journal_entry['GL56-01d'] or '-'} | {journal_entry['GL60-01d'] or '-'}:{journal_entry['GL60-03d'] or '-'} | {journal_entry['GL63-02c'] or '-'} JPY {journal_entry['GL56-01c'] or '-'} | {journal_entry['GL60-01c'] or '-'}:{journal_entry['GL60-03c'] or '-'}")

def main():
    in_file = 'data/journal_entry/horizontal_ledger.csv'

    global lines
    global postedMonth
    global monthDebit
    global monthCredit
    global totalDebit
    global totalCredit
    global netAmount

    # 1. 仕訳データを読み込む
    horizontal_header = list(horizontalDict.keys())
    with open(in_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, fieldnames=horizontal_header)
        next(reader)
        journal_data = []
        for row in reader:
            journal_data.append(row)

    # 2. 総勘定元帳を初期化する
    general_ledger = {}

    # 3. 仕訳データを処理して、総勘定元帳を更新する
    for entry in journal_data:
        if ''==entry['GL02-GL55'] or ''!=entry['GL55-GL60d'] or ''!=entry['GL55-GL60c'] or ''!=entry['GL55-GL61']:
            continue
        # 借方科目、貸方科目、借方金額、貸方金額、日付、摘要を取得する
        if ''==entry['GL56-01d'] or ''==entry['GL56-01c']:
            print_entry('金額ゼロ',entry)
            continue 
        debit_account = entry['GL63-01d']
        credit_account = entry['GL63-01c']
        debit_account_name = entry['GL63-02d']
        credit_account_name = entry['GL63-02c']
        debit_amount = int(entry['GL56-01d'])
        credit_amount = int(entry['GL56-01c'])
        date = entry['GL69-02']
        note = entry['GL55-04']

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
        transaction_data = {'date': date, 'debit_account': debit_account, 'debit_amount': debit_amount,
                            'credit_account': credit_account, 'credit_amount': credit_amount, 'note': note}
        if 'transactions' not in general_ledger[debit_account]:
            general_ledger[debit_account]['transactions'] = []
        general_ledger[debit_account]['transactions'].append(transaction_data)
        if 'transactions' not in general_ledger[credit_account]:
            general_ledger[credit_account]['transactions'] = []
        general_ledger[credit_account]['transactions'].append(transaction_data)

    # 4. 総勘定元帳を勘定コード順にソートする
    sorted_general_ledger = sorted(general_ledger.items(), key=lambda x: x[0])

    # 5. 総勘定元帳を出力する
    for account_code, account_data in sorted_general_ledger:
        account_name = account_data['account_name']
        debit_amount = account_data['debit']
        credit_amount = account_data['credit']
        balance = account_data['balance']
        print(f'Account Code: {account_code} ({account_name})')
        for transaction_data in account_data.get('transactions', []):
            date = transaction_data['date']
            debit_account = transaction_data['debit_account']
            debit_amount = transaction_data['debit_amount']
            credit_account = transaction_data['credit_account']
            credit_amount = transaction_data['credit_amount']
            note = transaction_data['credit_amount']
            print(f'{date} {debit_account}')

    print('END')

if __name__ == '__main__':
    main()
