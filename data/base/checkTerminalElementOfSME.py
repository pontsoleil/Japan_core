#!/usr/bin/env python3
#coding: utf-8
#
# check SME terminal elements containing calue from syntax binding CSV
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
sme_binding_file = 'sme_binding.csv'
sme_terminal_elementsfile = 'sme_terminal_elements.txt'

DEBUG = True

def file_path(pathname):
	if SEP == pathname[0:1]:
		return pathname
	else:
		dir = os.path.dirname(__file__)
		new_path = os.path.join(dir, pathname)
		return new_path

if __name__ == '__main__':
	elements = set()
	binding_header = ['semSort','id','card','level','businessTerm','desc','dataType','syntaxID','businessTerm_ja','desc_ja','synSort','element','synDatatype','xPath','occur']
	sme_binding_file = f'{base}{sme_binding_file}'.replace('/', SEP)
	sme_binding_file = file_path(sme_binding_file)
	with open(sme_binding_file, encoding='utf_8', newline='') as f:
		reader = csv.DictReader(f, fieldnames=binding_header)
		for r in reader:
			id = r['id']
			xPath = r['xPath']
			loc = xPath.rfind('/')
			if loc > 1 and 'JBT'==id[:3].upper():
				element = xPath[loc+1:]
				elements.add(element)

	sme_terminal_elementsfile = f'{base}{sme_terminal_elementsfile}'.replace('/', SEP)
	sme_terminal_elementsfile = file_path(sme_terminal_elementsfile)
	with open(sme_terminal_elementsfile, 'w', encoding='utf_16', newline='') as f:
		for e in list(elements):
			f.write(f'{e}\n')

	print(f'** END \n{sme_binding_file} \n{sme_terminal_elementsfile}')