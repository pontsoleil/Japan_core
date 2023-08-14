import csv

bie_file = 'data/base/BIE.csv'
header = ['UNID', 'kind', 'C1', 'C2', 'C3', 'C4', 'C5',
           'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12', 'card']

records0 = []
records  = []

def search_for_corresponding_BIE(start_index, current_d):
    global records
    names = []
    for j in range(start_index, len(records)):
        record = records[j]
        UNID = record['UNID']
        kind = record['kind']
        card = record['card']
        name = record['name']
        # 次の 'ABIE' のレコードに達したら探索を終了する
        if kind in ['ASMA','ABIE'] and record['d'] == current_d:
            break
        # 対応する 'BIE' が見つかったら名前を追加する
        elif kind == 'BBIE' and record['d'] == 1 + current_d:
            names.append({'UNID':UNID,'name':name,'card':card})
    return names

with open(bie_file, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f, fieldnames=header)
    next(reader)
    next(reader)
    records = []
    for row in reader:
        if 'END' == row['kind']:
            break
        records0.append(row)

for i in range(len(records0)):
    data   = {}
    record = records0[i]
    data['kind'] = record['kind']
    if len(record['C1']) > 0:
        d = 1
        name = record['C1']
    if len(record['C2']) > 0:
        d = 2
        name = record['C2']
    if len(record['C3']) > 0:
        d = 3
        name = record['C3']
    if len(record['C4']) > 0:
        d = 4
        name = record['C4']
    if len(record['C5']) > 0:
        d = 5
        name = record['C5']
    if len(record['C6']) > 0:
        d = 6
        name = record['C6']
    if len(record['C7']) > 0:
        d = 7
        name = record['C7']
    if len(record['C8']) > 0:
        d = 8
        name = record['C8']
    if len(record['C9']) > 0:
        d = 9
        name = record['C9']
    if len(record['C10']) > 0:
        d = 10
        name = record['C10']
    if len(record['C11']) > 0:
        d = 11
        name = record['C11']
    if len(record['C12']) > 0:
        d = 12
        name = record['C12']
    data['UNID'] = record['UNID']
    data['d'] = d
    data['name'] = name
    data['card'] = record['card']
    records.append(data)

# 指定した d 値の ABIE のみを対象として処理
result = {}
for d_value in [1,3,5,7,9,11]:
    for i in range(len(records)):
        recordABIE = records[i]
        kind = recordABIE['kind']
        d = recordABIE['d']
        if kind in ['ASMA','ABIE'] and d == d_value:
            name  = recordABIE['name']
            start_index = i+1
            names = search_for_corresponding_BIE(start_index, d_value)
            if names:
                if name in result:
                    result[name].append(names)
                else:
                    result[name] = [names]

print(result)  # 出力: {'A': [['B'], ['G']], 'D': [['E']]}

# if __name__ == '__main__':
#     main()