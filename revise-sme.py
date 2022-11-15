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

def convert_record(record):
	record = re.sub(r'<udt:DateTimeString format="102">([0-9]{4})([0-9]{2})([0-9]{2})</udt:DateTimeString>','<udt:DateTime>\1-\2-\3</udt:DateTime>',record)
	record = record.replace('ram:GuidelineSpecifiedCIDocumentContextParameter','ram:BusinessProcessSpecifiedCIDocumentContextParameter')
	record = record.replace('','')
	record = record.replace('','')
	record = record.replace('','')
	record = record.replace('','')
	return record

if __name__ == '__main__':
	files = os.listdir(DIR)

	for file in files:
		if 'SME' == file[:3]:

			revised_file = '_SME' + file[3:]
			lines =[]
			with open(file_path(f'{DIR}{SEP}{file}'), encoding='utf-8', newline='') as f:
				records = f.readlines()
			for record in records:
				record = convert_record(record)
				lines.append(record)
			
			with open(file_path(f'{DIR}{SEP}{revised_file}'), 'w', encoding='utf_8', newline='') as f:
				f.writelines(lines)

		print(revised_file)
	print(f'END {DIR}')

