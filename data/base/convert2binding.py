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
import csv
import os

# DEBUG = None
SEP = os.sep

base = ''
core_japan_file = 'core_japan.csv'
_core_japan_file = '_core_japan.csv'
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
	core_japan_entries = []
	jp_pint_entries = []
	sme_entries = []
	_core_japan_file = f'{base}{_core_japan_file}'.replace('/', SEP)
	_core_japan_file = file_path(_core_japan_file)
	core_japan_file = f'{base}{core_japan_file}'.replace('/', SEP)
	core_japan_file = file_path(core_japan_file)
	# header = ['semSort','kind','id','level','occurrence','term','desc','representation',
	# 'UN_CCL_ID','smeKind','smeSeq','smeID','smeTerm','smeDesc','smeDefault','smeOccur','smeLevel','smeXPath',
	# 'pintSort','pintID','pintOccur','pintLevel','pintTerm','pintTermJA','pintDesc','pintDefault','pintDefault','pintXPath']
	header = ['semSort','group','id','table_id','field_id','level','occurrence','term','kind','class','propertyTerm','representation','associatedClass','desc',
	   'UN_CCL_ID','smeKind','smeSeq','smeID','smeTerm','smeDesc','smeDefault','smeOccur','smeLevel','smeXPath',
	   'pintSort','pintID','pintOccur','pintLevel','pintTerm','pintTermJA','pintDesc','pintDescJA','pintDefault','pintXPath']
	binding_header = ['semSort','id','card','level','businessTerm','desc','defaultValue','dataType','syntaxID','businessTerm_en','businessTerm_ja','desc_ja','synSort','xPath','occur']
	with open(core_japan_file, encoding='utf_8', newline='') as f:
		reader = csv.DictReader(f, fieldnames=header)
		next(reader)
		for row in reader:
			desc = row['desc'].replace(r'[\r|\n]', r'\\n')
			if len(row['pintXPath']) > 0:
				desc_ja = row['pintDefault'].replace(r'[\r|\n]', r'\\n')
				jp_pint_entry = {}
				jp_pint_entry['semSort'] = row['semSort'] and int(row['semSort']) or 0
				jp_pint_entry['id'] = row['id']
				jp_pint_entry['card'] = row['occurrence']
				jp_pint_entry['level'] = row['level'] and int(row['level']) or 0
				jp_pint_entry['businessTerm'] = row['term']
				jp_pint_entry['desc'] = desc
				jp_pint_entry['defaultValue'] = row['pintDefault']
				jp_pint_entry['dataType'] = row['representation']
				jp_pint_entry['syntaxID'] = row['pintID']
				jp_pint_entry['businessTerm'] = row['pintTerm']
				jp_pint_entry['businessTerm_ja'] = row['pintTermJA']
				jp_pint_entry['desc_ja'] = desc_ja
				jp_pint_entry['synSort'] = row['pintSort'] and int(row['pintSort']) or 0
				jp_pint_entry['xPath'] = row['pintXPath']
				jp_pint_entry['occur'] = row['pintOccur']
				jp_pint_entries.append(jp_pint_entry)
			if len(row['smeXPath']) > 0:
				desc_ja = row['smeDesc'].replace(r'[\r|\n]', r'\\n')
				sme_entry = {}
				sme_entry['semSort'] = row['semSort'] and int(row['semSort']) or 0
				sme_entry['id'] = row['id']
				sme_entry['card'] = row['occurrence']
				sme_entry['level'] = row['level'] and int(row['level']) or 0
				sme_entry['businessTerm'] = row['term']
				sme_entry['desc'] = desc
				sme_entry['defaultValue'] = row['smeDefault']
				sme_entry['dataType'] = row['representation']
				sme_entry['syntaxID'] = row['UN_CCL_ID']
				sme_entry['businessTerm_ja'] = row['smeTerm']
				sme_entry['desc_ja'] = desc_ja
				sme_entry['synSort'] = row['smeSeq'] and int(row['smeSeq']) or 0
				sme_entry['xPath'] = row['smeXPath']
				sme_entry['occur'] = row['smeOccur']
				sme_entries.append(sme_entry)
			core_japan_entries.append(row)

	jp_pint_binding_file = f'{base}{jp_pint_binding_file}'.replace('/', SEP)
	jp_pint_binding_file = file_path(jp_pint_binding_file)

	with open(_core_japan_file, 'w', encoding='utf_8', newline='') as f:
		writer = csv.DictWriter(f, fieldnames=header)
		writer.writeheader()
		writer.writerows(core_japan_entries)

	with open(jp_pint_binding_file, 'w', encoding='utf_8', newline='') as f:
		writer = csv.DictWriter(f, fieldnames=binding_header)
		writer.writeheader()
		writer.writerows(jp_pint_entries)

	jp_pint_binding_tsv_file = jp_pint_binding_file.replace('csv', 'utf-16TSV.csv')
	with open(jp_pint_binding_tsv_file, 'w', encoding='utf_16', newline='') as f:
		writer = csv.DictWriter(f,delimiter='\t',fieldnames=binding_header)
		writer.writeheader()
		writer.writerows(jp_pint_entries)

	sme_binding_file = f'{base}{sme_binding_file}'.replace('/', SEP)
	sme_binding_file = file_path(sme_binding_file)
	with open(sme_binding_file, 'w', encoding='utf_8', newline='') as f:
		writer = csv.DictWriter(f, fieldnames=binding_header)
		writer.writeheader()
		writer.writerows(sme_entries)

	sme_binding_tsv_file = sme_binding_file.replace('csv', 'utf-16TSV.csv')
	with open(sme_binding_tsv_file, 'w', encoding='utf_16', newline='') as f:
		writer = csv.DictWriter(f, delimiter='\t',fieldnames=binding_header)
		writer.writeheader()
		writer.writerows(sme_entries)

	print(f'** END \n{_core_japan_file} \n{jp_pint_binding_file} \n{sme_binding_file}')