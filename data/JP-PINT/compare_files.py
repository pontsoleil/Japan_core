import csv
import difflib

def read_html_file(file_path):
    with open(file_path, 'r', encoding="utf-8" ) as file:
        return file.read()

def compare_html_files(file1_path, file2_path):
    file1_content = read_html_file(file1_path)
    file2_content = read_html_file(file2_path)

    diff = difflib.unified_diff(file1_content.splitlines(), file2_content.splitlines())
    diff_lines = list(diff)

    return diff_lines

def save_comparison_to_csv(file1_path, file2_path, diff_lines):
    rows = []
    file1_range = ""
    file2_range = ""
    for line in diff_lines:
        if line.startswith('@@'):
            line_parts = line.split(' ')
            file1_range = line_parts[1]
            file2_range = line_parts[2]
        else:
            rows.append([file1_range, file1_path, file2_range, file2_path, line])

    with open('data/JP-PINT/file_comparison_result.csv', 'w', encoding="utf-8-sig", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['file1行範囲', 'file1テキスト', 'file2行範囲', 'file2テキスト', '差分行'])
        writer.writerows(rows)

# 例として、2つのHTMLファイルを比較してCSVファイルに出力する場合のコードです
file1_path = 'data/JP-PINT/pint-jp-resources JP PINT v1/trn-invoice/schematron/PINT-jurisdiction-aligned-rules.sch'
file2_path = 'data/JP-PINT/pint-jp-ntr-resources-dev/trn-invoice/schematron/PINT-jurisdiction-aligned-rules.sch'

diff_lines = compare_html_files(file1_path, file2_path)

save_comparison_to_csv(file1_path, file2_path, diff_lines)
