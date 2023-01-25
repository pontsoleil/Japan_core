#!/usr/bin/env python3
#coding: utf-8
#
# create XPath field for SME common invoice
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
import xml.etree.ElementTree as ET
import datetime
from collections import defaultdict
import csv
import re
import json
import sys
import os
import argparse
import math

# DEBUG = None
SEP = os.sep

DIR = 'examples'

def file_path(pathname):
    if SEP == pathname[0:1]:
        return pathname
    else:
        dir = os.path.dirname(__file__)
        new_path = os.path.join(dir, pathname)
        return new_path

def convert_record(r,data):
	bie = r['bie']
	if 'bie'==bie:
		return ''
	den = [
		r['den1'],
		r['den2'],
		r['den3'],
		r['den4'],
		r['den5'],
		r['den6'],
		r['den7'],
		r['den8'],
		r['den9'],
		r['den10'],
		r['den11'],
		r['den12']
	]
	for i in range(12):
		if den[i]:
			name = den[i]
			if bie in ['ASBIE','BBIE']:
				pos = name.find('.')
				name = name[(pos+1):]
			if 'Identification. Identifier' in name:
				name = name.replace('Identification. Identifier','ID')
			elif '. Identifier' in name:
				name = name.replace('. Identifier','ID')
			elif '. Text' in name:
				name = name.replace('. Text','')
			elif '. Details' in name:
				name = name.replace('. Details','')
			name = name.replace('_','')
			name = name.replace('.','')
			name = name.replace(' ','')
			break
	if i==0:
		name = 'rsm:'+name
	else:
		name = 'ram:'+name
	data[i] = {'bie':bie,'name':name}
	path = ''
	if 'ABIE'!=bie:
		path = ''
		for n in range(1+i):
			if 'ABIE'!=data[n]['bie']:
				path += '/'+data[n]['name']
	data[i]['xpath'] = path[1:]
	print(f'{data[i]["bie"]} {data[i]["name"]} {data[i]["xpath"]}')
	for key in ['num','kind','unid','term','desc','occur']:
		data[i][key] = r[key]
	return data[i]

if __name__ == '__main__':

	in_file = 'CIUS/data/base/sme_binding.csv'
	out_file = 'CIUS/data/base/sme_syntax_binding.txt'

	lines =[]
	data = [{}]*12
	with open(file_path(in_file), encoding='utf-8', newline='') as f:
		in_header = ['num','kind','unid','bie','den1','den2','den3','den4','den5','den6','den7','den8','den9','den10','den11','den12','term','desc','occur']
		reader = csv.DictReader(f, fieldnames=in_header)
		records = [row for row in reader]
		for record in records:
			row = convert_record(record,data)
			if row:
				lines.append(row)

	with open(file_path(out_file), 'w', encoding='utf_16', newline='') as f:
		out_header = ['num','kind','unid','bie','term','desc','name','occur','xpath']
		writer = csv.DictWriter(f,fieldnames=out_header,delimiter='\t')
		writer.writeheader()
		writer.writerows(lines)

	print(f'** END {out_file}')
