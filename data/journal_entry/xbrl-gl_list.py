import os

# ディレクトリのパスを指定する
dir_path = "../../"

# ディレクトリ内のファイル一覧を取得する
file_list = os.listdir(dir_path)

# ファイル一覧をHTMLのリストとして整形する
html_list = "<ul>\n"
for file_name in file_list:
    # ファイル名から拡張子を取得する
    _, file_ext = os.path.splitext(file_name)
    # 拡張子がhtmlの場合にはリンクを生成する
    if file_ext == ".html":
        html_list += f'<li><a href="{file_name}">{file_name}</a></li>\n'
html_list += "</ul>"

# HTMLを出力する
print(html_list)