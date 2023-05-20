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

# horizontalDict2 = {
#     'GL00': 'num',
#     'GL02': 'GL',
#     'GL02-GL55': 'GL詳細',
#     'GL55-GL60d': '借方勘定科目セグメント',
#     'GL55-GL60c': '貸方勘定科目セグメント',
#     'GL55-GL61': '事業セグメント',

#     'GL02-01': '仕訳ID',
#     'GL64-01': 'ソースコード',
#     'GL64-02': 'ソース説明',
#     'GL64-03': 'ERPサブレジャーモジュール',
#     'GL64-04': 'システムマニュアル識別子',
#     'GL57-01': '作成者ユーザーID',
#     'GL57-02': '作成日',
#     'GL55-03': '仕訳エントリタイプコード',
#     'GL55-04': '仕訳エントリ行説明',

#     'GL69-02': '記帳日',
#     'GL56-02': '通貨コード',

#     'GL63-01d': '借方勘定科目番号',
#     'GL63-02d': '借方勘定科目名',
#     'GL63-03d': '借方財務諸表キャプション',

#     'GL56-01d': '借方金額',

#     'GL60-01d': '借方勘定科目セグメント番号',
#     'GL60-02d': '借方勘定科目セグメントコード',
#     'GL60-03d': '借方勘定科目セグメント名',

#     'GL63-01c': '貸方勘定科目番号',
#     'GL63-02c': '貸方勘定科目名',
#     'GL63-03c': '貸方財務諸表キャプション',

#     'GL56-01c': '貸方金額',

#     'GL60-01c': '貸方勘定科目セグメント番号',
#     'GL60-02c': '貸方勘定科目セグメントコード',
#     'GL60-03c': '貸方勘定科目セグメント名',

#     'GL61-01': '事業セグメント順序番号',
#     'GL61-02': '事業セグメントコード',
#     'GL61-03': '組織タイプ名'
# }

horizontalDict = {
    'GL00':      'num',
    'GL02':      'GL',
    'GL02-GL55': 'GL詳細',
    'GL55-GL68d': '借方税情報',
    'GL55-GL68c': '貸方税情報',
    'GL55-GL60d': '借方勘定科目セグメント',
    'GL55-GL60c': '貸方勘定科目セグメント',
    'GL55-GL61': '事業セグメント',

    'GL02-01': '仕訳ID',
    'GL02-02': '仕訳ID', #
    'GL02-03': '文書コメント', #

    'GL64-01': 'ソースコード',
    'GL64-02': 'ソース説明',
    'GL64-03': 'ERPサブレジャーモジュール',
    'GL64-04': 'システムマニュアル識別子',

    'GL57-01': '作成者ユーザーID',
    'GL57-02': '作成日',

    'GL55-01': '明細行番号', #
    'GL55-02': '転記日付', #
    'GL55-03': '仕訳エントリタイプコード',
    'GL55-04':  '仕訳エントリ行説明',
    'GL55-06': '元文書番号', #
    'GL55-08': '元文書日付', #

    'GL69-02':  '記帳日',

    'GL56-02':  '通貨コード',

    'GL63-01d': '借方勘定科目番号',
    'GL63-02d': '借方勘定科目名',
    'GL63-03d': '借方財務諸表キャプション',
    'GL56-01d': '借方金額',
    'GL56-02d': '借方金額コード',

    'GL68-01d': '借方税コード', #
    'GL68-02d': '借方税パーセント', #
    'GL68-04d': '借方税コード説明', #
    
    'GL60-01d': '借方勘定科目セグメント番号',
    'GL60-02d': '借方勘定科目セグメントコード',
    'GL60-03d': '借方勘定科目セグメント名',

    'GL63-01c': '貸方勘定科目番号',
    'GL63-02c': '貸方勘定科目名',
    'GL63-03c': '貸方財務諸表キャプション',
    'GL56-01c': '貸方金額',
    'GL56-02c': '貸方金額コード',

    'GL68-01c': '貸方税コード', #
    'GL68-02c': '貸方税パーセント', #
    'GL68-04c': '貸方税コード説明', #
    
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
    party = '北海道産業(株)'
    in_file = f'data/journal_entry/{party}/horizontal_ledger.csv'

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
    for i in range(len(records)):
        row = records[i]
        if len(row['GL02-GL55'])>0:
            num              = row['GL00']
            GL02             = row['GL02']
            GL02_GL55        = row['GL02-GL55']
            dbt_account      = row['GL63-01d']
            cdt_account      = row['GL63-01c']
            dbt_account_name = row['GL63-02d']
            cdt_account_name = row['GL63-02c']
            dbt_amount       = row['GL56-01d'].isdigit() and int(row['GL56-01d']) or 0
            cdt_amount       = row['GL56-01c'].isdigit() and int(row['GL56-01c']) or 0
            dbt_tax_code     = row['GL68-01d']
            cdt_tax_code     = row['GL68-01c']
            dbt_tax_rate     = row['GL68-02d']
            cdt_tax_rate     = row['GL68-02c']
            dbt_tax_desc     = row['GL68-04d']
            cdt_tax_desc     = row['GL68-04c']
            date             = row['GL69-02']
            note             = row['GL55-04']
            # 借方勘定ごとに総勘定元帳を更新する
            if dbt_account in general_ledger:
                general_ledger[dbt_account]['dbt']     += dbt_amount
                general_ledger[dbt_account]['balance'] += dbt_amount
            else:
                general_ledger[dbt_account] = {'account_name': dbt_account_name, 'dbt': dbt_amount, 'cdt': 0, 'balance': dbt_amount}
            # 貸方勘定ごとに総勘定元帳を更新する
            if cdt_account in general_ledger:
                general_ledger[cdt_account]['cdt']     += cdt_amount
                general_ledger[cdt_account]['balance'] -= cdt_amount
            else:
                general_ledger[cdt_account] = {'account_name': cdt_account_name, 'dbt': 0, 'cdt': cdt_amount, 'balance': -cdt_amount}
            # 取引データを総勘定元帳に追加する
            if 'transactions' not in general_ledger[dbt_account]:
                general_ledger[dbt_account]['transactions'] = []
            debit_transaction_data = {'num': num, 'GL02':GL02, 'GL02-GL55':GL02_GL55,
                                'date': date, 'contra_acct': cdt_account, 'contra_acct_name': cdt_account_name,
                                'dbt_amount': dbt_amount, 'cdt_amount': 0, 'balance': general_ledger[dbt_account]["balance"],
                                'dbt_tax_code': dbt_tax_code, 'dbt_tax_rate': dbt_tax_rate, 'dbt_tax_desc': dbt_tax_desc,
                                'cdt_tax_code': '', 'cdt_tax_rate': '', 'cdt_tax_desc': '',
                                'note': note}
            general_ledger[dbt_account]['transactions'].append(debit_transaction_data)
            if 'transactions' not in general_ledger[cdt_account]:
                general_ledger[cdt_account]['transactions'] = []
            credit_transaction_data = {'num': num, 'GL02':GL02, 'GL02-GL55':GL02_GL55,
                                'date': date, 'contra_acct': dbt_account, 'contra_acct_name': dbt_account_name,
                                'dbt_amount': 0, 'cdt_amount': cdt_amount, 'balance': general_ledger[cdt_account]["balance"],
                                'dbt_tax_code': '', 'dbt_tax_rate': '', 'dbt_tax_desc': '',
                                'cdt_tax_code': cdt_tax_code, 'cdt_tax_rate': cdt_tax_rate, 'cdt_tax_desc': cdt_tax_desc,
                                'note': note}
            general_ledger[cdt_account]['transactions'].append(credit_transaction_data)

    # 4. 総勘定元帳を勘定コード順にソートする
    sorted_general_ledger = sorted(general_ledger.items(), key=lambda x: x[0])

    # 検算
    account_totals  = {}
    dbt_total = cdt_total = 0
    current_month = None
    for account_code, account_data in sorted_general_ledger:
        transactions = account_data['transactions']
        last = {'num': 'END', 'GL02':'', 'GL02-GL55':'','date': '', 'contra_acct': '', 'contra_acct_name': '',
                'dbt_amount': '', 'cdt_amount': '', 'balance': '',
                'dbt_tax_code': '', 'dbt_tax_rate': '', 'dbt_tax_desc': '',
                'cdt_tax_code': '', 'cdt_tax_rate': '', 'cdt_tax_desc': '',
                'note': ''}
        transactions.append(last)
        for transaction_data in transactions:
            date = transaction_data['date']
            if ''!=date:
                month = date[:7]
            if (current_month and current_month!=month) or (''==date):
                if current_month not in account_totals:
                    account_totals[current_month] = {}
                if account_code not in account_totals[current_month]:
                    account_totals[current_month][account_code] = {}
                account_totals[current_month][account_code]['dbt'] = dbt_total
                account_totals[current_month][account_code]['cdt'] = cdt_total
                dbt_total = cdt_total = 0
            if ''!=date:
                dbt_total += transaction_data['dbt_amount']
                cdt_total += transaction_data['cdt_amount']
                current_month = month

    monthly_totals = {}
    for month,total_data in account_totals.items():
        if month not in monthly_totals:
            monthly_totals[month] = {}
            monthly_totals[month]['dbt'] = 0
            monthly_totals[month]['cdt'] = 0
        for account_code,total in total_data.items():
            monthly_totals[month]['dbt'] += total['dbt']
            monthly_totals[month]['cdt'] += total['cdt']
    # 検算
    for month in monthly_totals:
        _dbt_total = monthly_totals[month]['dbt']
        _cdt_total = monthly_totals[month]['cdt']
        if DEBUG: print(f'{month} 借方 {_dbt_total} 貸方 {_cdt_total} {_dbt_total - _cdt_total}')

    # 5. 総勘定元帳を出力する    
    for account_code, account_data in sorted_general_ledger:
        account_name = account_data['account_name']
        dbt_amount   = account_data['dbt']
        cdt_amount   = account_data['cdt']
        balance      = account_data['balance']
        # dbt_tax_code = account_data['dbt_tax_code']
        # dbt_tax_rate = account_data['dbt_tax_rate']
        # dbt_tax_desc = account_data['dbt_tax_desc']
        # cdt_tax_code = account_data['cdt_tax_code']
        # cdt_tax_rate = account_data['cdt_tax_rate']
        # cdt_tax_desc = account_data['cdt_tax_desc']
        if DEBUG: print(f'Account Code: {account_code}:{account_name} Dr {"{:,}".format(dbt_amount)} Cr {"{:,}".format(cdt_amount)}')
        record = {
            'num':              '',
            'GL02':             '',
            'GL02-GL55':        '',
            'date':             '',
            'contra_acct':      account_code,
            'contra_acct_name': account_name,
            'dbt_amount':       dbt_amount,
            'cdt_amount':       cdt_amount,
            'balance':          balance,
            # 'dbt_tax_code':     dbt_tax_code,
            # 'dbt_tax_rate':     dbt_tax_rate,
            # 'dbt_tax_desc':     dbt_tax_desc,
            # 'cdt_tax_code':     cdt_tax_code,
            # 'cdt_tax_rate':     cdt_tax_rate,
            # 'cdt_tax_desc':     cdt_tax_desc,
            'note':             ''
        }
        if 'record' not in general_ledger[account_code]:
            general_ledger[account_code]['record'] = []
        general_ledger[account_code]['record'].append(record)
        # transaction data
        dbt_total = cdt_total = 0
        month = None
        transactions = account_data['transactions']
        for transaction_data in transactions:
            if 'END'==transaction_data['num']:
                continue
            if month and month!=transaction_data['date'][:7]:
                record = {
                    'num':              '',
                    'GL02':             '',
                    'GL02-GL55':        '',
                    'date':             month,
                    'contra_acct':      '',
                    'contra_acct_name': '※※月計※※',
                    'dbt_amount':       dbt_total,
                    'cdt_amount':       cdt_total,
                    'balance':          '',
                    # 'dbt_tax_code':     '',
                    # 'dbt_tax_rate':     '',
                    # 'dbt_tax_desc':     '',
                    # 'cdt_tax_code':     '',
                    # 'cdt_tax_rate':     '',                    
                    'note':             ''
                }
                general_ledger[account_code]['record'].append(record)
                if DEBUG: print(f'{month} {account_code}:{account_name} Dr {"{:,}".format(dbt_amount)} Cr {"{:,}".format(cdt_amount)}')
                dbt_total = cdt_total = 0
            num              = transaction_data['num']
            GL02             = transaction_data['GL02']
            GL02_GL55        = transaction_data['GL02-GL55']
            date             = transaction_data['date']
            contra_acct      = transaction_data['contra_acct']
            contra_acct_name = transaction_data['contra_acct_name']
            dbt_amount       = transaction_data['dbt_amount']
            cdt_amount       = transaction_data['cdt_amount']
            balance          = transaction_data['balance']
            # dbt_tax_code     = transaction_data['dbt_tax_code']
            # dbt_tax_rate     = transaction_data['dbt_tax_rate']
            # dbt_tax_desc     = transaction_data['dbt_tax_desc']
            # cdt_tax_code     = transaction_data['cdt_tax_code']
            # cdt_tax_rate     = transaction_data['cdt_tax_rate']
            # cdt_tax_desc     = transaction_data['cdt_tax_desc']
            note             = transaction_data['note']
            month            = date[:7]
            dbt_total       += dbt_amount
            cdt_total       += cdt_amount
            if DEBUG: print(f'{num} {GL02} {GL02_GL55} {date} {contra_acct} {contra_acct_name} {dbt_amount} {cdt_amount} {balance} {note}')
            record = {
                'num':              num,
                'GL02':             GL02,
                'GL02-GL55':        GL02_GL55,
                'date':             date,
                'contra_acct':      contra_acct,
                'contra_acct_name': contra_acct_name,
                'note':             note,
                'dbt_amount':       dbt_amount,
                'cdt_amount':       cdt_amount,
                'balance':          balance
                # 'dbt_tax_code':     dbt_tax_code,
                # 'dbt_tax_rate':     dbt_tax_rate,
                # 'dbt_tax_desc':     dbt_tax_desc,
                # 'cdt_tax_code':     cdt_tax_code,
                # 'cdt_tax_rate':     cdt_tax_rate,
                # 'cdt_tax_desc':     cdt_tax_desc
            }
            if 'record' not in general_ledger[account_code]:
                general_ledger[account_code]['record'] = []
            general_ledger[account_code]['record'].append(record)
        # 最終レコードの処理
        record = {
            'num':              '',
            'GL02':             '',
            'GL02-GL55':        '',
            'date':             month,
            'contra_acct':      '',
            'contra_acct_name': '※※月計※※',
            'note':             '',
            'dbt_amount':       dbt_total,
            'cdt_amount':       cdt_total,
            'balance':          balance,
            'dbt_tax_code':     '',
            'dbt_tax_rate':     '',
            'dbt_tax_desc':     '',
            'cdt_tax_code':     '',
            'cdt_tax_rate':     '',
            'cdt_tax_desc':     ''
        }
        general_ledger[account_code]['record'].append(record)

        dir_path = f'data/journal_entry/{party}/GL'
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        with open(f'{dir_path}/{account_code}{account_name}.csv', 'w', newline='', encoding='utf-8-sig') as file:
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
    m= 0
    for month,total_data in account_totals.items():
        m += 1
        if month not in monthly_balance:
            monthly_balance[month] = {}
        dbt_total = 0
        cdt_total = 0
        for account_code,account_total in total_data.items():
            beginning_balance[account_code][m] = beginning_balance[account_code][m-1] + account_total['dbt'] - account_total['cdt']
            monthly_balance[month][account_code] = {
                'month':             month,
                'account_code':      account_code,
                'account_name':      accounts[account_code],
                'beginning_balance': beginning_balance[account_code][m-1],
                'dbt_amount':        account_total['dbt'],
                'cdt_amount':        account_total['cdt'],
                'ending_balance':    beginning_balance[account_code][m]
            }
            dbt_total += account_total['dbt']
            cdt_total += account_total['cdt']
        if dbt_total!= monthly_totals[month]['dbt'] or cdt_total!=monthly_totals[month]['cdt']:
            print (f"計算エラー {dbt_total}:{monthly_totals[month]['dbt']}  {cdt_total}:{monthly_totals[month]['cdt']}")
        monthly_balance[month][''] = {
                'month':             month,
                'account_code':      '',
                'account_name':      '',
                'beginning_balance': '',
                'dbt_amount':        dbt_total,
                'cdt_amount':        cdt_total,
                'ending_balance':    ''
            }        

    # 検算
    for month in monthly_totals:
        _dbt_total = monthly_totals[month]['dbt']
        _cdt_total = monthly_totals[month]['cdt']
        if DEBUG: print(f'{month} 借方 {_dbt_total} 貸方 {_cdt_total} {_dbt_total - _cdt_total}')

    for month in monthly_totals:
        dir_path = f'data/journal_entry/{party}/TB'
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        with open(f'{dir_path}/{month}trial_balance.csv', 'w', newline='', encoding='utf-8-sig') as file:
            header = ['month','account_code','account_name','beginning_balance','dbt_amount','cdt_amount','ending_balance']
            writer = csv.DictWriter(file, fieldnames=header)
            # writer.writeheader()
            writer.writerow({'month':'月','account_code':'コード','account_name':'科目','beginning_balance':'前月残高','dbt_amount':'借方','cdt_amount':'貸方','ending_balance':'当月残高'})
            for row in list(monthly_balance[month].values()):
                writer.writerow(row)

    print('END')

if __name__ == '__main__':
    main()
