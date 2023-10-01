#!/usr/bin/env python3
# coding: utf-8
#
# generate CSV fron UN/CEFACT ram schema file
#
# designed by SAMBUICHI, Nobuyuki (Sambuichi Professional Engineers Office)
# written by SAMBUICHI, Nobuyuki (Sambuichi Professional Engineers Office)
#
# MIT License
#
# (c) 2022 SAMBUICHI Nobuyuki (Sambuichi Professional Engineers Office)
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
from xml.etree import ElementTree as ET

# XMLスキーマファイルのパス
xml_file = 'data/SME_Common/15JUL23XMLSchemas-D23A/uncefact/data/standard/ReusableAggregateBusinessInformationEntity_33p0.xsd'

UNIDs = set(['UN01005480', 'UN01014895', 'UN01005876', 'UN01005917', 'UN01005478', 'UN01003138', 'UN01005428', 'UN01015593', 'UN01014643', 'UN01006002', 'UN01005784', 'UN01006005', 'UN01005679', 'UN01005694', 'UN01015592', 'UN01005720', 'UN01005950', 'UN01005738', 'UN01005875', 'UN01005994', 'UN01005997', 'UN01005562', 'UN01005741', 'UN01011457', 'UN01005762', 'UN01012746', 'UN01008451', 'UN01014639', 'UN01005945', 'UN01005817', 'UN01005909', 'UN01005484', 'UN01005936', 'UN01011456', 'UN01004493', 'UN01005924', 'UN01005925', 'UN01008502', 'UN01000372', 'UN01005944', 'UN01015534', 'UN01005487', 'UN01006039', 'UN01005761', 'UN01005998', 'UN01005953', 'UN01005557', 'UN01014647', 'UN01009647', 'UN01009650', 'UN01005765', 'UN01009660', 'UN01005488', 'UN01006080', 'UN01005814', 'UN01005836', 'UN01006004', 'UN01005943', 'UN01000371', 'UN01015590', 'UN01005721', 'UN01009653', 'UN01006021', 'UN01005812', 'UN01005479', 'UN01005996', 'UN01014642', 'UN01005706', 'UN01014637', 'UN01005833', 'UN01005689', 'UN01005880', 'UN01005842', 'UN01006006', 'UN01005869', 'UN01009669', 'JPS2300021', 'UN01011516', 'UN01014897', 'UN01005913', 'UN01005811', 'UN01005483', 'UN01009651', 'UN01005700', 'UN01005574', 'UN01005957', 'UN01005402', 'UN01005715', 'UN01013096', 'UN01005960', 'UN01014641', 'UN01005968', 'UN01005813', 'UN01006003', 'UN01005718', 'UN01005780', 'UN01005475', 'UN01005779', 'UN01015490', 'UN01005989', 'UN01005586', 'UN01006009', 'UN01011519', 'UN01005729', 'UN01009648', 'UN01005759', 'UN01013318', 'UN01009664', 'UN01005573', 'UN01005783', 'UN01005426', 'UN01004497', 'UN01009649', 'UN01014644', 'UN01005758', 'UN01005558', 'UN01005680', 'UN01009661', 'UN01015492', 'UN01009672', 'UN01006014', 'UN01008455', 'UN01013091', 'UN01005919', 'UN01015539', 'UN01005963', 'UN01005834', 'UN01014894', 'UN01009655', 'UN01013039', 'UN01008533', 'UN01005878', 'UN01005719', 'UN01003139', 'UN01014899', 'UN01006040', 'UN01005931', 'UN01005815', 'UN01005739', 'UN01005716', 'UN01008457', 'UN01005857', 'UN01008286', 'UN01005791', 'UN01005954', 'UN01009654', 'UN01005939', 'UN01008456', 'UN01005940', 'UN01012702', 'UN01013040', 'UN01005398', 'UN01005832', 'UN01009671', 'UN01005860', 'UN01005929', 'UN01012127', 'UN01014649', 'UN01015596', 'UN01015504', 'UN01005915', 'UN01005628', 'UN01005713', 'UN01005730', 'UN01005580', 'UN01005489', 'UN01005756', 'UN01005861', 'UN01005725', 'UN01005879', 'UN01004496', 'UN01005745', 'UN01005941', 'UN01005790', 'UN01005839', 'UN01005916', 'UN01005401', 'UN01005588', 'UN01005581', 'UN01005991', 'UN01005567', 'UN01005922', 'UN01005473', 'UN01006019', 'UN01005921', 'UN01007174', 'UN01005863', 'UN01005923', 'UN01006026', 'UN01005841', 'UN01005850', 'UN01005474', 'UN01005670', 'UN01005948', 'UN01005980', 'UN01005793', 'UN01005585', 'UN01010016', 'UN01005862', 'UN01009659', 'UN01005864', 'UN01005471', 'UN01005560', 'UN01005726', 'UN01011455', 'UN01005683', 'UN01005821', 'UN01005735', 'UN01005579', 'UN01005693', 'UN01015493', 'UN01005626', 'UN01009658', 'UN01005914', 'UN01005710', 'UN01000374', 'UN01005570', 'UN01005472', 'UN01005490', 'UN01005486', 'UN01006011', 'UN01006015', 'UN01015591', 'UN01005736', 'UN01005481', 'UN01006008', 'UN01006020', 'UN01005937', 'UN01005757', 'UN01009966', 'UN01005692', 'UN01005859', 'UN01005608', 'UN01008445', 'UN01006415', 'UN01005930', 'UN01005865', 'UN01005918', 'UN01005744', 'UN01005946', 'UN01014645', 'UN01005687', 'UN01009662', 'UN01005612', 'UN01005400', 'UN01006057', 'UN01005988', 'UN01005707', 'UN01005685', 'UN01005476', 'UN01005874', 'UN01015533', 'UN01005992', 'UN01003140', 'UN01005809', 'UN01011521', 'UN01005986', 'UN01005827', 'UN01005958', 'UN01005792', 'UN01005858', 'UN01004495', 'UN01005961', 'UN01012925', 'UN01005613', 'UN01014636', 'UN01005677', 'UN01005714', 'UN01009656', 'UN01005810', 'UN01005823', 'UN01014650', 'UN01009665', 'UN01005990', 'UN01005582', 'UN01005672'])
# XMLファイルをパース
tree = ET.parse(xml_file)
root = tree.getroot()

# # 名前空間マップを取得
# namespaces = root.nsmap  # If this line doesn't work, you might need to extract the namespaces differently.
# XMLの名前空間を定義
namespaces = {
    'xsd': 'http://www.w3.org/2001/XMLSchema',
    'ccts': "urn:un:unece:uncefact:documentation:standard:CoreComponentsTechnicalSpecification:2" 
}
# CSVファイルに書き込むデータを格納するリスト
data_to_write = []
csv_columns = ['UniqueID', 'Acronym', 'name', 'type', 'DictionaryEntryName', 'Definition']

# 各エレメントとコンプレックスタイプを処理
elements0 = root.findall('.//xsd:element', namespaces)
elements1 = root.findall('.//xsd:complexType', namespaces)
elements = elements0 + elements1
for elem in elements:
    data = {}
    data['name'] = elem.get('name')
    data['type'] = elem.get('type') if elem.tag.endswith('element') else None
    
    annotation = elem.find('xsd:annotation/xsd:documentation', namespaces)
    if annotation is not None:
        for child in annotation:
            tag = child.tag.split('}')[-1]  # Removing the namespace from the tag
            if tag in csv_columns:
                data[tag] = child.text
    if data['UniqueID'] not in UNIDs:
        continue
    data_to_write.append(data)

# CSVファイルにデータを書き込む
csv_file = 'ram_definitions.csv'

try:
    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in data_to_write:
            writer.writerow(data)
except IOError:
    print("I/O error")

print(f'** END {csv_file}')