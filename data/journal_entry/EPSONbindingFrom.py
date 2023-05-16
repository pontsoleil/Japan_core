import csv
import re

DEBUG = False

EPSONcolumns = {
    'A':'月種別',
    'B':'種類',
    'C':'形式',
    'D':'作成方法',
    'E':'付箋',
    'F':'伝票日付',
    'G':'伝票番号',
    'H':'伝票摘要',
    'I':'枝番',
    'J':'借方部門',
    'K':'借方部門名',
    'L':'借方科目',
    'M':'借方科目名',
    'N':'借方補助',
    'O':'借方補助科目名',
    'P':'借方金額',
    'Q':'借方消費税コード',
    'R':'借方消費税業種',
    'S':'借方消費税税率',
    'T':'借方資金区分',
    'U':'借方任意項目１',
    'V':'借方任意項目２',
    'W':'貸方部門',
    'X':'貸方部門名',
    'Y':'貸方科目',
    'Z':'貸方科目名',
    'AA':'貸方補助',
    'AB':'貸方補助科目名',
    'AC':'貸方金額',
    'AD':'貸方消費税コード',
    'AE':'貸方消費税業種',
    'AF':'貸方消費税税率',
    'AG':'貸方資金区分',
    'AH':'貸方任意項目１',
    'AI':'貸方任意項目２',
    'AJ':'摘要',
    'AK':'期日',
    'AL':'証番号',
    'AM':'入力マシン',
    'AN':'入力ユーザ',
    'AO':'入力アプリ',
    'AP':'入力会社',
    'AQ':'入力日付'
}

def main():

    semantics_file   = 'data/base/adcs_semantics.csv'
    semantics_header = ['semSort','id','kind','card','level','ObjectClass','Property','Property_ja','Representation','AssociatedClass','ReferencedClass']
    binding_file     = 'data/journal_entry/EPSONbinding.csv'
    binding_header   = ['column', 'name', 'card', 'datatype', 'semSort', 'semPath', 'fixedValue']

    data_file = 'data/journal_entry/北海道産業(株)_tidy.csv'
    # data_file = 'data/journal_entry/北海道産業(株).csv'
    out_file = 'data/journal_entry/北海道産業(株)_.csv'

    tidyData = []

    semanticsDict = {}
    with open(semantics_file, mode='r', encoding='utf-8-sig') as file:
        csv_reader = csv.DictReader(file, fieldnames=semantics_header)
        next(csv_reader)  # 見出し行を読み飛ばす
        for row in csv_reader:
            semanticsDict[row['id']] = row

    bindingDict = {}
    with open(binding_file, mode='r', encoding='utf-8-sig') as file:
        csv_reader = csv.DictReader(file, fieldnames=binding_header)
        next(csv_reader)  # 見出し行を読み飛ばす
        for row in csv_reader:
            # if row['semSort'] != '':
            bindingDict[row[binding_header[0]]] = row
  
    dataList = []
    with open(data_file, mode='r', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        # 先頭行をキーとする辞書を作成
        header = next(reader)  # 先頭行を取得

    records = []
    with open(data_file, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file, fieldnames=header)
        next(reader)  # 見出し行を読み飛ばす
        for row in reader:
            records.append(row)
    
    pattern0 = r"^GL[0-9]+$"
    pattern1 = r"^GL[0-9]+-GL[0-9]+$"
    dim_header = [x for x in header if re.match(pattern0,x) or re.match(pattern1,x)]
    pattern2 = r"^GL[0-9]+-[0-9]+$"
    element_header = [x for x in header if re.match(pattern2,x)]

    selector = {}
    for item in [x['semPath'] for x in bindingDict.values() if '[' in x['semPath']]:
        founds = re.findall(r'\[([^\[\]]+)\]', item)
        pattern = r"([^\[\]-]+-\d+)=([^\[\]]+)"
        for found in founds:
            match = re.search(pattern, found)
            if match:
                check = match.group(1)
                value = match.group(2)
                if check not in selector:
                    selector[check] = set()
                selector[check].add(value)
    
    to_remove = []  # 削除する要素を一時的に保存するリスト
    for k, v in selector.items():
        if len(v) == 1:
            to_remove.append(k)  # 削除する要素をリストに追加
    # ループの後で要素を辞書から削除
    for k in to_remove:
        del selector[k]

    tidyData = {}
    for i in range(len(records)):
        record = records[i]
        dims = list(record.values())[:len(dim_header)]
        data = {}
        for k,v in record.items():
            if k in element_header:
            # if v and k in element_header:
                data[k] = v
        if dims[0]:
            if dims[1]:
                if dims[2] or dims[3]:
                    if not dims[3]:
                        dim = dim_header[2][1+dim_header[2].index('-'):]
                        for check in selector:
                            if dim in check:
                                v = record[check]
                                selector2 = f'{dim_header[2]}[{check}={v}]'
                                break
                        tidyData[selector0][selector1][selector2] = data
                        if DEBUG: print(f'tidyData[{selector0}][{selector1}][{selector2}]')
                    elif not dims[2]:
                        dim = dim_header[3][1+dim_header[3].index('-'):]
                        for check in selector:
                            if dim in check:
                                v = record[check]
                                selector2 = f'{dim_header[3]}[{check}={v}]'
                        tidyData[selector0][selector1][selector3] = data
                        if DEBUG: print(f'tidyData[{selector0}][{selector1}][{selector3}]')
                    else:
                        selector2 = f'{dim_header[2]}={dims[2]}'
                        selector3 = f'{dim_header[3]}={dims[3]}'
                        tidyData[selector0][selector1][selector2][selector3] = data
                        if DEBUG: print(f'tidyData[{selector0}][{selector1}][{selector2}][{selector3}]')
                else:
                    dim = dim_header[1][1+dim_header[1].index('-'):]
                    for check in selector:
                        condition = None
                        for k,v in record.items():
                            if v and check==k:
                                condition = f'{check}={v}'
                                if DEBUG: print(condition)
                        if dim in check:
                            v = record[check]
                            selector1 = f'{dim_header[1]}[{condition}]'
                            tidyData[selector0][selector1] = data
                            if DEBUG: print(f'tidyData[{selector0}][{selector1}]')
                        elif condition:
                            cls = check[:check.index('-')]
                            candidate = [v for k,v in selector.items() if cls in k][0]
                            if condition[1+condition.index('='):] in candidate:
                                tidyData[selector0][selector1] = {k:v for k,v in data.items() if cls not in k}
                                if DEBUG: print(f'* tidyData[{selector0}][{selector1}]')
                                selector2 = f'{[x for x in dim_header if cls in x][0]}[{condition}]'
                                tidyData[selector0][selector1][selector2] = {k:v for k,v in data.items() if cls in k}
                                if DEBUG: print(f'tidyData[{selector0}][{selector1}][{selector2}]')                    
            else:
                selector0 = f'{dim_header[0]}={dims[0]}'
                tidyData[selector0] = data
                if DEBUG: print(f'tidyData[{selector0}]')

    records = {}
    for id,record in tidyData.items():
        n = id.split('=')[1]
        records[n] = {}
        fixedValues = {k:v for k,v in bindingDict.items() if ''==v['semSort']}
        for k,v in fixedValues.items():
            records[n][k] = v['fixedValue']
        for k,binding in bindingDict.items():
            column = k
            semPath = binding['semPath']
            val = None
            if '/' not in semPath:
                if semPath in record:
                    val = record[semPath]
                    records[n][column] = val
            else:
                paths = semPath.split('/')
                if 2==len(paths):
                    if paths[0] in record:
                        if paths[1] in record[paths[0]]:
                            val = record[paths[0]][paths[1]]
                            records[n][column] = val
                elif 3==len(paths):
                    if paths[0] in record:
                        if paths[1] in record[paths[0]]:
                            if paths[2] in record[paths[0]][paths[1]]:
                                val = record[paths[0]][paths[1]][paths[2]]
                                records[n][column] = val
                        else:
                            if paths[2] in record[paths[0]]:
                                val = record[paths[0]][paths[2]]
                                records[n][column] = val
        if DEBUG: print(records[n])

    header = []
    for k,v in records.items():
        for column in v.keys():
            if column not in header:
                header.append(column)
    header.sort(key=lambda x: (len(x), x))

    rows = list(records.values())

    with open(f'{out_file}', 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.DictWriter(file,fieldnames=header)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

    print(f'** END {data_file} to {out_file}')

if __name__=='__main__':
    main()