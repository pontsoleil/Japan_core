#!/usr/bin/env python3
#coding: utf-8
#
# convert core_japan.csv to each syntax binding CSV
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

base = ''
core_japan_file = 'core_japan.csv'
syntax_binding_file = 'syntax_binding.csv'
jp_pint_binding_file = 'jp_pint_binding.csv'
sme_binding_file = 'sme_binding.csv'

DEBUG = True

def file_path(pathname):
	if SEP == pathname[0:1]:
		return pathname
	else:
		dir = os.path.dirname(__file__)
		new_path = os.path.join(dir, pathname)
		return new_path

if __name__ == '__main__':
	jp_pint_entries = []
	sme_entries = []
	core_japan_file = f'{base}{core_japan_file}'.replace('/', SEP)
	core_japan_file = file_path(core_japan_file)
	header = ['num','kind','id','lvl','occur','name','desc','datatype','UN_CCL_ID','sme_kind','sme_sort','sme_id','sme_name','sme_desc','sme_occur','sme_level','sme_xpath','pint_sort','pint_Id','pint_card','Level','pint_name','pint_name_ja','Description','pint_desc','pint_datatype','pint_xpath']
	binding_header = ['semSort','id','card','level','businessTerm','desc','dataType','syntaxID','businessTerm_ja','desc_ja','synSort','element','synDatatype','xPath','occur']
	with open(core_japan_file, encoding='utf_8', newline='') as f:
		reader = csv.DictReader(f, fieldnames=header)
		next(reader)
		for row in reader:
			desc = row['desc']
			# if len(desc.splitlines()) > 1:#len(desc)>0 and '\n' in desc:
			# 	desc = desc.replace('\n','\\n')
			if len(row['pint_sort'])>0:
				pint_desc = row['pint_desc']
				jp_pint_entry = {}
				jp_pint_entry['semSort'] = row['num'] and int(row['num']) or 0
				jp_pint_entry['id'] = row['id']
				jp_pint_entry['card'] = row['occur']
				jp_pint_entry['level'] = row['lvl'] and int(row['lvl']) or 0
				jp_pint_entry['businessTerm'] = row['name']
				jp_pint_entry['desc'] = desc
				jp_pint_entry['dataType'] = row['datatype']
				jp_pint_entry['syntaxID'] = row['pint_Id']
				jp_pint_entry['businessTerm_ja'] = row['pint_name_ja']
				jp_pint_entry['desc_ja'] = pint_desc
				jp_pint_entry['synSort'] = row['pint_sort'] and int(row['pint_sort']) or 0
				jp_pint_entry['xPath'] = row['pint_xpath']
				jp_pint_entry['occur'] = row['pint_card']
				jp_pint_entries.append(jp_pint_entry)
			if len(row['sme_sort'])>0:
				sme_desc = row['sme_desc']
				# if len(sme_desc.splitlines()) > 1:
				# 	sme_desc = sme_desc.replace('\n','\\n')				
				sme_entry = {}
				sme_entry['semSort'] = row['num'] and int(row['num']) or 0
				sme_entry['id'] = row['id']
				sme_entry['card'] = row['occur']
				sme_entry['level'] = row['lvl'] and int(row['lvl']) or 0
				sme_entry['businessTerm'] = row['name']
				sme_entry['desc'] = desc
				sme_entry['dataType'] = row['datatype']
				sme_entry['syntaxID'] = row['UN_CCL_ID']
				sme_entry['businessTerm_ja'] = row['sme_name']
				sme_entry['desc_ja'] = sme_desc
				sme_entry['synSort'] = row['sme_sort'] and '#N/A'!=row['sme_sort'] and int(row['sme_sort']) or 0
				sme_entry['xPath'] = row['sme_xpath']
				sme_entry['occur'] = row['sme_occur']
				sme_entries.append(sme_entry)
			# _entry[''] = row['kind']
			# _entry[''] = row['sme_kind']
			# _entry[''] = row['sme_id']
			# _entry[''] = row['sme_name']
			# _entry[''] = row['sme_desc']
			# _entry[''] = row['sme_level']
			# _entry[''] = row['pint_Id']
			# _entry[''] = row['pint_card']
			# _entry[''] = row['Level']
			# _entry[''] = row['pint_name']
			# _entry[''] = row['pint_name_ja']
			# _entry[''] = row['Description']
			# _entry[''] = row['pint_desc']
			# _entry[''] = row['pint_datatype']


	jp_pint_binding_file = f'{base}{jp_pint_binding_file}'.replace('/', SEP)
	jp_pint_binding_file = file_path(jp_pint_binding_file)
	with open(jp_pint_binding_file, 'w', encoding='utf_8', newline='') as f:
		writer = csv.DictWriter(f, fieldnames=binding_header)
		writer.writeheader()
		writer.writerows(jp_pint_entries)

	sme_binding_file = f'{base}{sme_binding_file}'.replace('/', SEP)
	sme_binding_file = file_path(sme_binding_file)
	with open(sme_binding_file, 'w', encoding='utf_8', newline='') as f:
		writer = csv.DictWriter(f, fieldnames=binding_header)
		writer.writeheader()
		writer.writerows(sme_entries)

	print(f'** END \n{jp_pint_binding_file} \n{sme_binding_file}')