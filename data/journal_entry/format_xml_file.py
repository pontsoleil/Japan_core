import os
import xml.dom.minidom


def format_xml_file(file_path):
    # XMLファイルの読み込み
    with open(file_path, 'r') as file:
        xml_data = file.read()

    # XMLをパースしてDOMオブジェクトを作成
    dom = xml.dom.minidom.parseString(xml_data)

    # XMLを整形
    xml_formatted = dom.toprettyxml(indent='  ')

    # 整形結果をファイルに書き込み（上書き）
    with open(file_path, 'w') as file:
        file.write(xml_formatted)

def format_xml_files_in_directory(directory):
    # ディレクトリ内のファイル・ディレクトリの一覧を取得
    for root, dirs, files in os.walk(directory):
        for file in files:
            # ファイルの拡張子が.xmlの場合に整形処理を実行
            if file.endswith('.xml'):
                file_path = os.path.join(root, file)
                format_xml_file(file_path)


def main():
    # ディレクトリのパスを指定してXMLファイルを整形
    directory_path = 'data/journal_entry/XBRL_GLinstances'
    format_xml_files_in_directory(directory_path)

if __name__ == '__main__':
    main()
