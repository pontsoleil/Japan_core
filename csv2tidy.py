import csv
import re

DEBUG = True

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

GWcolumns = {
    'A': '自会社コード',
    'B': 'ＥＤＩ対象企業コード',
    'C': '発注ＳＥＱＮＯ',
    'D': '受注担当',
    'E': '出荷先コード',
    'F': '出荷先名称　＜漢字＞',
    'G': '出荷先住所　＜漢字＞',
    'H': 'コメント ＜漢字＞',
    'I': '商品コード',
    'J': '商品名＜半角英数カナ＞',
    'K': '数量',
    'L': '単価',
    'M': '納品書番号',
    'N': '納品日',
    'O': '請求書番号',
    'P': '請求書発行日',
    'Q': '事業者登録番号',
    'R': '税額合計1',
    'S': '税率1',
    'T': '税額合計2',
    'U': '税率2',
    'V': '税込み合計金額',
    'W': '請求明細番号',
    'X': '税抜き明細金額',
    'Y': '明細行税率',
    'Z': '明細行課税区分'
}

# semantics_file   = 'data/base/ADC/adcs_semantics.csv'
# semantics_header = ['semSort','id','kind','card','level','ObjectClass','Property','Property_ja','Representation','AssociatedClass','ReferencedClass']
# binding_file     = 'data/journal_entry/EPSONbinding.csv'
# binding_header   = ['column', 'name', 'card', 'datatype', 'semSort', 'semPath', 'fixedValue']
# data_file = 'data/journal_entry/北海道産業(株)/北海道産業(株).csv'
# out_file  = 'data/journal_entry/北海道産業(株)/GL_Details.csv'

semantics_file   = 'data/base/japan-core_semantics.csv'
semantics_header = ['semSort','semPath','id','kind','level','ObjectClass','Property','Representation','AssociatedClass','ReferencedClass','n']
binding_file     = 'data/グローバルワイズ/sem-binding.csv'
binding_header   = ['column', 'name', 'card', 'datatype', 'semSort', 'semPath', 'value', 'term']

data_file        = 'data/グローバルワイズ/invoice.csv'
out_file         = 'data/グローバルワイズ/tidy.csv'

tidyData         = []
semanticsDict    = {}
header           = None

def determine_type(value):
    if isinstance(value, (int, float, str, bool, bytes, complex)):
        return 'atomic'
    elif isinstance(value, dict):
        return 'dict'
    elif isinstance(value, list):
        return 'list'
    else:
        return 'unknown'
    
def notEmptyRecord(record):
    global dataLine
    Empty = True
    for k in dataLine.keys():
        if record[k] and len(record[k]) > 0:
            Empty = False
            break
    return not Empty

def isEmptyRecord(record):
    global dataLine
    Empty = True
    for k in dataLine.keys():
        if record[k] and len(record[k]) > 0:
            Empty = False
            break
    return not Empty

def setRecord(element, value):
    global dimLevel
    global dimLine
    global dataLine
    global record
    for d_k,d_v in dimLine.items():
        if d_k not in record or d_v!=record[d_k]:
            record[d_k] = d_v
    record[element] = value
    dataLine.add(element)

def atomicProcess(d, path):
    global dimLevel
    global dimLine
    global dataLine
    global record
    global records
    element = path.strip('/').split('/')[-1]
    value   = d
    setRecord(element,value)

def listProcess(d, path):
    global dimLevel
    global dimLine
    global dataLine
    global record
    global records
    for sub in d:
        if len(records)>0:
            print(records[-1])
        dim     = path.strip('/').split('/')[-1]
        dim     = re.sub(r'\[\d+\]$', '', dim)
        changed = False
        dLevel  = -1      
        record  = {}
        records.append(record)
        for d in dimLine.keys():
            if d==dim:
                dimLine[d] += 1
                count       = dimLine[d]
                dLevel      = dimLevel[d]
                changed     = True
        for d in dimLine.keys():
            if changed and dimLevel[d]>=dLevel and dim!=d:
                dimLine[d] = 0
        for d in dimLine.keys():
            record[d] = dimLine[d]
        # print(f'- listProcess dimLine:{dimLine}')
        path   = re.sub(r'\[\d+\]/$', '/', path)
        path   = f'{path[:-1]}[{count}]/'
        flatten_dict(sub, path)

def dictProcess(d, path):
    global dimLevel
    global dimLine
    global dataLine
    global record
    global records
    for k, v in d.items():
        if 'atomic'==determine_type(v):
            path += f'{k}/'
            atomicProcess(v, path)
    for k, v in d.items():
        if 'dict'==determine_type(v):
            path += f'{k}/'
            flatten_dict(v, path)
    for k, v in d.items():
        if 'list'==determine_type(v):
            path += f'{k}/'
            listProcess(v, path)

def flatten_dict(d, path='/'):
    global dimLevel
    global dimLine
    global dataLine
    global record
    global records
    if 'atomic'==determine_type(d):
        atomicProcess(d, path)
    elif 'dict'==determine_type(d):
        dictProcess(d, path)
    elif 'list'==determine_type(d):
        listProcess(d, path)

def dict_to_csv(data, filename):
    global dimLevel
    global dimLine
    global dataLine
    """Converts a flattened dictionary to CSV."""
    flatten_dict(data)
    header = list(dimLine.keys()) + sorted(dataLine)
    with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        for record in records:
            writer.writerow(record)

def setPathValue(data, query):
    def find_node_by_condition(test_node, condition_key, condition_value):
        if isinstance(test_node,list):
            keys = condition_key.split('/')
            for sub_node in test_node:
                current_node = sub_node
                for key in keys[:-1]:
                    if key in current_node:
                        current_node = current_node[key]
                    else:
                        break
                if condition_value==current_node[keys[-1]]:
                    return sub_node
            return None

    def find_or_create_node_with_condition(test_node, condition_key, condition_value):
        keys = condition_key.split('/')
        if isinstance(test_node,dict):
            current_node = test_node
            found        = True
            for key in keys:
                if isinstance(current_node, dict) and key in current_node:
                    found_node   = current_node
                    current_node = current_node[key]
                elif isinstance(current_node, list):
                    for checking_node in current_node:
                        found_node = find_or_create_node_with_condition(checking_node, condition_key, condition_value)
                        return found_node
                else:
                    found = False
                    break
            if found and current_node == condition_value:
                return test_node
            new_node     = {}
            current_node = new_node
            for key in keys[:-1]:
                current_node[key] = {}
                current_node      = current_node[key]
            current_node[keys[-1]] = condition_value
            test_node[keys[-1]]    = condition_value
            return test_node
        elif isinstance(test_node,list):
            if 0==len(test_node):
                new_node     = {}
                current_node = new_node
                for key in keys[:-1]:
                    current_node[key] = {}
                    current_node      = current_node[key]
                current_node[keys[-1]] = condition_value
                test_node.append(new_node)
                return test_node
            else:
                for sub_node in test_node:
                    current_node = sub_node
                    found = True
                    for key in keys[:-1]:
                        if isinstance(current_node, dict) and key in current_node:
                            current_node = current_node[key]
                        else:
                            found = False
                            break
                    if found and condition_value==current_node[keys[-1]]:
                        return test_node
                new_node = {}
                current_node = new_node
                for key in keys[:-1]:
                    current_node[key] = {}
                    current_node = current_node[key]
                current_node[keys[-1]] = condition_value
                if 1==len(keys):
                    target_node = [x for x in test_node if condition_value == x[keys[0]]]
                elif 2==len(keys):
                    target_node = [x for x in test_node if condition_value == x.get(keys[0]).get(keys[1])]
                if not target_node or 0 == len(target_node):
                    test_node.append(new_node)
                else:
                    test_node = target_node
                return test_node

    def lookup(node, query_elements):
        if not query_elements:
            return
        first, *rest = query_elements
        if "[" in first and "]" in first:
            key, conditions = re.split(r'\[|\]', first)[:2]
            conditions = conditions.split('and')
            conditions = [condition.strip() for condition in conditions]
            if 1==len(conditions):
                condition = conditions[0]
                condition_key, condition_value = condition.split("=")
                condition_key   = condition_key.strip()
                condition_value = condition_value.strip("'")
                if isinstance(node, dict):
                    if key not in node:
                        node[key] = []
                    existing_node = find_or_create_node_with_condition(node[key], condition_key, condition_value)
                    return lookup(existing_node, rest)
                elif isinstance(node, list):
                    existing_node = find_or_create_node_with_condition(node, condition_key, condition_value)
                    found_node    = find_node_by_condition(node, condition_key, condition_value)
                    return lookup(found_node, rest)
            elif 2==len(conditions) and isinstance(node, list):
                condition_key0, condition_value0 = conditions[0].split("=")
                condition_key0   = condition_key0.strip()
                condition_value0 = condition_value0.strip("' ")
                selected_node    = find_node_by_condition(node, condition_key0, condition_value0)
                condition_key1, condition_value1 = conditions[1].split("=")
                condition_key1   = condition_key1.strip()
                condition_value1 = condition_value1.strip("' ")
                current_node     = selected_node
                keys1 = condition_key1.split('/') # パスを'/'で分割
                for key in keys1[:-1]:
                    if key not in current_node:
                        current_node[key] = {}
                    current_node = current_node[key]
                current_node[keys1[-1]] = condition_value1
                return lookup(selected_node, rest)
        elif isinstance(node, dict):
            if first not in node:
                if '=' in first:
                    k, v = first.split("=", 1)
                    node[k] = v.strip("' ")
                    return
                elif rest and '[' in rest[0]:
                    node[first] = []
                else:
                    node[first] = {}
            return lookup(node[first], rest)
        elif isinstance(node, list):
            for sub_node in node:
                return lookup(sub_node, query_elements)

    def transform_conditions(element):
        conditions = re.findall(r"\[(.*?)\]", element) # 角括弧内の内容を抽出
        if len(conditions) > 1:
            new_conditions = ' and '.join(conditions) # 複数の条件を 'and' で結合
            return f"[{new_conditions}]"
        return element

    def compare_key_value_pairs(pair1, pair2):
        key1, value1 = pair1.split("=")
        key2, value2 = pair2.split("=")
        if key1 != key2:
            return False  # Keys must match for the pairs to be considered equal
        try:
            value1 = int(value1.strip("'"))
        except ValueError:
            value1 = value1.strip("'")  # Remove single quotes if present, else leave as is
        try:
            value2 = int(value2.strip("'"))
        except ValueError:
            value2 = value2.strip("'")  # Remove single quotes if present, else leave as is
        return value1 == value2

    def combine_conditions(element_list):
        combined = []
        last_condition_prefix = None

        for element in element_list:
            condition_match = re.search(r"\[([_\w]+)_\d+=['\w]+", element) or re.search(r"([_\w]+)_\d+=['\w]+", element)
            if condition_match:
                condition_prefix = condition_match.group(1)
                if condition_prefix == last_condition_prefix:
                    pair1 = combined[-1][1:-1]
                    if '['==element[0]:
                        pair2 = element[1:-1]
                    else:
                        pair2 = element
                    if not compare_key_value_pairs(pair1, pair2):
                        combined[-1] = f"[{pair1} and {pair2}]"
                    else:
                        continue
                else:
                    combined.append(element)
                last_condition_prefix = condition_prefix
            else:
                combined.append(element)
                last_condition_prefix = None

        return combined

    def split_elements(query):
        elements = re.findall(r"(\[[^\]]+\]|[^/\[\]=]+=[^/\[\]=]+|\w+)", query.strip("/"))
        return combine_conditions(elements)

    elements = split_elements(query)
    elements = [transform_conditions(e) for e in elements]
    lookup(data, elements)

def main():
    global dimLevel
    global dimLine
    global dataLine
    global record
    global records

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
            if row['column'] != '':
                bindingDict[row[binding_header[0]]] = row

    # CSVcolumns = EPSONcolumns
    # CSVcolumns = GWcolumns
    CSVcolumnNames = [{x['column']:x['name']} for k,x in bindingDict.items() if 'd'!=k[0]]
    CSVcolumns = {}
    for d in CSVcolumnNames:
        CSVcolumns.update(d)
    data_header = list(CSVcolumns.keys())

    sorted_binding = sorted(bindingDict.values(), key=lambda x: int(x['semSort']))

    dataList = []
    with open(data_file, mode='r', encoding='utf-8-sig') as file:
        csv_reader = csv.DictReader(file, fieldnames=data_header)
        next(csv_reader)  # 見出し行を読み飛ばす
        for row in csv_reader:
            if row['A'] != '':
                dataList.append(row)

    dimension  = {}
    elements   = {}
    line       = -1
    tidyDict   = {}
    for record in dataList:
        line += 1
        # print(f'** line: {line}')
        for item in sorted_binding:
            column   = item['column']
            datatype = item['datatype']
            semPath  = item['semPath']
            value    = item['value']
            if 'd'==column[:1]:
                columns   = column.split(',')
                if 1==len(columns):
                    columnValue = record[column[1:]]
                    pathElements = []
                    elements = re.findall(r"(\w+)", semPath.strip("/"))
                    for element in elements:
                        if element in dimension:
                            if '*' in value and element==elements[-1]:
                                path = f"{element}{value.replace('*',columnValue)}"
                                dimension[element] = path
                            e = dimension[element]
                            pathElements.append(e)
                        elif '*' in value:
                            path = f"{element}{value.replace('*',columnValue)}"
                            dimension[element] = path
                            pathElements.append(path)
                        else:
                            pathElements.append(element)
                    p = '/' + '/'.join(pathElements)
                    # print(p)
                    setPathValue(tidyDict, p)
                else:
                    elements = re.findall(r"(\w+)", semPath.strip("/"))
                    values   = value.split(' ')
                    for i in range(len(values)):
                        pathElements = []
                        for element in elements:
                            if element in dimension:
                                element = dimension[element]
                                pathElements.append(element)
                            elif '*' in value:
                                path = f"{element}{value.replace('*',columnValue)}"
                                dimension[element] = path
                                pathElements.append(path)
                            else:
                                pathElements.append(f"{element}{values[i]}")
                        p = '/' + '/'.join(pathElements)
                        # print(p)
                        setPathValue(tidyDict, p)
            else: # element
                # if 'A'==column:
                #     print(f'-- dimension: {dimension}')
                columnValue = record[column]
                columnValue = re.sub('\s+',' ',columnValue)
                columnValue = columnValue.strip('\s')
                pathElements = []
                elements = re.findall(r"(['=\[\]\w]+)", semPath.strip("/"))
                for element in elements:
                    if element in dimension:
                        element = dimension[element]
                        pathElements.append(element)
                    else:
                        pathElements.append(element)
                path = '/' + '/'.join(pathElements)
                if 'Date'==datatype and re.match(r'^\d{8}$',columnValue):
                    columnValue = f"{columnValue[0:4]}-{columnValue[4:6]}-{columnValue[6:8]}"
                if datatype in ['Amount','Unit Price Amount','Quantity','Integer','Numeric']:
                    path = f"{path}={columnValue}"
                else:
                    path = f"{path}='{columnValue}'"
                setPathValue(tidyDict, path)

    dimData = [{x['semPath'].split('/')[-1]:len(x['semPath'].split('/'))-2} for k,x in bindingDict.items() if 'd'==k[0]]
    dimLevel = {}
    for d in dimData:
        dimLevel.update(d)
    dimLine = {}
    for k in dimLevel.keys():
        dimLine.update({k:0})
    dataLine = set()
    record   = {}
    records  = []

    dict_to_csv(tidyDict, out_file)
    
    print(f'** END converted {data_file} to {out_file}')

if __name__=='__main__':
    main()