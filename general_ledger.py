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

DEBUG = True

lines       = []
effectiveMonth = None
monthDebit  = 0
monthCredit = 0
totalDebit  = 0
totalCredit = 0
netAmount   = 0

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
    'GL55-02': '記帳日付', #
    'GL55-03': '仕訳エントリタイプコード',
    'GL55-04': '仕訳エントリ行説明',
    'GL55-06': '元文書番号', #
    'GL55-08': '元文書日付', #

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
    'GL55-02': '伝票日付',
    'GL55-04': '摘要',

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

    'GL55-02': '伝票日付',
    'GL55-04': '摘要',

    'GL63-01cn': '相手勘定科目番号',
    'GL63-02cn': '相手勘定科目名',

    'GL56-01d': '借方金額',
    'GL56-01c': '貸方金額',
    'GL56-01net': '差引金額'    
}

header = ['GL02','GL02-GL55','GL55-04','GL55-02','GL63-01cn','GL63-02cn','GL56-01d','GL56-01c','GL56-01net']

def record_entry(accountNumber,entry):
    global lines
    global effectiveMonth
    global monthDebit
    global monthCredit
    global totalDebit
    global totalCredit
    global netAmount
    effectiveMonth = entry['GL55-02'][:7]
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
    line['GL55-02']   = entry['GL55-02']
    line['GL55-04']   = entry['GL55-04']
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
    global effectiveMonth
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
            if ''==row['GL02-GL55']:# or ''!=row['GL55-GL60d']or ''!=row['GL55-GL60c']or ''!=row['GL55-GL61']:
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
    previous_GL55_02 = previous_GL55_04 = ''
    for i in range(len(records)):
        row = records[i]
        if len(row['GL02-GL55'])>0:
            num              = row['GL00']
            GL02             = row['GL02']
            GL02_GL55        = row['GL02-GL55']
            date             = row['GL55-02']
            form             = row['GL55-03']       
            note             = row['GL55-04']
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
                                'date': date, 'form': form, 'contra_acct': cdt_account, 'contra_acct_name': cdt_account_name,
                                'dbt_amount': dbt_amount, 'cdt_amount': 0, 'balance': general_ledger[dbt_account]["balance"],
                                'dbt_tax_code': dbt_tax_code, 'dbt_tax_rate': dbt_tax_rate, 'dbt_tax_desc': dbt_tax_desc,
                                'cdt_tax_code': '', 'cdt_tax_rate': '', 'cdt_tax_desc': '',
                                'note': note}
            general_ledger[dbt_account]['transactions'].append(debit_transaction_data)
            if 'transactions' not in general_ledger[cdt_account]:
                general_ledger[cdt_account]['transactions'] = []
            credit_transaction_data = {'num': num, 'GL02':GL02, 'GL02-GL55':GL02_GL55,
                                'date': date, 'form': form, 'contra_acct': dbt_account, 'contra_acct_name': dbt_account_name,
                                'dbt_amount': 0, 'cdt_amount': cdt_amount, 'balance': general_ledger[cdt_account]["balance"],
                                'dbt_tax_code': '', 'dbt_tax_rate': '', 'dbt_tax_desc': '',
                                'cdt_tax_code': cdt_tax_code, 'cdt_tax_rate': cdt_tax_rate, 'cdt_tax_desc': cdt_tax_desc,
                                'note': note}
            general_ledger[cdt_account]['transactions'].append(credit_transaction_data)

    account_totals  = {}
    dbt_total = cdt_total = 0
    target_months = list(set([x['date'][:7] for key in general_ledger for x in general_ledger[key]['transactions']]))
    for account_code, account_data in general_ledger.items():
        for month in target_months:
            if month not in account_totals:
                account_totals[month] = {}
            if account_code not in account_totals[month]:
                account_totals[month][account_code] = {}
            account_totals[month][account_code]['dbt'] = sum([x['dbt_amount'] for x in general_ledger[account_code]['transactions'] if month == x['date'][:7]])
            account_totals[month][account_code]['cdt'] = sum([x['cdt_amount'] for x in general_ledger[account_code]['transactions'] if month == x['date'][:7]])
            
    monthly_totals = {}
    for month in target_months:
        if month not in monthly_totals:
            monthly_totals[month] = {}
        monthly_totals[month]['dbt'] = sum(
                [x['dbt_amount'] for key in general_ledger 
                                    for x in general_ledger[key]['transactions'] if month == x['date'][:7]])
        monthly_totals[month]['cdt'] = sum(
                [x['dbt_amount'] for key in general_ledger 
                                    for x in general_ledger[key]['transactions'] if month == x['date'][:7]])
    for month in monthly_totals:
        _dbt_total = monthly_totals[month]['dbt']
        _cdt_total = monthly_totals[month]['cdt']
        if DEBUG: print(f'{month} 借方 {_dbt_total} 貸方 {_cdt_total} {_dbt_total - _cdt_total}')

    # 5. 総勘定元帳を出力する    
    for account_code, account_data in general_ledger.items():
        account_name = account_data['account_name']
        dbt_amount   = account_data['dbt']
        cdt_amount   = account_data['cdt']
        balance      = account_data['balance']
        if DEBUG: print(f'期間合計: {account_code}:{account_name} 借方 {"{:,}".format(dbt_amount)} 貸方 {"{:,}".format(cdt_amount)}')
        record = {
            'num':              '',#f'{account_code}:{account_name}',
            'GL02':             '',
            'GL02-GL55':        '',
            'date':             '期間合計',
            'contra_acct':      '',
            'contra_acct_name': '',
            'dbt_amount':       dbt_amount,
            'cdt_amount':       cdt_amount,
            'balance':          balance
        }
        if 'record' not in general_ledger[account_code]:
            general_ledger[account_code]['record'] = []
        general_ledger[account_code]['record'].append(record)
        # transaction data
        dbt_total = cdt_total = 0
        month = None
        transactions = account_data['transactions']
        sorted_transactions = sorted(transactions, key=lambda x: x['date'])
        for transaction_data in sorted_transactions:
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
                    'balance':          ''
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
            dbt_tax_code     = transaction_data['dbt_tax_code']
            dbt_tax_rate     = transaction_data['dbt_tax_rate']
            dbt_tax_desc     = transaction_data['dbt_tax_desc']
            cdt_tax_code     = transaction_data['cdt_tax_code']
            cdt_tax_rate     = transaction_data['cdt_tax_rate']
            cdt_tax_desc     = transaction_data['cdt_tax_desc']
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
                'dbt_tax_code':     dbt_tax_code,
                'dbt_tax_rate':     dbt_tax_rate,
                'dbt_tax_desc':     dbt_tax_desc,
                'cdt_amount':       cdt_amount,
                'cdt_tax_code':     cdt_tax_code,
                'cdt_tax_rate':     cdt_tax_rate,
                'cdt_tax_desc':     cdt_tax_desc,
                'balance':          balance
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
            'dbt_tax_code':     '',
            'dbt_tax_rate':     '',
            'dbt_tax_desc':     '',
            'cdt_amount':       cdt_total,
            'cdt_tax_code':     '',
            'cdt_tax_rate':     '',
            'cdt_tax_desc':     '',
            'balance':          balance
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
    monthly_balance = {}
    ending_balance = {}
    totals = dict(sorted(account_totals.items()))
    months = sorted(totals.keys())  # 月の一覧をソート
    beginning_balance = {month: {account: 0 for account in totals[months[0]]} for month in months}

    for i in range(len(months)):
        month = months[i]
        next_month = months[i+1] if i < len(months)-1 else None

        monthly_balance[month] = {}
        ending_balance[month] = {}

        for account in sorted(totals[month].keys()):
            dbt = totals[month][account]['dbt']
            cdt = totals[month][account]['cdt']

            balance = beginning_balance[month][account] + dbt - cdt
            ending_balance[month][account] = balance

            monthly_balance[month][account] = {
                'month': month,
                'account_code': account,
                'account_name': accounts[account],
                'beginning_balance': beginning_balance[month][account],
                'dbt_amount': dbt,
                'cdt_amount': cdt,
                'ending_balance': balance
            }

        if next_month:
            beginning_balance[next_month] = ending_balance[month].copy()

    for month in monthly_totals:
        dir_path = f'data/journal_entry/{party}/TB'
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        with open(f'{dir_path}/{month}trial_balance.csv', 'w', newline='', encoding='utf-8-sig') as file:
            header = ['month','account_code','account_name','beginning_balance','dbt_amount','cdt_amount','ending_balance']
            writer = csv.DictWriter(file, fieldnames=header)
            writer.writerow({'month':'月','account_code':'コード','account_name':'科目','beginning_balance':'前月残高','dbt_amount':'借方','cdt_amount':'貸方','ending_balance':'当月残高'})
            for row in list(monthly_balance[month].values()):
                writer.writerow(row)

    print(f'** END data/journal_entry/{party}')

if __name__ == '__main__':
    main()
