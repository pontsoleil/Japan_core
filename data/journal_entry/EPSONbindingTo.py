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

    data_file = 'data/journal_entry/北海道産業(株).csv'
    # data_file = 'data/journal_entry/北海道産業(株).csv'
    out_file = 'data/journal_entry/北海道産業(株)_tidy.csv'

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
            if row['semSort'] != '':
                bindingDict[row[binding_header[0]]] = row

    data_header = list(EPSONcolumns.keys())
    dataList = []
    with open(data_file, mode='r', encoding='utf-8-sig') as file:
        csv_reader = csv.DictReader(file, fieldnames=data_header)
        next(csv_reader)  # 見出し行を読み飛ばす
        for row in csv_reader:
            if row['G'] != '':
                dataList.append(row)

    sorted_binding = sorted(bindingDict.values(), key=lambda x: int(x['semSort']))

    n = 1
    dimensions = {}
    elements = {}
    edges = set()
    pattern = r"^([^\[\]]+)\[([^\[\]-]+-\d+)=([^\[\]]+)\]"
    for record in dataList:
        if DEBUG: print(record)
        tidyRecord = {}
        for item in sorted_binding:
            column  = item['column']
            name    = item['name']
            semPath = item['semPath'].split('/')
            if '-'==column:
                value = n
            else:
                value = record[column]
                datatype = bindingDict[column]['datatype']
                if 'Date'==datatype and re.match(r'^(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})$',value):
                    value = f'{value[:4]}-{value[4:6]}-{value[6:]}'
            if (''==value or '0'==value):
                continue
            parent = semPath[0]
            edge   = semPath[-1]
            edges.add(edge)
            if DEBUG: print(f'{column} {semPath} {name} {value}')
            match = re.search(pattern, parent)
            if match:
                dimension = match.group(1)
                element   = match.group(2)
                condition = match.group(3)                        
                dimensions[dimension] = semanticsDict[dimension]
                elements[element]     = semanticsDict[element]
                if not parent in tidyRecord:
                    tidyRecord[parent] = {}
                if not element in tidyRecord[parent]:
                    tidyRecord[parent][element] = {}
                if not tidyRecord[parent][element]:
                    tidyRecord[parent][element] = condition
                    if DEBUG: print(f"tidyRecord[{parent}][{element}] = {condition}")
            if 1==len(semPath):
                if parent not in tidyRecord:
                    tidyRecord[parent] = {}
                tidyRecord[parent] = value
                if DEBUG: print(f"tidyRecord[{parent}] = {value}")
            elif 2==len(semPath):
                parent  = semPath[0]
                if parent not in tidyRecord:
                    tidyRecord[parent] = {}
                child = semPath[1]
                if child not in tidyRecord[parent]:
                    tidyRecord[parent][child] = {}
                match = re.search(pattern, child)
                if match:
                    dimension = match.group(1)
                    element   = match.group(2)
                    condition = match.group(3)                        
                    dimensions[dimension] = semanticsDict[dimension]
                    elements[element]     = semanticsDict[element]
                    if not tidyRecord[parent][child][element]:
                        tidyRecord[parent][child][element] = condition
                        if DEBUG: print(f"tidyRecord[{parent}][{child}][{element}] = {condition}")
                tidyRecord[parent][child] = value
                if DEBUG: print(f"tidyRecord[{parent}][{child}] = {value}")
            elif 3==len(semPath):
                parent  = semPath[0]
                if parent not in tidyRecord:
                    tidyRecord[parent] = {}
                child = semPath[1]
                if child not in tidyRecord[parent]:
                    tidyRecord[parent][child] = {}
                match = re.search(pattern, child)
                if match:
                    dimension = match.group(1)
                    element   = match.group(2)
                    condition = match.group(3)                        
                    dimensions[dimension] = semanticsDict[dimension]
                    elements[element]     = semanticsDict[element]
                    if not tidyRecord[parent][child]:
                        tidyRecord[parent][child][element] = condition
                        if DEBUG: print(f"tidyRecord[{parent}][{child}][{element}] = {condition}")
                grandchild = semPath[2]
                tidyRecord[parent][child][grandchild] = value
                if DEBUG: print(f"tidyRecord[{parent}][{child}][{grandchild}] = {value}")
            else:
                continue
        tidyData.append(tidyRecord)
        n += 1

    # 重複を削除してキー（key）の値でソート
    data = [{v['semSort']:v['semPath'].split('/')[-1]} for v in sorted_binding]
    unique_data = {}
    for item in data:
        key, value = next(iter(item.items()))
        if key not in unique_data:
            unique_data[key] = value
    sorted_data = sorted(unique_data.items(), key=lambda x: x[0])
    data_header = [item[1] for item in sorted_data]
    for element in data_header:
        elements[element] = semanticsDict[element]

    sorted_dimensions = sorted(dimensions.items(), key=lambda x: int(x[1]['semSort']))
    dimension_header = [item[1]['id'] for item in sorted_dimensions]

    sorted_elements = sorted(elements.items(), key=lambda x: int(x[1]['semSort']))
    element_header = [item[1]['id'] for item in sorted_elements]    

    def parseDict(k0, v0, parent, dims, records, n):
        record = records[-1]
        record[0] = n
        dims[0]   = n
        match = re.search(pattern, k0)
        if match:
            dimension = match.group(1)
            siblings = list(parent.keys())
            count = 0
            for sib in siblings:
                if dimension in sib:
                    count += 1
            if count > 0:
                idx1 = header.index(dimension)
                j = dims[idx1] or 0
                j += 1
                dims[idx1] = j
                record = ['']*len(header)
                records.append(record)
                for idx in range(len(dims)-1):
                    record[idx] = dims[idx]
        for k1, v1 in v0.items(): # v0 is dict
            if not isinstance(v1, dict):
                idx = header.index(k1)
                record[idx] = v1
            else: # v1 is dict
                match = re.search(pattern, k1)
                if match:
                    dimension = match.group(1)
                    siblings = list(parent.keys())
                    count = 0
                    for sib in siblings:
                        if dimension in sib:
                            count += 1
                    if count > 0:
                        idx2 = header.index(dimension)
                        j = dims[idx2] or 0
                        j += 1
                        dims[idx2] = j
                        record = ['']*len(header)
                        records.append(record)
                        for idx in range(len(dims)-1):
                            record[idx] = dims[idx]
                for k2,v2 in v1.items():
                    if not isinstance(v2, dict):
                        idx = header.index(k2)
                        record[idx] = v2
                    else: # v2 is dict
                        records = parseDict(k2, v2, v1, dims, records, n)
        return records

    header = ['GL02'] + dimension_header + element_header
    if DEBUG: print(header)

    records = []
    pattern = r"^([^\[\]]+)\[([^\[\]-]+-\d+)=([^\[\]]+)\]"
    n = 0
    # dims[0] = n
    for d in tidyData:
        dims   = ['']*(1+len(dimension_header))
        record = ['']*len(header)
        records.append(record)
        n += 1
        dims[0] = n
        records[-1][0] = n
        if not isinstance(d, dict):
            continue
        else: # d is dict
            for k, v in d.items():
                if not isinstance(v, dict):
                    idx = header.index(k)
                    record[idx] = v
                else: # v is dict
                    records = parseDict(k, v, d, dims, records, n)

    with open(f'{out_file}', 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        for row in records:
            writer.writerow(row)

    print(f'** END {data_file} to {out_file}')

if __name__=='__main__':
    main()