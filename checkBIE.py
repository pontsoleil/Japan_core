import csv
import json
from lxml import etree

# bie = 'SMEinvoice-BIE'
bie = 'core_compare'
bie_file = f'data/BIE/{bie}.csv'
xpath_file = f'data/BIE/{bie}1.csv'
header0 = ['seq','part','UNID','kind','C1','C2','C3','C4','C5','C6','C7','C8','C9','C10','C11','C12','term','desc','card','n','code','num','level']
header1 = ['seq','part','UNID','kind','C1','C2','C3','C4','C5','C6','C7','C8','C9','C10','C11','C12','term','desc','card','n','code','num','level','XPath','d1','d2','d3','d4','SemPath']
bie1_json = f'data/BIE/{bie}_1.json'
bie2_json = f'data/BIE/{bie}_2.json'
log_file  = f'data/BIE/{bie}.log'

json_path = 'data/BIE/ABIE.json'
xsd_path  = "data/SME_Common/15JUL23XMLSchemas-D23A/uncefact/data/standard/ReusableAggregateBusinessInformationEntity_33p0.xsd"

records0  = []
records1  = []
records   = []
UNIDs     = None
abieDict  = {}
abieLabel = {}
abieNum   = {}

def den_to_xml_element_name(den):
    name = ''
    # property = den[2+den.index('.'):]
    # `. Details` で終わる場合の削除
    if den.endswith(". Details"):
        name = den.rsplit(". Details", 1)[0] + "Type"
    # ` Identification. Identifier` で終わる場合の変換
    elif den.endswith("Identification. Identifier"):
        name = den.rsplit("Identification. Identifier", 1)[0] + "ID"
    # `. Identifier` で終わる場合の変換
    elif den.endswith(" Identifier"):
        name = den.rsplit(" Identifier", 1)[0] + "ID"
        # `. Identifier` で終わる場合の変換
    elif den.endswith(". Text"):
        name = den.rsplit(". Text", 1)[0]
    # else:
    #     name = property
    # スペース、アンダースコア、ピリオドを削除して単語に分割
    words = name.replace("_", " ").replace(".", "").split()    
    # 各単語の最初の文字を大文字に変換
    camel_case_name = ''.join(words)
    return camel_case_name

def search_for_corresponding_BIE(start_index, current_d):
    global records
    data = []
    for j in range(start_index, len(records)):
        record = records[j]
        UNID   = record['UNID']
        kind   = record['kind']
        den    = record['DEN']
        name   = record['name']
        card   = record['card']
        XPath  = record['XPath']
        # 次の 'ABIE' のレコードに達したら探索を終了する
        if kind in ['ASMA','ABIE'] and record['d'] == current_d:
            break
        # 対応する 'BIE' が見つかったら名前を追加する
        elif kind in ['BBIE','ASBIE'] and record['d'] == 1 + current_d:
            data.append({
                'UNID':  UNID,
                'kind':  kind,
                'DEN':   den,
                'name':  name,
                'card':  card,
                'XPath': XPath
            })
    return data

def extract_complex_type_data(xsd_content):
    # tree = etree.fromstring(xsd_content)
    tree = etree.parse(xsd_path)
    namespace = {
        'xsd': 'http://www.w3.org/2001/XMLSchema',
        'ccts': 'urn:un:unece:uncefact:documentation:standard:CoreComponentsTechnicalSpecification:2'  # この名前空間URIを正確なものに置き換えてください
    }
    complex_types = tree.xpath('//xsd:complexType', namespaces=namespace)
    result = {}
    for ctype in complex_types:
        name = ctype.get("name")
        annotation = ctype.find('xsd:annotation/xsd:documentation', namespaces=namespace)
        # ComplexTypeの主要な情報を取得
        den      = annotation.find('ccts:DictionaryEntryName', namespaces=namespace).text
        unidABIE = annotation.find('ccts:UniqueID', namespaces=namespace).text
        key_name = f"{unidABIE} {den} {name}"
        abieLabel[unidABIE] = key_name
        if unidABIE not in UNIDs:
            continue
        if unidABIE not in abieNum:
            abieNum[unidABIE] = {}
        result[unidABIE] = []
        elements = ctype.xpath('.//xsd:element', namespaces=namespace)
        # 各子要素の情報を取得
        num = 0
        for elem in elements:
            elem_annotation = elem.find('xsd:annotation/xsd:documentation', namespaces=namespace)
            kind      = elem_annotation.find('ccts:Acronym', namespaces=namespace).text
            unidBBIE  = elem_annotation.find('ccts:UniqueID', namespaces=namespace).text
            den       = elem_annotation.find('ccts:DictionaryEntryName', namespaces=namespace).text
            name      = elem.get("name")
            type      = elem.get("type")
            minOccurs = elem.get("minOccurs")
            maxOccurs = elem.get("maxOccurs")
            card = elem_annotation.find('ccts:Cardinality', namespaces=namespace).text
            num += 1
            abieNum[unidABIE][unidBBIE] = num
            BBIEinfo = {
                "kind": kind,
                "UNID": unidBBIE,
                "DEN":  den,
                "card": card,
                "name": name,
                "type": type,
                "minOccurs": minOccurs,
                "maxOccurs": maxOccurs
            }
            result[unidABIE].append(BBIEinfo)
    return result

def is_valid_sublist(original, sublist):
    """
    Check if the sublist is a valid partial selection from the original list 
    while maintaining the order.
    """
    # 現在の位置を追跡するための変数
    current_index = 0
    # 部分リストの各要素に対して
    for item in sublist:
        # 要素が元のリストに存在する場合、その位置を取得
        if 'JP'==item[:2]:
            continue
        try:
            index = original.index(item, current_index)
            current_index = index + 1
        except ValueError:
            # 要素が元のリストに存在しない場合、部分リストは無効
            return False
    # すべての要素が正しい順序で存在する場合、部分リストは有効
    return True

with open(bie_file, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f, fieldnames=header0)
    next(reader)
    next(reader)
    records = []
    for row in reader:
        if 'END' == row['kind']:
            break
        record = {}
        for k,v in row.items():
            if k in header0:
                record[k] = v
        records0.append(record)

UNIDs = list(set([x['UNID'] for x in records0]))
abieDict = extract_complex_type_data(xsd_path)

root = 'SMEInvoice'
unidABIE = None
path = [root] + ['']*6
for i in range(len(records0)):
    data   = {}
    record = records0[i]
    unid = record['UNID']
    kind = record['kind']
    data['kind'] = kind
    if 'ABIE'==kind:
        unidABIE = unid
    if 'BBIE'==kind and  unidABIE and unidABIE in abieNum:
        if unid in abieNum[unidABIE]:
            num = abieNum[unidABIE][unid]
        else:
            print(f"** {unid} NOT in abieNum[{unidABIE}]")
            num = ''
    else:
        num = record['num']
    den = ''
    level = None
    if len(record['C1']) > 0:
        d = 1
        level = 1
        den = record['C1']
    if len(record['C2']) > 0:
        d = 2
        level = 2
        den = record['C2']
    if len(record['C3']) > 0:
        d = 3
        den = record['C3']
    if len(record['C4']) > 0:
        d = 4
        level = 3
        den = record['C4']
    if len(record['C5']) > 0:
        d = 5
        den = record['C5']
    if len(record['C6']) > 0:
        d = 6
        level = 4
        den = record['C6']
    if len(record['C7']) > 0:
        d = 7
        den = record['C7']
    if len(record['C8']) > 0:
        d = 8
        level = 5
        den = record['C8']
    if len(record['C9']) > 0:
        d = 9
        den = record['C9']
    if len(record['C10']) > 0:
        d = 10
        level = 6
        den = record['C10']
    if len(record['C11']) > 0:
        d = 11
        den = record['C11']
    if len(record['C12']) > 0:
        d = 12
        level = 7
        den = record['C12']
    den  = den.replace('\n', '').strip('\u3000 ')
    name = den_to_xml_element_name(den)
    XPath = ''
    if level!=None:
        if 1==level:
            name = name[:-4]
            path[1] = name
            XPath = '/ '+path[0]+'/ '+path[1]
        elif level > 1:
            path[level] = name
            i = level + 1
            while i < 6:
                path[i] = ''
                i += 1
            XPath = '/ '+path[0]
            i = 1
            while i <= level:
                XPath += '/ '+path[i]
                i += 1        

    data = {
        'UNID':  unid,
        'kind':  record['kind'],
        'd':     d,
        'DEN':   den,
        'name':  name,
        'card':  record['card'],
        'XPath': XPath,
        'term': record['term'],
        'desc': record['desc'],
        'n': record['n'],
        'code': record['code'],
        'num': num
    }
    records.append(data)

    record['XPath'] = XPath
    records1.append(record)

# CSVファイルを書き込みモードで開く
with open(xpath_file, "w", encoding='utf-8-sig', newline='') as csvfile:
    # DictWriterオブジェクトの作成
    writer = csv.DictWriter(csvfile, fieldnames=header1)
    # ヘッダーの書き込み
    writer.writeheader()
    # 各行を書き込む
    ds = ['JC00','','','','']
    nums = list(set([x['UNID'] for x in records0 if 'BBIE'!=x['kind']]))
    for row in records1:
        code = row['code']
        if code:
            unid = f"UN010{code}"
            num = ''
            if unid in nums:
                num = nums.index(unid)
            else:
                unid = f"JPS23{code}"
                if unid in nums:
                    num = nums.index(unid)
            if num:
                hexNum = hex(num)[2:]
                if 1==len(hexNum):
                    code = f'JC0{hexNum}'
                else:
                    code = f'JC{hexNum}'
            else:
                print(f'** {code} NOT in nums.')
            num = row['num']
            if num:
                num = format(int(row['num']), '02x')
                row['code'] = f"{code}-{num}"
            elif row['XPath']:
                row['code'] = code
            else:
                row['code'] = ''
        if row['level']:
            n = row['level']
            i = int(n)
            j = 1
            ds[i] = code
            idx = i+1
            while idx > i and idx <= 4:
                ds[idx] = ''
                idx += 1
        if 'ABIE'!=row['kind']:
            idx = 1
            while idx <= 4:
                row['d'+str(idx)] = ds[idx]
                idx += 1
        row['SemPath'] = ds[0]+(ds[1] and f'-{ds[1]}')+(ds[2] and f'-{ds[2]}')+(ds[3] and f'-{ds[3]}')+(ds[4] and f'-{ds[4]}')+f'-{code}'
        writer.writerow(row)

# 指定した d 値の ABIE のみを対象として処理
result1 = {}
for d_value in [1,3,5,7,9,11]:
    for i in range(len(records)):
        recordABIE = records[i]
        kind = recordABIE['kind']
        d = recordABIE['d']
        if kind in ['ASMA','ABIE'] and d == d_value:
            UNID  = recordABIE['UNID']
            den   = recordABIE['DEN']
            name  = recordABIE['name']
            XPath = recordABIE['XPath']
            start_index = i+1
            data = search_for_corresponding_BIE(start_index, d_value)
            if data:
                key  = f"{UNID} {den}"
                data = [f"{x['UNID']} {x['kind']} {x['card']} {x['DEN']} {x['XPath']}"  for x in data]
                if key in result1:
                    result1[key].append(data)
                else:
                    result1[key] = [data]

# JSON ファイルとして書き出し
with open(bie1_json, 'w') as json_file:
    json.dump(result1, json_file, indent=4)

# 指定した d 値の ABIE のみを対象として処理
result2 = {}
for d_value in [1,3,5,7,9,11]:
    for i in range(len(records)):
        recordABIE = records[i]
        kind = recordABIE['kind']
        d = recordABIE['d']
        if kind in ['ASMA','ABIE'] and d == d_value:
            UNID  = recordABIE['UNID']
            den   = recordABIE['DEN']
            name  = recordABIE['name']
            start_index = i+1
            data = search_for_corresponding_BIE(start_index, d_value)
            if data:
                key = f"{UNID} {den} {name}"
                if key in result2:
                    result2[key].append(data)
                else:
                    result2[key] = [data]

# JSON ファイルとして書き出し
with open(bie2_json, 'w') as json_file:
    json.dump(result2, json_file, indent=4)

with open(log_file, 'w') as file:
    # for key,data in result2.items():
    for key,data in result1.items():
        unid      = key[:key.index(' ')]
        den       = key[1+key.index(' '):]
        name      = den_to_xml_element_name(den)
        # key_name = f"{unid} {den} {name}"
        abie      = abieDict[unid]
        den       = key[1+key.index(' '):key.rindex(' ')]
        base_list = [x['UNID'] for x in abie]
        unid      = key[:key.index(' ')]
        i = 0
        for restricted in data:
            i += 1
            children = [x[:x.index(' ')] for x in restricted]
            if not is_valid_sublist(base_list,children):
                base_list = '\n'.join(base_list)
                children  = '\n'.join(children)
                file.write(f"\n** No. {i} is wrong order.\nABIE {key}\n{base_list}\n{den}\n{children}\n")

print(f'** END {bie1_json}')