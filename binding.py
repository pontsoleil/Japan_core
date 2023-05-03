# import csv
# import os
# import xml.etree.ElementTree as ET

# # CSVファイルの読み込み
# with open('data/base/xBRL_GL_binding.csv', 'r',encoding='utf-8') as csv_file:
#     reader = csv.DictReader(csv_file, skipinitialspace=True)
#     columns = [row['id'] for row in reader if len(row['id']) > 0]
#     xpaths = [row['xPath'] for row in reader if row['xPath']]

# # XMLファイルが含まれるディレクトリのパス
# directory_path = 'data\\xml\\XBRL-GL'

# # 出力用CSVファイルを作成
# with open('output.csv', 'w', newline='') as output_file:
#     writer = csv.writer(output_file)
#     writer.writerow(columns)

#     # ディレクトリ内のXMLファイルに対して処理を実行
#     for filename in os.listdir(directory_path):
#         if filename.endswith('.xml'):
#             file_path = os.path.join(directory_path, filename)

#             # XMLファイルの読み込み
#             tree = ET.parse(file_path)
#             root = tree.getroot()

#             # XPathに対応する要素の情報を取得
#             values = []
#             for xpath in xpaths:
#                 element = root.find(xpath)
#                 if element is not None:
#                     value = element.text
#                 else:
#                     value = ''
#                 values.append(value)

#             # CSVファイルに出力
#             writer.writerow(values)


import csv
import os
import xml.etree.ElementTree as ET

ns = {
    'xbrli': 'http://www.xbrl.org/2001/instance', 
    'gl-cor': 'http://www.xbrl.org/int/gl/cor/2015-12-23',
    'ISO4217': 'http://www.xbrl.org/2003/iso4217',
    'gl-bus': 'http://www.xbrl.org/taxonomy/int/gl/bus/2003-08-29/',
    'gl-cor': 'http://www.xbrl.org/taxonomy/int/gl/cor/2003-08-29/',
    'gl-muc': 'http://www.xbrl.org/taxonomy/int/gl/muc/2003-08-29/',
    'gl-plt': 'http://www.xbrgl.com/gl-plt/',
    'gl-usk': 'http://www.xbrl.org/taxonomy/int/gl/usk/2003-08-29/',
    'link': 'http://www.xbrl.org/2001/XLink/xbrllinkbase',
    'tdb': 'www.tdb.co.jp',
    'xbrli': 'http://www.xbrl.org/2001/instance',
    'xhtml': 'http://www.w3.org/1999/xhtml',
    'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
    'jp-bs': 'http://www.xbrl-jp.org/taxonomy/jp/fr/common/bs/2003-08-31',
    'jp-gcd': 'http://www.xbrl-jp.org/taxonomy/jp/gcd/2003-08-31',
    'jp-pl': 'http://www.xbrl-jp.org/taxonomy/jp/fr/common/pl/2003-08-31',
    'jp-sc': 'http://www.xbrl-jp.org/taxonomy/jp/fr/common/sc/2003-08-31',
    'jp-sr': 'http://www.xbrl-jp.org/taxonomy/jp/fr/common/sr/2003-08-31',
    'jp-ta-bs': 'http://www.xbrl-jp.org/taxonomy/jp/fr/ta/bs/2003-08-31',
    'jp-ta-pl': 'http://www.xbrl-jp.org/taxonomy/jp/fr/ta/pl/2003-08-31',
    'jp-ta-sc': 'http://www.xbrl-jp.org/taxonomy/jp/fr/ta/sc/2003-08-31',
    'jp-ta-sr': 'http://www.xbrl-jp.org/taxonomy/jp/fr/ta/sr/2003-08-31',
    'pca-bs': 'http://www.pca.co.jp/taxonomy/jp/fr/bs/2003-08-31',
    'pca-pl': 'http://www.pca.co.jp/taxonomy/jp/fr/pl/2003-08-31',
    'pca-sr': 'http://www.pca.co.jp/taxonomy/jp/fr/sr/2003-08-31'
}

# CSVファイルの読み込み
columns = []
xpaths = []
with open('data/base/xBRL_GL_binding.csv', 'r', encoding='utf-8') as csv_file:
    reader = csv.DictReader(filter(lambda row: row[0]!='\n', csv_file), skipinitialspace=True)
    for row in reader:
        if len(row['id']) > 0:
            columns.append(row['id'])
            xpaths.append(row['xPath'] if row['xPath'] else None)

# XMLファイルが含まれるディレクトリのパス
directory_path = 'data\\xml\\XBRL-GL'

# 出力用CSVファイルを作成
with open('output.csv', 'w', newline='') as output_file:
    writer = csv.writer(output_file)
    writer.writerow(columns)

    # ディレクトリ内のXMLファイルに対して処理を実行
    for filename in os.listdir(directory_path):
        if filename.endswith('.xml'):
            file_path = os.path.join(directory_path, filename)

            # XMLファイルの読み込み
            tree = ET.parse(file_path)
            root = tree.getroot()

            # XPathに対応する要素の情報を取得
            values = []
            for i, xpath in enumerate(xpaths):
                if xpath:
                    # XPathを相対パスに変更
                    relative_xpath = xpath.replace('/xbrli:group', '.')
                    element = root.find(relative_xpath, namespaces=ns)
                if element is not None:
                    value = element.text.strip()
                else:
                    print(f'XPath not found: {xpath}')  # どのXPathで問題が起きたかを出力
                    value = ''
                values.append(value)    

            # CSVファイルに出力
            writer.writerow(values)
print('END')