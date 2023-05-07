import csv


def main():

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

        'GL63-01': '総勘定元帳科目番号 (GL Account Number)',
        'GL63-02': '総勘定元帳科目名 (GL Account Name)',
        'GL63-03': '財務諸表キャプション (Financial Statement Caption)',
        'GL56-01': '機能通貨金額 (Functional Amount)',

        'GL56-02': '機能通貨コード (Functional Currency Code)',
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
        'GL56-02': '機能通貨コード (Functional Currency Code)',

        'GL63-01d': '借方総勘定元帳科目番号 (Debit Account Number)',
        'GL63-02d': '借方総勘定元帳科目名 (Debit Account Name)',
        'GL63-03d': '借方財務諸表キャプション (Debit Financial Statement Caption)',

        'GL56-01d': '借方機能通貨金額 (Debit Functional Amount)',

        'GL60-01d': '借方勘定科目セグメント番号 (Account Segment Number)',
        'GL60-02d': '借方勘定科目セグメントコード (Account Segment Code)',
        'GL60-03d': '借方勘定科目セグメント名 (Account Segment Name)',

        'GL63-01c': '貸方総勘定元帳科目番号 (Credit Account Number)',
        'GL63-02c': '貸方総勘定元帳科目名 (Credit Account Name)',
        'GL63-03c': '貸方財務諸表キャプション (Credit Financial Statement Caption)',

        'GL56-01c': '貸方機能通貨金額 (CreditFunctional Amount)',

        'GL60-01c': '貸方勘定科目セグメント番号 (Account Segment Number)',
        'GL60-02c': '貸方勘定科目セグメントコード (Account Segment Code)',
        'GL60-03c': '貸方勘定科目セグメント名 (Account Segment Name)',

        'GL61-01': '事業セグメント順序番号 (Business Segment Sequence Number)',
        'GL61-02': '事業セグメントコード (Business Segment Code)',
        'GL61-03': '組織タイプ名 (Organization Type Name)'
    }

    out_header = list(outDict.keys())

    entryDict = {}
    journal_records = []
    debit_records = []
    credit_records = []
    GL02 = None
    num = 0
    # CSVファイルからデータを読み込む 0001-20090405-254-13-1-487.csv 0001-20100331-70-2778-1-6017.csv 0001-20100331-70-2778-1-6017.csv
    with open('instances.csv', 'r', encoding='utf-8-sig') as f:
        header = list(termDict.keys())
        reader = csv.DictReader(f, fieldnames=header)
        next(reader)

        records = []
        for row in reader:
            records.append(row)

    last = {'GL02':'END'}
    for i in range(1,len(header)):
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
            debit_records   = []
            credit_records  = []
            detail_records  = []
            num = 0
        if 'END'==GL02:
            break
        if len(row['GL02-01'])>0:
            # GL Header
            if 'GL02'==GL02:
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
            journal_record['GL02-01']   = row['GL02-01']
            journal_record['GL64-01']   = row['GL64-01']
            journal_record['GL64-02']   = row['GL64-02']
            journal_record['GL64-03']   = row['GL64-03']
            journal_record['GL64-04']   = row['GL64-04']
            journal_record['GL57-01']   = row['GL57-01']
            journal_record['GL57-02']   = row['GL57-02']
            out_record = {}
            for k in out_header:
                out_record[k] = k in journal_record and journal_record[k] or ''
            entryDict[GL02].append(out_record)
            num += 1
        elif len(row['GL02-GL55'])>0:
            # GL Detail
            if len(row['GL55-05'])>0:
                debit_credit = row['GL55-05']
            journal_record = {}
            journal_record['num'] = num
            num += 1
            journal_record['GL02'] = GL02
            journal_record['GL02-GL55'] = row['GL02-GL55']
            if len(row['GL55-03'])>0: GL55_03 = row['GL55-03']
            journal_record['GL55-03'] = (not 'GL55-GL60' in row or ''==row['GL55-GL60']) and GL55_03 or ''
            if len(row['GL55-04'])>0: GL55_04 = row['GL55-04']
            journal_record['GL55-04'] = (not 'GL55-GL60' in row or ''==row['GL55-GL60']) and GL55_04 or ''
            if len(row['GL56-02'])>0: GL56_02 = row['GL56-02']
            journal_record['GL56-02'] = (not 'GL55-GL60' in row or ''==row['GL55-GL60']) and GL56_02 or ''
            if len(row['GL69-02'])>0: GL69_02 = row['GL69-02']
            journal_record['GL69-02'] = (not 'GL55-GL60' in row or ''==row['GL55-GL60']) and GL69_02 or ''
            if len(row['GL61-01'])>0: GL61_01 = row['GL61-01']
            journal_record['GL61-01'] = (not 'GL55-GL60' in row or ''==row['GL55-GL60']) and GL61_01 or ''
            if len(row['GL61-02'])>0: GL61_02 = row['GL61-02']
            journal_record['GL61-02'] = (not 'GL55-GL60' in row or ''==row['GL55-GL60']) and GL61_02 or ''
            if len(row['GL61-03'])>0: GL61_03 = row['GL61-03']
            journal_record['GL61-03'] = (not 'GL55-GL60' in row or ''==row['GL55-GL60']) and GL61_03 or ''
            # debit
            journal_record['GL55-GL60d'] = 'debit'==debit_credit  and len(row['GL55-GL60'])>0 and row['GL55-GL60'] or ''
            journal_record['GL63-01d'] = 'debit'==debit_credit  and len(row['GL55-03'])>0 and row['GL63-01'] or ''
            journal_record['GL63-02d'] = 'debit'==debit_credit  and len(row['GL55-03'])>0 and row['GL63-02'] or ''
            journal_record['GL63-03d'] = 'debit'==debit_credit  and len(row['GL55-03'])>0 and row['GL63-03'] or ''
            journal_record['GL56-01d'] = 'debit'==debit_credit  and len(row['GL56-01'])>0 and int(row['GL56-01']) or ''
            journal_record['GL60-01d'] = 'debit'==debit_credit  and row['GL60-01'] or ''
            journal_record['GL60-02d'] = 'debit'==debit_credit  and row['GL60-02'] or ''
            journal_record['GL60-03d'] = 'debit'==debit_credit  and row['GL60-03'] or ''
            # credit
            journal_record['GL55-GL60c'] = 'credit'==debit_credit and len(row['GL55-GL60'])>0 and row['GL55-GL60'] or ''
            journal_record['GL63-01c'] = 'credit'==debit_credit and len(row['GL55-03'])>0 and row['GL63-01'] or ''
            journal_record['GL63-02c'] = 'credit'==debit_credit and len(row['GL55-03'])>0 and row['GL63-02'] or ''
            journal_record['GL63-03c'] = 'credit'==debit_credit and len(row['GL55-03'])>0 and row['GL63-03'] or ''
            journal_record['GL56-01c'] = 'credit'==debit_credit and len(row['GL56-01'])>0 and int(row['GL56-01']) or ''
            journal_record['GL60-01c'] = 'credit'==debit_credit and row['GL60-01'] or ''
            journal_record['GL60-02c'] = 'credit'==debit_credit and row['GL60-02'] or ''
            journal_record['GL60-03c'] = 'credit'==debit_credit and row['GL60-03'] or ''

            detail_records.append(journal_record)

            debit_records  = [x for x in detail_records if ''!=x['GL56-01d']]
            credit_records = [x for x in detail_records if ''!=x['GL56-01c']]
            debit_amounts  = sum([x['GL56-01d'] for x in debit_records])
            credit_amounts = sum([x['GL56-01c'] for x in credit_records])
            debit_count  = len(debit_records)
            credit_count = len(credit_records)
            if abs(debit_amounts - credit_amounts) < 2:
                j = i +1
                next_row = records[j]
                if ''!=next_row['GL55-GL60']:
                    continue                            
                deleted_GL02_GL55 = None
                if 1 == debit_count:
                    for record in detail_records:
                        if record['num']==debit_records[0]['num'] or 0==len(record['GL55-03']) or (''==record['GL56-01d'] and ''==record['GL56-01c']):
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
                        if record['num']==debit_records[0]['num']:
                            deleted_GL02_GL55 = 'GL02-GL55' in debit_records[0] and debit_records[0]['GL02-GL55'] or None
                            del detail_records[i]
                            break                            
                elif 1 == credit_count:
                    for record in detail_records:
                        if record['num']==credit_records[0]['num'] or 0==len(record['GL55-03']) or (''==record['GL56-01d'] and ''==record['GL56-01c']):
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
                        if record['num']==credit_records[0]['num']:
                            deleted_GL02_GL55 = 'GL02-GL55' in credit_records[0] and credit_records[0]['GL02-GL55'] or None
                            del detail_records[i]
                            break
                        i += 1
                if deleted_GL02_GL55:
                    target_records    = [x for x in detail_records if ''==x['GL55-GL60d'] and ''==x['GL55-GL60c']]
                    inserting_records = [x for x in detail_records + journal_records if (''!=x['GL55-GL60d'] or ''!=x['GL55-GL60c']) and deleted_GL02_GL55==x['GL02-GL55']]
                    if len(target_records)>0 and len(inserting_records)>0:
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
                        detail_records  = []
                    else:
                        journal_records += detail_records
                        detail_records  = []
                else:
                    journal_records +=  [x for x in detail_records if ''==x['GL55-GL60d'] and ''==x['GL55-GL60c']]
                    detail_records  = []

    out_records = []
    for k,v in entryDict.items():
        for record in v:
            out_record = {}
            for key in out_header:
                if key in record:
                    out_record[key] = record[key]
                else:
                    out_record[key] = ''
            out_records.append(out_record)

    sorted_out_records = sorted(out_records, key=lambda x: (x['GL02'],int(x['GL02-GL55']) if x['GL02-GL55'].isdigit() else -1, int(x['GL55-GL60d']) if x['GL55-GL60d'].isdigit() else -1, int(x['GL55-GL60c']) if x['GL55-GL60c'].isdigit() else -1))

    with open('debit_credit.csv', 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.DictWriter(file, fieldnames=out_header)
        writer.writeheader()
        for row in sorted_out_records:
            writer.writerow(row)

    print('END')

if __name__ == '__main__':
    main()
