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

DEBUG = True

termDict ={
    'GL02': 'GL',
    'GL02-GL55': 'GL詳細',
    'GL55-GL60': '勘定科目セグメント',
    'GL55-GL68': '税情報',

    'GL02-01': 'seq', #
    'GL02-02': '仕訳ID', #
    'GL02-03': '文書コメント', #

    'GL64-02': 'ソース説明',
    'GL64-03': 'ERPサブレジャーモジュール',
    'GL64-04': 'システムマニュアル識別子',

    'GL57-01': '作成者ユーザーID',
    'GL57-02': '作成日',

    'GL55-01': '明細行番号', #
    'GL55-02': '転記日付', #
    'GL55-03': '仕訳エントリタイプコード',
    'GL55-04': '仕訳エントリ行説明',

    'GL55-05': '借方/貸方インディケータ',

    'GL55-06': '元文書番号', #
    'GL55-08': '元文書日付', #

    'GL63-01': '勘定科目番号',
    'GL63-02': '勘定科目名',

    'GL56-01': '金額',

    'GL60-01': '勘定科目セグメント番号',
    'GL60-02': '勘定科目セグメントコード',
    'GL60-03': '勘定科目セグメント名',

    'GL68-01': '税コード', #
    'GL68-02': '税率', #
    'GL68-04': '税コード説明' #
}
#TODO GL55-07 元文書種別, GL56-02 通貨コード のデフォルト値を設定する
termDictSorted = {
    'GL00':      'num',
    'GL02':      'GL',
    'GL02-GL55': 'GL詳細',
    'GL55-GL68': '税情報',
    'GL55-GL60': '勘定科目セグメント',
    'GL55-GL61': '事業セグメント',
    
    'GL02-01': 'seq', #
    'GL02-02': '仕訳ID', #
    'GL02-03': '文書コメント', #

    'GL64-01':   'ソースコード',
    'GL64-02':   'ソース説明',
    'GL64-03':   'ERPサブレジャーモジュール',
    'GL64-04':   'システムマニュアル識別子',

    'GL57-01':   '作成者ユーザーID',
    'GL57-02':   '作成日',

    'GL55-01': '明細行番号', #
    'GL55-02': '転記日付', #
    'GL55-03':   '仕訳エントリタイプコード',
    'GL55-04':   '仕訳エントリ行説明',
    'GL55-05':   '借方/貸方インディケータ',
    'GL55-06': '元文書番号', #
    'GL55-08': '元文書日付', #

    'GL63-01':   '勘定科目番号',
    'GL63-02':   '勘定科目名',
    'GL63-03':   '財務諸表キャプション',

    'GL56-01':   '金額',

    'GL68-01': '税コード', #
    'GL68-02': '税率', #
    'GL68-04': '税コード説明', #

    'GL60-01':   '勘定科目セグメント番号',
    'GL60-02':   '勘定科目セグメントコード',
    'GL60-03':   '勘定科目セグメント名',

    'GL61-01':   '事業セグメント順序番号',
    'GL61-02':   '事業セグメントコード',
    'GL61-03':   '組織タイプ名'
}

outDict = {
    'GL00':      'num',
    'GL02':      'GL',
    'GL02-GL55': 'GL詳細',
    'GL55-GL68d': '借方税情報',
    'GL55-GL68c': '貸方税情報',
    'GL55-GL60d': '借方勘定科目セグメント',
    'GL55-GL60c': '貸方勘定科目セグメント',
    'GL55-GL61': '事業セグメント',

    'GL02-01': '仕訳番号',
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
    'GL55-04': '摘要',
    'GL55-06': '元文書番号', #
    'GL55-08': '元文書日付', #

    'GL63-01d': '借方勘定科目番号',
    'GL63-02d': '借方勘定科目名',
    'GL63-03d': '借方財務諸表キャプション',

    'GL56-01d': '借方金額',
    'GL56-02d': '借方金額コード',

    'GL68-01d': '借方税コード', #
    'GL68-02d': '借方税率', #
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
    'GL68-02c': '貸方税率', #
    'GL68-04c': '貸方税コード説明', #
    
    'GL60-01c': '貸方勘定科目セグメント番号',
    'GL60-02c': '貸方勘定科目セグメントコード',
    'GL60-03c': '貸方勘定科目セグメント名',

    'GL61-01': '事業セグメント順序番号',
    'GL61-02': '事業セグメントコード',
    'GL61-03': '組織タイプ名'
}

def print_row(row):
    print(f"row {row['GL00']} | {row['GL02-GL55']} | {row['GL55-02']} | {row['GL55-04']} | {row['GL55-05']} | {row['GL63-02'] or '-'} JPY {row['GL56-01'] or '-'} | {row['GL60-01'] or '-'}:{row['GL60-03'] or '-'}")

def print_entry(journal_entry):
    print(f"{journal_entry['GL00']} | {journal_entry['GL02-GL55']} | {journal_entry['GL55-02']} | {journal_entry['GL55-04']} | {journal_entry['GL63-02d'] or '-'} JPY {journal_entry['GL56-01d'] or '-'} | {journal_entry['GL60-01d'] or '-'}:{journal_entry['GL60-03d'] or '-'} | {journal_entry['GL63-02c'] or '-'} JPY {journal_entry['GL56-01c'] or '-'} | {journal_entry['GL60-01c'] or '-'}:{journal_entry['GL60-03c'] or '-'}")

def main():
    in_file = "data/journal_entry/北海道産業(株)/GL_Details.csv"
    out_file = 'data/journal_entry/北海道産業(株)/horizontal_ledger.csv'
    out_header = list(outDict.keys())
    entryDict = {}
    journal_entries = []
    debit_records = []
    credit_records = []
    GL02 = None
    num = 0

    with open(in_file, 'r', encoding='utf-8-sig') as f:
        header = list(termDict.keys())
        reader = csv.DictReader(f, fieldnames=header)
        next(reader)
        records = []
        for row in reader:
            records.append(row)

    sorted_records = sorted(records, key=lambda x: (
        int(x['GL02']) if x.get('GL02') and 'END'!=x['GL02'] and x['GL02'].isdigit() else -1, 
        int(x['GL02-GL55']) if x.get('GL02-GL55') and x['GL02-GL55'].isdigit() else -1,  
        int(x['GL55-GL68']) if x.get('GL55-GL68') and x['GL55-GL68'].isdigit() else -1,  
        int(x['GL55-GL60']) if x.get('GL55-GL60') and x['GL55-GL60'].isdigit() else -1,  
        int(x['GL55-GL61']) if x.get('GL55-GL61') and x['GL55-GL61'].isdigit() else -1
    ))

    last = {'GL02': 'END'}
    for i in range(1, len(header)):
        last[header[i]] = ''
    sorted_records.append(last)

    with open(f'{in_file[:-4]}_sorted.csv', 'w', newline='', encoding='utf-8-sig') as file:
        header = list(termDictSorted.keys())
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writerow(termDictSorted)
        for num in range(len(sorted_records)):
            row = sorted_records[num]
            row['GL00'] = str(1+num)
            writer.writerow(row)

    previous_GL55_02 = previous_GL55_03 = previous_GL55_04 = ''
    previous_GL69_02 = ''
    previous_GL61_01 = previous_GL61_02 = previous_GL61_03 = ''
    debit_credit = None
    journal_entries = []
    debit_records = []
    credit_records = []
    detail_records = []    
    for i in range(len(sorted_records)):
        row = sorted_records[i]
        if GL02 and GL02!=row['GL02']:
            for journal_entry in journal_entries:
                out_record = {}
                for k in out_header:
                    out_record[k] = k in journal_entry and journal_entry[k] or ''
                # 重複をチェックしてリストに追加
                if not any(d['GL00'] == out_record['GL00'] and d['GL02'] == out_record['GL02'] and d['GL02-GL55'] == out_record['GL02-GL55'] for d in entryDict[GL02]):
                    entryDict[GL02].append(out_record) # GL Details
                else:
                    if DEBUG:
                        print(f"** GL Details GL00:{out_record['GL00']} GL02:{out_record['GL02']} GL02-GL55:{out_record['GL02-GL55']}")
            journal_entries = []
            debit_records = []
            credit_records = []
            detail_records = []
        if 'END'==GL02:
            break
        if ''!=row['GL02-01']:
            GL02 = row['GL02']
            # GL Header
            if 'GL02'==GL02:
                continue
            if not GL02 in entryDict:
                entryDict[GL02] = []
                previous_GL55_02 = previous_GL55_03 = previous_GL55_04 = ''
                previous_GL61_01 = previous_GL61_02 = previous_GL61_03 = ''
            journal_entry = {}
            journal_entry['GL00'] = row['GL00']
            journal_entry['GL02'] = GL02
            journal_entry['GL02-GL55'] = row['GL02-GL55']
            journal_entry['GL55-GL61'] = 'GL55-GL61' in row and row['GL55-GL61'] or ''
            journal_entry['GL02-01'] = 'GL02-01' in row and row['GL02-01'] or ''
            journal_entry['GL02-02'] = 'GL02-02' in row and row['GL02-02'] or ''
            journal_entry['GL02-03'] = 'GL02-03' in row and row['GL02-03'] or ''
            journal_entry['GL64-01'] = 'GL64-01' in row and row['GL64-01'] or ''
            journal_entry['GL64-02'] = 'GL64-02' in row and row['GL64-02'] or ''
            journal_entry['GL64-03'] = 'GL64-03' in row and row['GL64-03'] or ''
            journal_entry['GL64-04'] = 'GL64-04' in row and row['GL64-04'] or ''
            journal_entry['GL57-01'] = 'GL57-01' in row and row['GL57-01'] or ''
            journal_entry['GL57-02'] = 'GL57-02' in row and row['GL57-02'] or ''
            if 'GL55-02' in row and row['GL55-02']: # 列に値が存在する場合はその値を使用
                value = row['GL55-02']
            else: # 列に値が存在しない場合は以前の行で定義されていた値を使用
                value = previous_GL55_02
            previous_GL55_02 = value # 現在の値を次の行の前回値として保持
            if 'GL55-03' in row and row['GL55-03']: # 列に値が存在する場合はその値を使用
                value = row['GL55-03']
            else: # 列に値が存在しない場合は以前の行で定義されていた値を使用
                value = previous_GL55_03
            previous_GL55_03 = value  # 現在の値を次の行の前回値として保持
            if 'GL55-04' in row and row['GL55-04']: # 列に値が存在する場合はその値を使用
                value = row['GL55-04']
            else: # 列に値が存在しない場合は以前の行で定義されていた値を使用
                value = previous_GL55_04
            previous_GL55_04 = value   # 現在の値を次の行の前回値として保持  
            out_record = {}
            for k in out_header:
                out_record[k] = k in journal_entry and journal_entry[k] or ''
            entryDict[GL02].append(out_record) # GL Header
            if DEBUG:
                print(f"** GL Header  GL00:{out_record['GL00']} GL02:{out_record['GL02']} GL02-GL55:{out_record['GL02-GL55']}")
        elif ''==row['GL02-01'] and ''!=row['GL02-GL55']:
            # GL Detail
            if DEBUG:
                print_row(row)
            if ''!=row['GL55-05']:
                debit_credit = row['GL55-05']            
            journal_entry = {}
            journal_entry['GL00'] = row['GL00']
            journal_entry['GL02'] = GL02
            journal_entry['GL02-GL55'] = row['GL02-GL55']
            if 'GL55-01' in row and row['GL55-01']: # 列に値が存在する場合はその値を使用
                value = row['GL55-01']
            else: # 列に値が存在しない場合は以前の行で定義されていた値を使用
                value = journal_entry['GL02-GL55']
            journal_entry['GL55-01'] = ('GL55-GL60' not in row or ''==row['GL55-GL60']) and value or ''
            # previous_GL55_01 = journal_entry['GL55-01']  # 現在の値を次の行の前回値として保持
            if 'GL55-02' in row and row['GL55-02']: # 列に値が存在する場合はその値を使用
                value = row['GL55-02']
            else: # 列に値が存在しない場合は以前の行で定義されていた値を使用
                value = previous_GL55_02
            journal_entry['GL55-02'] = ('GL55-GL60' not in row or ''==row['GL55-GL60']) and value
            previous_GL55_02 = journal_entry['GL55-02']  # 現在の値を次の行の前回値として保持
            if 'GL55-03' in row and row['GL55-03']: # 列に値が存在する場合はその値を使用
                value = row['GL55-03']
            else: # 列に値が存在しない場合は以前の行で定義されていた値を使用
                value = previous_GL55_03
            journal_entry['GL55-03'] = ('GL55-GL60' not in row or ''==row['GL55-GL60']) and value
            previous_GL55_03 = journal_entry['GL55-03']  # 現在の値を次の行の前回値として保持
            if 'GL55-04' in row and row['GL55-04']: # 列に値が存在する場合はその値を使用
                value = row['GL55-04']
            else: # 列に値が存在しない場合は以前の行で定義されていた値を使用
                value = previous_GL55_04
            journal_entry['GL55-04'] = ('GL55-GL60' not in row or ''==row['GL55-GL60']) and value
            previous_GL55_04 = journal_entry['GL55-04']   # 現在の値を次の行の前回値として保持      
            # debit
            journal_entry['GL55-GL60d'] = '借方'==debit_credit and 'GL55-GL60' in row and row['GL55-GL60'] or ''
            journal_entry['GL63-01d'] = '借方'==debit_credit and 'GL63-01' in row and row['GL63-01'] or ''
            journal_entry['GL63-02d'] = '借方'==debit_credit and 'GL63-02' in row and row['GL63-02'] or ''
            journal_entry['GL63-03d'] = '借方'==debit_credit and 'GL63-03' in row and row['GL63-03'] or ''
            journal_entry['GL56-01d'] = '借方'==debit_credit and 'GL56-01' in row and row['GL56-01'].isdigit() and int(row['GL56-01']) or ''
            journal_entry['GL56-02d'] = '借方'==debit_credit and 'GL56-02' in row and ''!=row['GL56-02'] or ''
            journal_entry['GL68-01d'] = '借方'==debit_credit and 'GL68-01' in row and row['GL68-01'] or ''
            journal_entry['GL68-02d'] = '借方'==debit_credit and 'GL68-02' in row and row['GL68-02'] or ''
            journal_entry['GL68-04d'] = '借方'==debit_credit and 'GL68-04' in row and row['GL68-04'] or ''
            journal_entry['GL60-01d'] = '借方'==debit_credit and 'GL60-01' in row and row['GL60-01'] or ''
            journal_entry['GL60-02d'] = '借方'==debit_credit and 'GL60-02' in row and row['GL60-02'] or ''
            journal_entry['GL60-03d'] = '借方'==debit_credit and 'GL60-03' in row and row['GL60-03'] or ''
            # credit
            journal_entry['GL55-GL60c'] = '貸方'==debit_credit and 'GL55-GL60' in row and row['GL55-GL60'] or ''
            journal_entry['GL63-01c'] = '貸方'==debit_credit and 'GL63-01' in row and row['GL63-01'] or ''
            journal_entry['GL63-02c'] = '貸方'==debit_credit and 'GL63-02' in row and row['GL63-02'] or ''
            journal_entry['GL63-03c'] = '貸方'==debit_credit and 'GL63-03' in row and row['GL63-03'] or ''
            journal_entry['GL56-01c'] = '貸方'==debit_credit and 'GL56-01' in row and row['GL56-01'].isdigit() and int(row['GL56-01']) or ''
            journal_entry['GL56-02c'] = '貸方'==debit_credit and 'GL56-02' in row and ''!=row['GL56-02'] or ''
            journal_entry['GL68-01c'] = '貸方'==debit_credit and 'GL68-01' in row and row['GL68-01'] or ''
            journal_entry['GL68-02c'] = '貸方'==debit_credit and 'GL68-02' in row and row['GL68-02'] or ''
            journal_entry['GL68-04c'] = '貸方'==debit_credit and 'GL68-04' in row and row['GL68-04'] or ''
            journal_entry['GL60-01c'] = '貸方'==debit_credit and 'GL60-01' in row and row['GL60-01'] or ''
            journal_entry['GL60-02c'] = '貸方'==debit_credit and 'GL60-02' in row and row['GL60-02'] or ''
            journal_entry['GL60-03c'] = '貸方'==debit_credit and 'GL60-03' in row and row['GL60-03'] or ''
            if 'GL61-01' in row and row['GL61-01']: # 列に値が存在する場合はその値を使用
                value = row['GL61-01']
            else: # 列に値が存在しない場合は以前の行で定義されていた値を使用
                value = previous_GL61_01
            journal_entry['GL61-01'] = ('GL55-GL60' not in row or ''==row['GL55-GL60']) and value or ''
            previous_GL61_01 = journal_entry['GL61-01']  # 現在の値を次の行の前回値として保持
            if 'GL61-02' in row and row['GL61-02']: # 列に値が存在する場合はその値を使用
                value = row['GL61-02']
            else: # 列に値が存在しない場合は以前の行で定義されていた値を使用
                value = previous_GL61_02
            journal_entry['GL61-02'] = ('GL55-GL60' not in row or ''==row['GL55-GL60']) and value
            previous_GL61_02 = journal_entry['GL61-02']  # 現在の値を次の行の前回値として保持
            if 'GL61-03' in row and row['GL61-03']: # 列に値が存在する場合はその値を使用
                value = row['GL61-03']
            else: # 列に値が存在しない場合は以前の行で定義されていた値を使用
                value = previous_GL61_03
            journal_entry['GL61-03'] = ('GL55-GL60' not in row or ''==row['GL55-GL60']) and value
            previous_GL61_03 = journal_entry['GL61-03']  # 現在の値を次の行の前回値として保持

            if DEBUG: print_entry(journal_entry)
            detail_records.append(journal_entry)

            debit_records = [x for x in detail_records if ''!=x['GL56-01d']]
            credit_records = [x for x in detail_records if ''!=x['GL56-01c']]
            debit_amounts = sum([x['GL56-01d'] for x in debit_records])
            credit_amounts = sum([x['GL56-01c'] for x in credit_records])
            debit_count = len(debit_records)
            credit_count = len(credit_records)
            next_row = sorted_records[i+1]
            if abs(debit_amounts - credit_amounts) < 2:
                if ''!=next_row['GL55-GL60']:
                    continue
                if 1==debit_count:
                    for record in detail_records:
                        if record['GL00']==debit_records[0]['GL00']:# or ''==record['GL55-02']:
                            continue
                        record['GL63-01d'] = debit_records[0]['GL63-01d'] or ''
                        record['GL63-02d'] = debit_records[0]['GL63-02d'] or ''
                        record['GL63-03d'] = debit_records[0]['GL63-03d'] or ''
                        record['GL56-01d'] = record['GL56-01c'] or ''
                        record['GL68-01d'] = debit_records[0]['GL68-01d'] or ''
                        record['GL68-02d'] = debit_records[0]['GL68-02d'] or ''
                        record['GL68-04d'] = debit_records[0]['GL68-04d'] or ''
                        record['GL60-01d'] = debit_records[0]['GL60-01d'] or ''
                        record['GL60-02d'] = debit_records[0]['GL60-02d'] or ''
                        record['GL60-03d'] = debit_records[0]['GL60-03d'] or ''
                        if DEBUG: print_entry(record)
                    i = 0
                    for record in detail_records:
                        if record['GL00']==debit_records[0]['GL00']:
                            del detail_records[i]
                        i += 1    
                elif 1==credit_count:
                    for record in detail_records:
                        if record['GL00']==credit_records[0]['GL00']:# or ''==record['GL55-02']:
                            continue
                        record['GL63-01c'] = credit_records[0]['GL63-01c'] or ''
                        record['GL63-02c'] = credit_records[0]['GL63-02c'] or ''
                        record['GL63-03c'] = credit_records[0]['GL63-03c'] or ''
                        record['GL56-01c'] = record['GL56-01d'] or ''
                        record['GL68-01c'] = credit_records[0]['GL68-01c'] or ''
                        record['GL68-02c'] = credit_records[0]['GL68-02c'] or ''
                        record['GL68-04c'] = credit_records[0]['GL68-04c'] or ''
                        record['GL60-01c'] = credit_records[0]['GL60-01c'] or ''
                        record['GL60-02c'] = credit_records[0]['GL60-02c'] or ''
                        record['GL60-03c'] = credit_records[0]['GL60-03c'] or ''
                        if DEBUG: print_entry(record)
                    i = 0
                    for record in detail_records:
                        if record['GL00']==credit_records[0]['GL00']:
                            del detail_records[i]                        
                        i += 1
                if DEBUG:
                    print('-- detail_records --')
                    for d in detail_records:
                        print_entry(d)
                    print('-- --')
                journal_entries += detail_records
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

    horizontal_ledger = sorted(horizontal_records, key=lambda x: (
        int(x['GL02']) if x.get('GL02') and 'END'!=x['GL02'] and x['GL02'].isdigit() else -1, 
        int(x['GL02-GL55']) if x.get('GL02-GL55') and x['GL02-GL55'].isdigit() else -1, 
        int(x['GL55-GL68d']) if x.get('GL55-GL68d') and x['GL55-GL68d'].isdigit() else -1, 
        int(x['GL55-GL68c']) if x.get('GL55-GL68c') and x['GL55-GL68c'].isdigit() else -1,
        int(x['GL55-GL60d']) if x.get('GL55-GL60d') and x['GL55-GL60d'].isdigit() else -1, 
        int(x['GL55-GL60c']) if x.get('GL55-GL60c') and x['GL55-GL60c'].isdigit() else -1
    ))

    with open(out_file, 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.DictWriter(file, fieldnames=out_header)
        writer.writerow(outDict)
        for row in horizontal_ledger:
            writer.writerow(row)

    print(f'** END {out_file}')

if __name__=='__main__':
    main()
