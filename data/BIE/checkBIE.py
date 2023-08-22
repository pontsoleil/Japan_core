import csv
import json
from lxml import etree

bie = 'SMEinvoice-BIE'
bie_file = f'data/BIE/{bie}.csv'
xpath_file = f'data/BIE/{bie}1.csv'
header0 = ['seq','part','UNID','kind','C1','C2','C3','C4','C5','C6','C7','C8','C9','C10','C11','C12','term','desc','card']
header1 = ['seq','part','UNID','kind','C1','C2','C3','C4','C5','C6','C7','C8','C9','C10','C11','C12','term','desc','card','XPath']
bie1_json = f'data/BIE/{bie}_1.json'
bie2_json = f'data/BIE/{bie}_2.json'
log_file  = f'data/BIE/{bie}.log'

json_path = 'data/BIE/ABIE.json'
xsd_path  = "data/SME_Common/15JUL23XMLSchemas-D23A/uncefact/data/standard/ReusableAggregateBusinessInformationEntity_33p0.xsd"

records0 = []
records1 = []
records  = []
UNIDs    = None

def den_to_xml_element_name(den):
    name = ''
    property = den[2+den.index('.'):]
    # `. Details` で終わる場合の削除
    if den.endswith(". Details"):
        name = den.rsplit(". Details", 1)[0] + "Type"
    # ` Identification. Identifier` で終わる場合の変換
    elif property.endswith(" Identification. Identifier"):
        name = property.rsplit(" Identification. Identifier", 1)[0] + "ID"
    # `. Identifier` で終わる場合の変換
    elif property.endswith(" Identifier"):
        name = property.rsplit(" Identifier", 1)[0] + "ID"
        # `. Identifier` で終わる場合の変換
    elif property.endswith(". Text"):
        name = property.rsplit(". Text", 1)[0]
    else:
        name = property
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
        unid     = annotation.find('ccts:UniqueID', namespaces=namespace).text
        key_name = f"{unid} {den} {name}"
        if unid not in UNIDs:
            continue
        result[key_name] = []
        elements = ctype.xpath('.//xsd:element', namespaces=namespace)
        # 各子要素の情報を取得
        for elem in elements:
            elem_annotation = elem.find('xsd:annotation/xsd:documentation', namespaces=namespace)
            kind = elem_annotation.find('ccts:Acronym', namespaces=namespace).text
            unid = elem_annotation.find('ccts:UniqueID', namespaces=namespace).text
            den  = elem_annotation.find('ccts:DictionaryEntryName', namespaces=namespace).text
            name = elem.get("name")
            type = elem.get("type")
            minOccurs = elem.get("minOccurs")
            maxOccurs = elem.get("maxOccurs")
            card = elem_annotation.find('ccts:Cardinality', namespaces=namespace).text
            elem_info = {
                "kind": kind,
                "UNID": unid,
                "DEN":  den,
                "card": card,
                "name": name,
                "type": type,
                "minOccurs": minOccurs,
                "maxOccurs": maxOccurs
            }
            result[key_name].append(elem_info)
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
        records0.append(row)

root = 'SMEInvoice'
path = [root] + ['']*6
for i in range(len(records0)):
    data   = {}
    record = records0[i]
    kind = record['kind']
    data['kind'] = kind
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
        'UNID':  record['UNID'],
        'kind':  record['kind'],
        'd':     d,
        'DEN':   den,
        'name':  name,
        'card':  record['card'],
        'XPath': XPath
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
        for row in records1:
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
                key = f"{UNID} {den}"
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
            den  = recordABIE['DEN']
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

UNIDs = [x[:x.index(' ')] for x in list(result1.keys())]
abieDict = extract_complex_type_data(xsd_path)

with open(log_file, 'w') as file:
    # for key,data in result2.items():
    for key,data in result1.items():
        unid = key[:key.index(' ')]
        den = key[1+key.index(' '):]
        name = den_to_xml_element_name(den)
        key_name = f"{unid} {den} {name}"
        abie = abieDict[key_name]
        den  = key[1+key.index(' '):key.rindex(' ')]
        base_list = [x['UNID'] for x in abie]
        unid = key[:key.index(' ')]
        i = 0
        for restricted in data:
            i += 1
            children = [x[:x.index(' ')] for x in restricted]
            if not is_valid_sublist(base_list,children):
                base_list = '\n'.join(base_list)
                children  = '\n'.join(children)
                file.write(f"\n** No. {i} is wrong order.\nABIE {key}\n{base_list}\n{den}\n{children}\n")

print(f'** END {bie1_json}')