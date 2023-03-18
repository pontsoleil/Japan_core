#!/usr/bin/env python3
#coding: utf-8
#
# convert core japan CSV to transposed CSV
#
# designed by SAMBUICHI, Nobuyuki (Sambuichi Professional Engineers Office)
# written by SAMBUICHI, Nobuyuki (Sambuichi Professional Engineers Office)
#
# MIT License
#
# (c) 2023 SAMBUICHI Nobuyuki (Sambuichi Professional Engineers Office)
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
import os
import argparse
import sys

# DEBUG = None
DEBUG = True

SEP = os.sep

base = ''
core_japan_file = 'core_japan.csv'
syntax_binding_file = 'syntax_binding.csv'
jp_pint_binding_file = 'jp_pint_binding.csv'
sme_binding_file = 'sme_binding.csv'

out_base = 'data/TRANSPOSE/'

def file_path(pathname):
	if SEP == pathname[0:1]:
		return pathname
	else:
		dir = os.path.dirname(__file__)
		new_path = os.path.join(dir, pathname)
		return new_path


if __name__ == '__main__':
	# Create the parser
	parser = argparse.ArgumentParser(prog='transpose-utf16.py',
									 usage='%(prog)s infile -o outfile -e encoding [options] ',
									 description='CSVファイルを転置する')
	# Add the arguments
	parser.add_argument('inFile', metavar='infile', type=str, help='定義CSVファイル')
	parser.add_argument('-o', '--outfile')  # core.xsd
	parser.add_argument('-e', '--encoding')  # 'Shift_JIS' 'cp932' 'utf_8'
	parser.add_argument('-v', '--verbose', action='store_true')
	parser.add_argument('-d', '--debug', action='store_true')

	args = parser.parse_args()
	in_file = None
	if args.inFile:
		in_file = args.inFile.strip()
		in_file = in_file.replace('/', SEP)
		in_file = file_path(in_file)
	if not in_file or not os.path.isfile(in_file):
		print('入力定義CSVファイルがありません')
		sys.exit()
	if args.outfile:
		out_file = args.outfile.lstrip()
		out_file = out_file.replace('/', SEP)
		out_file = file_path(out_file)
		out_base = os.path.dirname(out_file)
	out_base = out_base.replace('/', SEP)
	if not os.path.isdir(out_base):
		print('出力ディレクトリがありません')
		sys.exit()

	ncdng = args.encoding
	if ncdng:
		ncdng = ncdng.lstrip()
	else:
		ncdng = 'UTF-8'
	VERBOSE = args.verbose
	DEBUG = args.debug

	with open(in_file, encoding='utf_8', newline='') as f:
		csvreader = csv.reader(f)
		content = [row for row in csvreader]

	rows = len(content)
	cols = len(content[0])
	used = [0 for x in range(cols)]
	for x in range(cols):
		for y in range(rows):
			used[x] += len(content[y][x])>0 and 1 or 0
	used_cols = len([x for x in used if x > 1])
	selected = [[0 for x in range(used_cols)] for y in range(rows)]
	
	i = 0
	for x in range(cols):
		if used[x] > 1:
			for y in range(rows):
				selected[y][i] = content[y][x]
			i += 1

	transposed = [[0 for x in range(rows)] for y in range(used_cols)]
	i = 0
	for x in range(used_cols):
		for y in range(rows):
			transposed[x][y] = selected[y][x]
	
	print('END')
