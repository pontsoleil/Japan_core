#!/usr/bin/env python3
# coding: utf-8
#
# generate horizontal ledger CSV xBRL-CSV
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

termDict = {
    'GL02': 'GL (General Ledger)',
    'GL02-GL55': 'GL詳細 (Specified GL Details)',
    'GL55-GL60': '勘定科目セグメント (Specified Account Segment)',
    'GL55-GL61': '事業セグメント (Specified Business Segment)',
    'GL02-01': '仕訳ID (Journal ID)',
    'GL64-01': 'ソースコード (Source Code)',
    'GL64-02': 'ソース説明 (Source Description)',
    'GL64-03': 'ERPサブレジャーモジュール (ERP Subledger Module)',
    'GL64-04': 'システムマニュアル識別子 (System Manual Identifier)',
    'GL57-01': '作成者ユーザーID (Created User ID)',
    'GL57-02': '作成日 (Created Date)',
    'GL55-03': '仕訳エントリタイプコード (Journal Entry Type Code)',
    'GL55-04': '仕訳エントリ行説明 (Journal Entry Line Description)',

    'GL55-05': '借方/貸方インディケータ (Credit Debit Indicator)',

    'GL63-01': '勘定科目番号 (GL Account Number)',
    'GL63-02': '勘定科目名 (GL Account Name)',
    'GL63-03': '財務諸表キャプション (Financial Statement Caption)',
    'GL56-01': '金額 (Functional Amount)',

    'GL56-02': '通貨コード (Functional Currency Code)',
    'GL69-02': '記帳日 (Posted Date)',

    'GL60-01': '勘定科目セグメント番号 (Account Segment Number)',
    'GL60-02': '勘定科目セグメントコード (Account Segment Code)',
    'GL60-03': '勘定科目セグメント名 (Account Segment Name)',

    'GL61-01': '事業セグメント順序番号 (Business Segment Sequence Number)',
    'GL61-02': '事業セグメントコード (Business Segment Code)',
    'GL61-03': '組織タイプ名 (Organization Type Name)'
}

outDict = {
    'GL02': 'GL (General Ledger)',
    'GL02-GL55': 'GL詳細 (Specified GL Details)',
    'GL55-GL60d': '借方勘定科目セグメント (Debit Account Segment)',
    'GL55-GL60c': '貸方勘定科目セグメント (Credit Account Segment)',
    'GL55-GL61': '事業セグメント (Specified Business Segment)',

    'GL02-01': '仕訳ID (Journal ID)',
    'GL64-01': 'ソースコード (Source Code)',
    'GL64-02': 'ソース説明 (Source Description)',
    'GL64-03': 'ERPサブレジャーモジュール (ERP Subledger Module)',
    'GL64-04': 'システムマニュアル識別子 (System Manual Identifier)',
    'GL57-01': '作成者ユーザーID (Created User ID)',
    'GL57-02': '作成日 (Created Date)',
    'GL55-03': '仕訳エントリタイプコード (Journal Entry Type Code)',
    'GL55-04': '仕訳エントリ行説明 (Journal Entry Line Description)',

    'GL69-02': '記帳日 (Posted Date)',
    'GL56-02': '通貨コード (Functional Currency Code)',

    'GL63-01d': '借方勘定科目番号 (Debit Account Number)',
    'GL63-02d': '借方勘定科目名 (Debit Account Name)',
    'GL63-03d': '借方財務諸表キャプション (Debit Financial Statement Caption)',

    'GL56-01d': '借方金額 (Debit Functional Amount)',

    'GL60-01d': '借方勘定科目セグメント番号 (Account Segment Number)',
    'GL60-02d': '借方勘定科目セグメントコード (Account Segment Code)',
    'GL60-03d': '借方勘定科目セグメント名 (Account Segment Name)',

    'GL63-01c': '貸方勘定科目番号 (Credit Account Number)',
    'GL63-02c': '貸方勘定科目名 (Credit Account Name)',
    'GL63-03c': '貸方財務諸表キャプション (Credit Financial Statement Caption)',

    'GL56-01c': '貸方金額 (CreditFunctional Amount)',

    'GL60-01c': '貸方勘定科目セグメント番号 (Account Segment Number)',
    'GL60-02c': '貸方勘定科目セグメントコード (Account Segment Code)',
    'GL60-03c': '貸方勘定科目セグメント名 (Account Segment Name)',

    'GL61-01': '事業セグメント順序番号 (Business Segment Sequence Number)',
    'GL61-02': '事業セグメントコード (Business Segment Code)',
    'GL61-03': '組織タイプ名 (Organization Type Name)'
}

outDictCT = {
    'GL02': 'GL (General Ledger)',
    'GL02-GL55': 'GL詳細 (Specified GL Details)',

    'GL69-02': '記帳日 (Posted Date)',
    'GL55-04': '仕訳エントリ行説明 (Journal Entry Line Description)',

    'GL63-01d': '借方勘定科目番号 (Debit Account Number)',
    'GL63-02d': '借方勘定科目名 (Debit Account Name)',
    'GL56-01d': '借方金額 (Debit Functional Amount)',
    'CT01d':    '借方消費税科目番号',
    'CT02d':    '借方消費税科目名',
    'CTdAmount':'借方消費税額',

    'GL63-01c': '貸方勘定科目番号 (Credit Account Number)',
    'GL63-02c': '貸方勘定科目名 (Credit Account Name)',
    'GL56-01c': '貸方金額 (CreditFunctional Amount)',
    'CT01c':    '貸方消費税科目番号',
    'CT02c':    '貸方消費税科目名',
    'CTcAmount':'貸方消費税額'
}

def main():
    in_file = 'data/journal_entry/test/793.csv' # 'data/journal_entry/instances.csv'
    out_file = 'data/journal_entry/test/horizontal_ledger.csv' #'data/journal_entry/horizontal_ledger.csv'
    out_header = list(outDict.keys())
    entryDict = {}
    journal_records = []
    debit_records = []
    credit_records = []
    GL02 = None
    num = 0
    # CSVファイルからデータを読み込む 0001-20090405-254-13-1-487.csv 0001-20100331-70-2778-1-6017.csv 0001-20100331-70-2778-1-6017.csv
    with open(in_file, 'r', encoding='utf-8-sig') as f:
        header = list(termDict.keys())
        reader = csv.DictReader(f, fieldnames=header)
        next(reader)
        records = []
        for row in reader:
            records.append(row)

    last = {'GL02': 'END'}
    for i in range(1, len(header)):
        last[header[i]] = ''
    records.append(last)

    GL55_04 = 0
    GL61_01 = GL61_02 = GL61_03 = 0
    debit_credit = None
    for i in range(len(records)):
        row = records[i]
        if GL02 != row['GL02']:
            if not GL02 in entryDict:
                entryDict[GL02] = []
            for journal_record in journal_records:
                out_record = {}
                for k in out_header:
                    out_record[k] = k in journal_record and journal_record[k] or ''
                entryDict[GL02].append(out_record)
            GL02 = row['GL02']
            journal_records = []
            debit_records = []
            credit_records = []
            detail_records = []
            num = 0
        if 'END' == GL02:
            break
        if len(row['GL02-01']) > 0:
            # GL Header
            if 'GL02' == GL02:
                continue
            if not GL02 in entryDict:
                entryDict[GL02] = []
                GL55_04 = 0
                GL61_01 = GL61_02 = GL61_03 = 0
            journal_record = {}
            journal_record['num'] = num
            journal_record['GL02'] = GL02
            journal_record['GL02-GL55'] = row['GL02-GL55']
            journal_record['GL55-GL61'] = row['GL55-GL61']
            journal_record['GL02-01'] = row['GL02-01']
            journal_record['GL64-01'] = row['GL64-01']
            journal_record['GL64-02'] = row['GL64-02']
            journal_record['GL64-03'] = row['GL64-03']
            journal_record['GL64-04'] = row['GL64-04']
            journal_record['GL57-01'] = row['GL57-01']
            journal_record['GL57-02'] = row['GL57-02']
            out_record = {}
            for k in out_header:
                out_record[k] = k in journal_record and journal_record[k] or ''
            entryDict[GL02].append(out_record)
            num += 1
        elif len(row['GL02-GL55']) > 0:
            # GL Detail
            if len(row['GL55-05']) > 0:
                debit_credit = row['GL55-05']
            journal_record = {}
            journal_record['num'] = num
            num += 1
            journal_record['GL02'] = GL02
            journal_record['GL02-GL55'] = row['GL02-GL55']
            if len(row['GL55-03']) > 0: GL55_03 = row['GL55-03']
            journal_record['GL55-03'] = (not 'GL55-GL60' in row or ''==row['GL55-GL60']) and GL55_03 or ''
            if len(row['GL55-04']) > 0: GL55_04 = row['GL55-04']
            journal_record['GL55-04'] = (not 'GL55-GL60' in row or ''==row['GL55-GL60']) and GL55_04 or ''
            if len(row['GL56-02']) > 0: GL56_02 = row['GL56-02']
            journal_record['GL56-02'] = (not 'GL55-GL60' in row or ''==row['GL55-GL60']) and GL56_02 or ''
            if len(row['GL69-02']) > 0: GL69_02 = row['GL69-02']
            journal_record['GL69-02'] = (not 'GL55-GL60' in row or ''==row['GL55-GL60']) and GL69_02 or ''
            if len(row['GL61-01']) > 0: GL61_01 = row['GL61-01']
            journal_record['GL61-01'] = (not 'GL55-GL60' in row or ''==row['GL55-GL60']) and GL61_01 or ''
            if len(row['GL61-02']) > 0: GL61_02 = row['GL61-02']
            journal_record['GL61-02'] = (not 'GL55-GL60' in row or ''==row['GL55-GL60']) and GL61_02 or ''
            if len(row['GL61-03']) > 0: GL61_03 = row['GL61-03']
            journal_record['GL61-03'] = (not 'GL55-GL60' in row or ''==row['GL55-GL60']) and GL61_03 or ''
            # debit
            journal_record['GL55-GL60d'] = 'debit' == debit_credit and len(row['GL55-GL60']) > 0 and row['GL55-GL60'] or ''
            journal_record['GL63-01d'] = 'debit' == debit_credit and len(row['GL55-03']) > 0 and row['GL63-01'] or ''
            journal_record['GL63-02d'] = 'debit' == debit_credit and len(row['GL55-03']) > 0 and row['GL63-02'] or ''
            journal_record['GL63-03d'] = 'debit' == debit_credit and len(row['GL55-03']) > 0 and row['GL63-03'] or ''
            journal_record['GL56-01d'] = 'debit' == debit_credit and len(row['GL56-01']) > 0 and int(row['GL56-01']) or ''
            journal_record['GL60-01d'] = 'debit' == debit_credit and row['GL60-01'] or ''
            journal_record['GL60-02d'] = 'debit' == debit_credit and row['GL60-02'] or ''
            journal_record['GL60-03d'] = 'debit' == debit_credit and row['GL60-03'] or ''
            # credit
            journal_record['GL55-GL60c'] = 'credit' == debit_credit and len(row['GL55-GL60']) > 0 and row['GL55-GL60'] or ''
            journal_record['GL63-01c'] = 'credit' == debit_credit and len(row['GL55-03']) > 0 and row['GL63-01'] or ''
            journal_record['GL63-02c'] = 'credit' == debit_credit and len(row['GL55-03']) > 0 and row['GL63-02'] or ''
            journal_record['GL63-03c'] = 'credit' == debit_credit and len(row['GL55-03']) > 0 and row['GL63-03'] or ''
            journal_record['GL56-01c'] = 'credit' == debit_credit and len(row['GL56-01']) > 0 and int(row['GL56-01']) or ''
            journal_record['GL60-01c'] = 'credit' == debit_credit and row['GL60-01'] or ''
            journal_record['GL60-02c'] = 'credit' == debit_credit and row['GL60-02'] or ''
            journal_record['GL60-03c'] = 'credit' == debit_credit and row['GL60-03'] or ''

            detail_records.append(journal_record)

            debit_records = [x for x in detail_records if '' != x['GL56-01d']]
            credit_records = [x for x in detail_records if '' != x['GL56-01c']]
            debit_amounts = sum([x['GL56-01d'] for x in debit_records])
            credit_amounts = sum([x['GL56-01c'] for x in credit_records])
            debit_count = len(debit_records)
            credit_count = len(credit_records)
            if abs(debit_amounts - credit_amounts) < 2:
                j = i + 1
                next_row = records[j]
                if '' != next_row['GL55-GL60']:
                    continue
                deleted_GL02_GL55 = None
                if 1 == debit_count:
                    for record in detail_records:
                        if record['num'] == debit_records[0]['num'] or 0 == len(record['GL55-03']) or ('' == record['GL56-01d'] and '' == record['GL56-01c']):
                            continue
                        record['GL63-01d'] = debit_records[0]['GL63-01d'] or ''
                        record['GL63-02d'] = debit_records[0]['GL63-02d'] or ''
                        record['GL63-03d'] = debit_records[0]['GL63-03d'] or ''
                        record['GL56-01d'] = record['GL56-01c'] or ''
                        record['GL60-01d'] = debit_records[0]['GL60-01d'] or ''
                        record['GL60-02d'] = debit_records[0]['GL60-02d'] or ''
                        record['GL60-03d'] = debit_records[0]['GL60-02d'] or ''
                    i = 0
                    for record in detail_records:
                        if record['num'] == debit_records[0]['num']:
                            deleted_GL02_GL55 = 'GL02-GL55' in debit_records[0] and debit_records[0]['GL02-GL55'] or None
                            del detail_records[i]
                            break
                elif 1 == credit_count:
                    for record in detail_records:
                        if record['num'] == credit_records[0]['num'] or 0 == len(record['GL55-03']) or ('' == record['GL56-01d'] and '' == record['GL56-01c']):
                            continue
                        record['GL63-01c'] = credit_records[0]['GL63-01c'] or ''
                        record['GL63-02c'] = credit_records[0]['GL63-02c'] or ''
                        record['GL63-03c'] = credit_records[0]['GL63-03c'] or ''
                        record['GL56-01c'] = record['GL56-01d'] or ''
                        record['GL60-01c'] = credit_records[0]['GL60-01c'] or ''
                        record['GL60-02c'] = credit_records[0]['GL60-02c'] or ''
                        record['GL60-03c'] = credit_records[0]['GL60-03c'] or ''
                    i = 0
                    for record in detail_records:
                        if record['num'] == credit_records[0]['num']:
                            deleted_GL02_GL55 = 'GL02-GL55' in credit_records[0] and credit_records[0]['GL02-GL55'] or None
                            del detail_records[i]
                            break
                        i += 1
                if deleted_GL02_GL55:
                    target_records = [
                        x for x in detail_records if '' == x['GL55-GL60d'] and '' == x['GL55-GL60c']]
                    inserting_records = [x for x in detail_records + journal_records if (
                        '' != x['GL55-GL60d'] or '' != x['GL55-GL60c']) and deleted_GL02_GL55 == x['GL02-GL55']]
                    if len(target_records) > 0 and len(inserting_records) > 0:
                        count_targets = len(target_records)
                        count_inserts = len(inserting_records)
                        for i in range(count_targets):
                            record = target_records[i*(1+count_inserts)]
                            insert_records = []
                            for i_record in inserting_records:
                                insert_record = i_record.copy()
                                insert_record['GL02-GL55'] = record['GL02-GL55']
                                insert_records.append(insert_record)
                            target_records[i*count_inserts+1:i*count_inserts+1] = insert_records
                        journal_records += target_records
                        detail_records = []
                    else:
                        journal_records += detail_records
                        detail_records = []
                else:
                    journal_records += [x for x in detail_records if ''==x['GL55-GL60d'] and '' == x['GL55-GL60c']]
                    detail_records = []

    horizontal_records = []
    for k, v in entryDict.items():
        for record in v:
            out_record = {}
            for key in out_header:
                if key in record:
                    out_record[key] = record[key]
                else:
                    out_record[key] = ''
            horizontal_records.append(out_record)

    horizontal_ledger = sorted(horizontal_records, key=lambda x: (x['GL02'], int(x['GL02-GL55']) if x['GL02-GL55'].isdigit(
    ) else -1, int(x['GL55-GL60d']) if x['GL55-GL60d'].isdigit() else -1, int(x['GL55-GL60c']) if x['GL55-GL60c'].isdigit() else -1))

    with open(out_file, 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.DictWriter(file, fieldnames=out_header)
        writer.writerow(outDict)
        for row in horizontal_ledger:
            writer.writerow(row)

    # account_list = {}
    # for row in horizontal_ledger:
    #     account_code = row['GL63-01d']
    #     account_name = row['GL63-02d']
    #     if '' != account_code:
    #         account_list[account_code] = account_name
    #     account_code = row['GL63-01c']
    #     account_name = row['GL63-02c']
    #     if '' != account_code:
    #         account_list[account_code] = account_name

    # accounts = sorted(account_list.items())

    # tax_accounts = [x for x in accounts if '消費税' in x[1]]
    # tax_keys = [x[0] for x in tax_accounts]

    # entries = []
    # for data in horizontal_ledger:
    #     entry = {}
    #     for k in out_header:
    #         if not k in ['GL02-01','GL55-03','GL56-02','GL57-01','GL57-02','GL60-01d', 'GL60-02d','GL60-03d','GL60-01c', 'GL60-02c','GL60-03c','GL61-01','GL61-02','GL61-03','GL63-03d','GL63-03c','GL64-01','GL64-02','GL64-03','GL64-04']:
    #             entry[k] = data[k]
    #     if ''==entry['GL02-GL55'] or ''!=entry['GL55-GL60d'] or ''!=entry['GL55-GL60c'] or ''!=entry['GL55-GL61']:
    #         continue
    #     del entry['GL55-GL60d']
    #     del entry['GL55-GL60c']
    #     del entry['GL55-GL61']
    #     if entry['GL63-01d'] in tax_keys:
    #         ct01d = entry['GL63-01d']
    #         ct02d = entry['GL63-02d']
    #         ctDamount = entry['GL56-01d']
    #         entries[-1]['GL56-01c'] = ctDamount + (''!=entries[-1]['GL56-01c'] and entries[-1]['GL56-01c'] or 0)
    #         entries[-1]['CT01d'] = ct01d
    #         entries[-1]['CT02d'] = ct02d
    #         entries[-1]['CTdAmount'] = ctDamount
    #         entries[-1]['CT01c'] = ''
    #         entries[-1]['CT02c'] = ''
    #         entries[-1]['CTcAmount'] = ''
    #     elif entry['GL63-01c'] in tax_keys:
    #         ct01c = entry['GL63-01c']
    #         ct02c = entry['GL63-02c']
    #         ctCamount = entry['GL56-01c']
    #         entries[-1]['GL56-01d'] = ctDamount + (''!=entries[-1]['GL56-01d'] and entries[-1]['GL56-01d'] or 0)
    #         entries[-1]['CT01d'] = ''
    #         entries[-1]['CT02d'] = ''
    #         entries[-1]['CTdAmount'] = ''
    #         entries[-1]['CT01c'] = ct01c
    #         entries[-1]['CT02c'] = ct02c
    #         entries[-1]['CTcAmount'] = ctCamount
    #     else:
    #         entry['CT01d'] = ''
    #         entry['CT02d'] = ''
    #         entry['CTdAmount'] = ''
    #         entry['CT01c'] = ''
    #         entry['CT02c'] = ''
    #         entry['CTcAmount'] = ''        
    #         entries.append(entry)

    # with open('data/journal_entry/horizontal_ledger_CT.csv', 'w', newline='', encoding='utf-8-sig') as file:
    #     out_headerCT = list(outDictCT.keys())
    #     writer = csv.DictWriter(file, fieldnames=out_headerCT)
    #     writer.writerow(outDictCT)
    #     # writer.writeheader()
    #     for row in entries:
    #         writer.writerow(row)

    print('END')

if __name__ == '__main__':
    main()
