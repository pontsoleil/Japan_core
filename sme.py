#!/usr/bin/env python3
#coding: utf-8
#
# convert EN 16931-3-3 eInvoice (CII) to SME common invoice
#
# designed by SAMBUICHI, Nobuyuki (Sambuichi Professional Engineers Office)
# written by SAMBUICHI, Nobuyuki (Sambuichi Professional Engineers Office)
#
# MIT License
#
# (c) 2022 SAMBUICHI Nobuyuki (Sambuichi Professional Engineers Office)
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
import os

SEP = os.sep
root = None
elementMap = {}

udtType = [
	"udt:AmountType",
	"udt:BinaryObjectType",
	"udt:CodeType",
	"udt:DateTimeType",
	"udt:IDType",
	"udt:IndicatorType",
	"udt:PercentType",
	"udt:QuantityType",
	"udt:RateType",
	"udt:TextType"
]

ramType = {
	"Sub-DivisionBranchFinancialInstitution": "ram:BranchFinancialInstitutionType",
	"SpecifiedProcuringProject": "ram:ProcuringProjectType",
	"AttachedSpecifiedBinaryFile": "ram:SpecifiedBinaryFileType",
	"ApplicableTradeSettlementFinancialCard": "ram:TradeSettlementFinancialCardType",
}

def file_path(pathname):
	if SEP == pathname[0:1]:
		return pathname
	else:
		dir = os.path.dirname(__file__)
		new_path = os.path.join(dir, pathname)
		return new_path

def write_header(f):
	header = [
		'<?xml version="1.0" encoding="UTF-8"?>\n',
		'<!-- ====================================================================== -->\n',
		'<!-- ===== Custom Aggregate Business Information Entity Schema Module ===== -->\n',
		'<!-- ====================================================================== -->\n',
		'<!--,'
		'Schema agency:  XBRL Japan\n',
		'Schema version: 0.1\n',
		'Schema date:    10NOV22\n',
		'\n',
		'Copyright (C) XBRL Japan. All Rights Reserved.\n',
		'-->\n',
		'<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema" targetNamespace="urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:31"\n',
		'\txmlns:ccts="urn:un:unece:uncefact:documentation:standard:CoreComponentsTechnicalSpecification:2"\n',
		'\txmlns:udt="urn:un:unece:uncefact:data:standard:UnqualifiedDataType:31"\n',
		'\txmlns:qdt="urn:un:unece:uncefact:data:standard:QualifiedDataType:31"\n',
		'\txmlns:ram="urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:31"\n',
		'\telementFormDefault="qualified" attributeFormDefault="unqualified" version="23.1">\n',
		'\t<!-- ======================================================================= -->\n',
		'\t<!-- ===== Imports                                                     ===== -->\n',
		'\t<!-- ======================================================================= -->\n',
		'\t<!-- ======================================================================= -->\n',
		'\t<!-- ===== Import of Unqualified Data Type Schema Module               ===== -->\n',
		'\t<!-- ======================================================================= -->\n',
		'\t<xsd:import namespace="urn:un:unece:uncefact:data:standard:UnqualifiedDataType:31" schemaLocation="UnqualifiedDataType_31p0.xsd"/>\n',
		'\t<!-- ======================================================================= -->\n',
		'\t<!-- ===== Import of Qualified Data Type Schema Module                 ===== -->\n',
		'\t<!-- ======================================================================= -->\n',
		'\t<xsd:import namespace="urn:un:unece:uncefact:data:standard:QualifiedDataType:31" schemaLocation="QualifiedDataType_31p0.xsd"/>\n',
		'\t<!-- ======================================================================= -->\n',
		'\t<!-- ===== Element Declarations                                        ===== -->\n',
		'\t<!-- ======================================================================= -->\n',
		'\t<!-- ================================================================== -->\n',
		'\t<!-- ===== Type Definitions                                       ===== -->\n'
	]
	for line in header:
		f.write(line)

def write_complex(f,aggregatename,elementnames):
	if root == aggregatename:
		return
	aggregate = elementMap[aggregatename]
	id = aggregate['id']
	name = aggregate['name'][4:]
	complex_start = [
		'\t<!-- ================================================================== -->\n',
		f'\t<!-- ===== Type Definition: {name} ===== -->\n',
		'\t<!-- ================================================================== -->\n',
		f'\t<xsd:complexType name="{name}">\n',
		f'\t\t<!--{id}-->\n',
		'\t\t<xsd:sequence>\n'
	]
	for line in complex_start:
		f.write(line)
	for elementname in elementnames:
		element = elementMap[elementname]
		id = element['id']
		kind = element['kind']
		name = element['name'][4:]
		type = None
		if 'BBIE'==kind:
			for t in udtType:
				_t = t[4:-4]
				length = len(_t)
				if name[-length:]==_t:
					type = t
					break
			if not type:
				type = 'udt:TextType'
		else:
			if 'CI' in name:
				n = name[name.index('CI'):]
				type = f'ram:{n}Type'
			else:
				for k,v in ramType.items():
					if k==name:
						type = v
		if not type:
			type = f'{name}Type'
		occurs = element['occurs']
		min = occurs[0]
		max = occurs[-1]
		if 'n'==max:
			max = 'unbounded'
		element = [
			f'\t\t\t<xsd:element name="{name}" type="{type}"  minOccurs="{min}" maxOccurs="{max}"  >\n',
			f'\t\t\t\t<!--{id}-->\n',
			'\t\t\t</xsd:element>\n'
		]
		for line in element:
			f.write(line)
	cpmplex_end = [
		'\t\t</xsd:sequence>\n',
		'\t</xsd:complexType>\n'
	]
	for line in cpmplex_end:
		f.write(line)

def write_closeschema(f):
	f.write('</xsd:schema>')

if __name__ == '__main__':
	file = file_path('sme.csv')
	lines =[]
	with open(file, encoding='utf-8', newline='') as f:
		reader = csv.DictReader(f)
		_path = []
		_path += ['']*12
		root = ''
		for r in reader:
			data = {}
			num = r['\ufeffnum']
			data['num'] = int(num)
			data['group'] = r['group']
			kind = r['kind']
			data['kind'] = kind
			for pos in range(1,13):
				if r[f'den{pos}']:
					if pos > 2:
						level = 1 + int(pos/2)
					else:
						level = pos
			data['level'] = level
			data['id'] = r['UN _CCL_ID']
			name = r['name']
			data['name'] = name
			data['name_ja'] = r['name_ja']
			data['desc_ja'] = r['desc_ja']
			data['occurs'] = r['occurs']
			data['ver'] = r['ver']
			path = []
			if 'ABIE'==kind:
				data['xpath'] = ''
			else:
				for i in range(level):
					if i < len(_path):
						path += [_path[i]]
				path += [name]
				_path = path
				xpath = '/'.join(path)
				data['xpath'] = xpath
			data['DEN'] = r['den']
			lines.append(data)
			elementMap[name] = data
			if not root:
				root = name
				_path[0] = f'/{root}'

	tmp_file = file_path('sme_tmp.csv')
	with open(tmp_file, 'w', encoding='utf_16', newline='') as csvfile:
		fieldnames = ['num','group','kind','level','id','name','name_ja','desc_ja','occurs','ver','xpath','DEN']
		writer = csv.DictWriter(csvfile, delimiter='\t', fieldnames=fieldnames)
		writer.writeheader()
		writer.writerows(lines)

	aggregates = ['']*7
	aggregateMap = {}
	for data in lines:
		num = data['num']
		kind = data['kind']
		level = data['level']
		name = data['name']
		if 'MA' == kind:
			aggregates[0] = name
			aggregateMap[name] = []
		elif kind in ['ASMA','ABIE']:
			aggregates[level] = name
			aggregateMap[name] = []
		if kind in ['ASMA','ASBIE','BBIE']:
			aggregate = aggregates[level - 1]
			if not name in aggregateMap[aggregate]:
				aggregateMap[aggregate] += [name]

	xsd_file = file_path('sme.xsd')
	with open(xsd_file, 'w', encoding='utf_8', newline='') as f:
		write_header(f)
		for aggregate,elements in aggregateMap.items():
			write_complex(f,aggregate,elements)
		write_closeschema(f)

	print(f'END {xsd_file}')

