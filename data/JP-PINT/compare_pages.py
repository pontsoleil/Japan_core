import csv
import requests
from bs4 import BeautifulSoup
import difflib

def get_html_content(url):
    response = requests.get(url)
    return response.content

def extract_text_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    divs = soup.find_all('div')
    extracted_text = ' '.join([div.get_text().strip() for div in divs])
    return extracted_text

def compare_text(text1, text2):
    diff = difflib.unified_diff(text1.splitlines(), text2.splitlines())
    return list(diff)

def save_comparison_to_csv(url1, url2, diff_lines):
    url1_range = ""
    url2_range = ""
    rows = []
    for line in diff_lines:
        if line.startswith('@@'):
            line_parts = line.split(' ')
            url1_range = line_parts[1]
            url2_range = line_parts[2]
        else:
            rows.append([url1_range, url1, url2_range, url2, line])

    with open('url_comparison_result.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['url1行範囲', 'url1テキスト', 'url2行範囲', 'url2テキスト', '差分行'])
        writer.writerows(rows)

# 例として、2つのウェブページを比較してCSVファイルに出力する場合のコードです
url1 = 'https://docs.peppol.eu/poac/jp/pint-jp/bis/'
url2 = 'https://test-docs.peppol.eu/pint/pint-jp/ntr-work-v1/pint-jp-ntr/bis/'

html_content1 = get_html_content(url1)
html_content2 = get_html_content(url2)

text1 = extract_text_from_html(html_content1)
text2 = extract_text_from_html(html_content2)

diff_lines = compare_text(text1, text2)

save_comparison_to_csv(url1, url2, diff_lines)
