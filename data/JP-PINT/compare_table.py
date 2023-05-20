import csv
import requests
from bs4 import BeautifulSoup
import difflib

def get_html_content(url):
    response = requests.get(url)
    return response.content

def extract_table_rows(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table')
    rows = table.find_all('tr')
    row_data = []
    for row in rows:
        cells = row.find_all('td')
        row_values = [cell.get_text(strip=True) for cell in cells]
        row_data.append(row_values)
    return row_data

def compare_rows(row_data1, row_data2):
    diff = difflib.unified_diff(row_data1, row_data2)
    return list(diff)

def save_comparison_to_csv(url1, url2, diff_lines):
    with open(output_csv, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['url1行内容', 'url2行内容', '差分行'])
        writer.writerows(diff_lines)

# 例として、2つのURLからテーブルの行を比較してCSVファイルに出力する場合のコードです
import csv
import requests
from bs4 import BeautifulSoup
import difflib

def get_html_content(url):
    response = requests.get(url)
    return response.content

def extract_table_rows(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table')
    rows = table.find_all('tr')
    row_data = []
    for row in rows:
        cells = row.find_all('td')
        row_values = [cell.get_text(strip=True) for cell in cells]
        row_data.append('\t'.join(row_values))  # 行データをタブ区切りの文字列に変換
    return row_data

def compare_rows(row_data1, row_data2):
    diff = difflib.unified_diff(row_data1, row_data2)
    return list(diff)

def save_comparison_to_csv(url1, url2, diff_lines):
    with open(output_csv, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['url1行内容', 'url2行内容', '差分行'])
        writer.writerows(diff_lines)

# 例として、2つのURLからテーブルの行を比較してCSVファイルに出力する場合のコードです
url1 = 'https://docs.peppol.eu/poac/jp/pint-jp/trn-invoice/syntax/'
url2 = 'https://test-docs.peppol.eu/pint/pint-jp/ntr-work-v1/pint-jp-ntr/trn-invoice/syntax/'
output_csv = 'data/JP-PINT/table_comparison_result.csv'

html_content1 = get_html_content(url1)
html_content2 = get_html_content(url2)

row_data1 = extract_table_rows(html_content1)
row_data2 = extract_table_rows(html_content2)

diff_lines = compare_rows(row_data1, row_data2)

save_comparison_to_csv(url1, url2, diff_lines)
