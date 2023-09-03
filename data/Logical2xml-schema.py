#!/usr/bin/env python3
# coding: utf-8
#
# generate Audit Data Collection XML Schema fron CSV file and header files
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

# import json
import argparse
import os
import sys
import csv
import re

DEBUG = True
VERBOSE = True
SEP = os.sep

source_base       = 'xBRL/source/'
out_file          = f'{source_base}ADC.csv'
source_base       = source_base.replace('/', SEP)
source_file       = f'{source_base}LogicalModel.csv'
# name_file         = f'{source_base}adc-label.csv'

xbrl_base         = 'xBRL/taxonomy/'
xbrl_base         = xbrl_base.replace('/', SEP)
core_xsd          = 'core.xsd'
core_definition   = 'core-def'
core_presentation = 'core-pre'
core_label        = 'core-lbl'

moduleDict = {
    'BS': {'name': 'Base', 'max': 0},
    'PE': {'name': 'PPE', 'max': 0},
    'PY': {'name': 'Payroll', 'max': 0},
    'SL': {'name': 'Sales', 'max': 0},
    'GL': {'name': 'Grneral Ledger', 'max': 0},
    'CC': {'name': 'Common', 'max': 0},
    'AR': {'name': 'Account Receivable', 'max': 0},
    'IV': {'name': 'Inventory', 'max': 0},
    'AP': {'name': 'Account Payable', 'max': 0},
    'PR': {'name': 'Purchase', 'max': 0}
}

representationMap = {
    'Identifier': 'Identifier',
    'Period Identifier': 'Identifier',
    'Year Identifier': 'Identifier',
    'Text': 'Text',
    'Name': 'Name',
    'Numeric': 'Numeric',
    'Quantity': 'Quantity',
    'Amount': 'Amount',
    'Price': 'Amount',
    'Percentage': 'Percentage',
    'Date': 'Date',
    'Time': 'Time',
    'Time Zone': 'Time Zone',
    'Indicator': 'Indicator',
    'Adjustment Indicator': 'Indicator',
    'Code': 'Code',
    'Country_ Code': 'Code',
    'Currency_ Code': 'Code',
    'Measurement Unit_ Code': 'Code',
    'Credit_ Indicator': 'Code',
    'Gl Account Number': 'Code',
    'Tax Type_ Code': 'Code',
    'Phone Number': 'Code',
    'Reference Level': 'Code',
    'Account Hierarchy': 'Code',
    'Region_ Code': 'Code',
    'Payment Term_ Code': 'Code',
    'State Province_ Code': 'Code',
    'Tax Identification Number': 'Code',
    'Hierarchy Level': 'Code',
    'Account Type': 'Code'
}

datatypeMap = {
    'Amount': {
        'adc': 'amountItemType',
        'xbrli': 'monetaryItemType'},
    'Binary Object': {
        'adc': 'binaryObjectItemType',
        'xbrli': 'stringItemType'},
    'Code': {
        'adc': 'codeItemType',
        'xbrli': 'tokenItemType'},
    'Date': {
        'adc': 'dateItemType',
        'xbrli': 'dateItemType'},
    'Document Reference': {
        'adc': 'documentReferenceItemType',
        'xbrli': 'tokenItemType'},
    'Identifier': {
        'adc': 'identifierItemType',
        'xbrli': 'tokenItemType'},
    'Indicator': {
        'adc': 'indicatorItemType',
        'xbrli': 'booleanItemType'},
    'Text': {
        'adc': 'textItemType',
        'xbrli': 'stringItemType'},
    'Time': {
        'adc': 'timeItemType',
        'xbrli': 'timeItemType'},
    'Percentage': {
        'adc': 'percentageItemType',
        'xbrli': 'pureItemType'},
    'Quantity': {
        'adc': 'quantityItemType',
        'xbrli': 'intItemType'},
    'Unit Price Amount': {
        'adc': 'unitPriceAmountItemType',
        'xbrli': 'monetaryItemType'},
}

abbreviationMap = {
    'ACC': 'Account',
    'ADJ': 'Adjustment',
    'BAS': 'Base',
    'BEG': 'Beginning',
    'CUR': 'Currency',
    'CUS': 'Customer',
    'FOB': 'Free On Board',
    'FS': 'Financial Statement',
    'INV': 'Inventory',
    'IT': 'Information Technology',
    'JE': 'Journal Entry',
    'NUM': 'Number',
    'ORG': 'Organization',
    'PK': 'Primary Key',
    'PO': 'Purchase Order',
    'PPE': 'Property, Plant and Equipment',
    'PRV': 'Province',
    'PUR': 'Purchase',
    'REF': 'Reference Identifier',
    'RFC': 'Request For Comments',
    'SAL': 'Sales',
    'TIN': 'Tax Identification Number',
    'TRX': 'Transactional',
    'UOM': 'Unit of Measurement',
    'WIP': 'Work In Progress'
}

duplicateNames = set()
names = set()
adcDict = {}
targetRefDict = {}
referenceDict = {}
sourceRefDict = {}
locsDefined = {}
arcsDefined = {}
locsDefined = {}
alias = {}
targets = {}
roleMap = None
primaryKeys = set()

def file_path(pathname):
    if SEP == pathname[0:1]:
        return pathname
    else:
        pathname = pathname.replace('/', SEP)
        dir = os.path.dirname(__file__)
        new_path = os.path.join(dir, pathname)
        return new_path

# lower camel case concatenate
def LC3(term):
    if not term:
        return ''
    terms = term.split(' ')
    name = ''
    for i in range(len(terms)):
        if i == 0:
            if 'TAX' == terms[i]:
                name += terms[i].lower()
            elif len(terms[i]) > 0:
                name += terms[i][0].lower() + terms[i][1:]
        else:
            name += terms[i][0].upper() + terms[i][1:]
    return name

# snake concatenate
def SC(term):
    if not term:
        return ''
    term = re.sub('_', '', term).strip()
    terms = term.split(' ')
    name = '_'.join(terms)
    return name

def remove_repeated_substrings(s):
    s += ' '
    while True:
        # 重複する任意の部分文字列を探します。
        match = re.search(r'(.+ )(?=\1)', s)        
        # 重複が見つからなければループを終了します。
        if not match:
            break        
        # 最初の重複を削除します。
        s = s[:match.start(1)] + s[match.start(1)+len(match.group(1)):]
    s = s.strip()
    return s

def getName(record):
    if not record:
        return ''
    classTerm    = record['classTerm']
    propertyTerm = record['propertyTerm']
    associatedClass = record['associatedClass']
    if kind in ['ABIE', 'ACC']:
        name = classTerm
    elif kind in ['ASBIE','ASCC']:
        name = f'{classTerm} {associatedClass}'
    elif kind in ['RFBIE','RFCC']:
        name = f'{propertyTerm} {associatedClass}'
    elif 'CC'==kind[-2:]:
        name = f'{classTerm} {propertyTerm}'
    else:
        name = propertyTerm
    name = re.sub(r'[-_,\.]','',name)
    name = remove_repeated_substrings(name)
    name = re.sub('Invoice Generated Invoice ','Invoice Generated ',name)
    name = re.sub('Invoice Generated Details Invoice Details ','Invoice Generated Details ',name)
    name = re.sub('Invoice Received Invoice ','Invoice Received ',name)
    name = re.sub('Invoice Received Details Invoice Details ','Invoice Received Details ',name)
    name = re.sub('Details Details','Details',name)
    name = re.sub('Order Details Order ','Order Details ',name)
    name = re.sub('Amount Multicurrency Amounts ','Multicurrency Amounts ',name)
    name = re.sub('Account Payable ','AP ',name)
    name = re.sub('Account Receivable ','AR ',name)
    name = re.sub('Unit of Measurement ','UOM ',name)
    name = re.sub('Property Plant and Equipment ','PPE ',name)
    return name

def getDEN(record):
    # record = getRecord(adc_id)
    classTerm = record['classTerm']
    if not record:
        return ''
    if kind in ['ABIE', 'ACC']:
        DEN = f'{classTerm}. Details'
    else:
        propertyTerm = record['propertyTerm']
        if kind in ['RFBIE', 'ASBIE']:
            associatedClass = record['associatedClass']
            DEN = f'{classTerm}. {propertyTerm}. {associatedClass}'
        else:
            representation = record['representation']
            DEN = f'{classTerm}. {propertyTerm}. {representation}'
    return DEN

def getLC3_DEN(adc_id):
    record = getRecord(adc_id)
    den = getDEN(record)
    if den:
        den = den[:den.find('.')]
        return LC3(den)
    return ''

def getSC_DEN(adc_id):
    record = getRecord(adc_id)
    den = getDEN(record)
    if den:
        den = den[:den.find('.')]
        return SC(den)
    return ''

def getClassName(adc_id):
    record = getRecord(adc_id)
    den = getDEN(record)
    if den:
        cn = den[5:den.find('.')]
        return cn
    return ''

def getRecord(adc_id):
    if adc_id in adcDict:
        record = adcDict[adc_id]
    else:
        target_id = adc_id[-4:]
        if target_id not in adcDict:
            print(f'** ERROR {target_id} not in adcDict')
            return None
        record = adcDict[target_id]
    return record

def getParent(parent_id_list):
    parent_id = parent_id_list[-1]
    if parent_id in adcDict:
        parent = adcDict[parent_id]
    else:
        parent = None
    return parent

def getChildren(adc_id):
    record = getRecord(adc_id)
    if not record:
        return []
    return record['children']

def childMember(link_id, child_id):
    global count
    global lines
    global locsDefined
    global arcsDefined
    global targetRefDict
    global referenceDict
    if link_id not in locsDefined:
        locsDefined[link_id] = set()
    if link_id not in arcsDefined:
        arcsDefined[link_id] = set()
    child = getRecord(child_id)
    child_kind = child['kind']
    if not child:
        return
    if child_id in targetRefDict:
        if not child_id in locsDefined[link_id]:
            locsDefined[link_id].add(child_id)
            lines.append(
                f'        <link:loc xlink:type="locator" xlink:href="{core_xsd}#{child_id}" xlink:label="{child_id}" xlink:title="{child_id}"/>\n')
        count += 1
        arc_id = f'{link_id} {child_id}'
        role_id = f'l_{child_id}'
        URI = f"/{role_id}"
        lines.append(f'        <!-- {child_id} targetRole {role_id} -->\n')
        if not child_id in locsDefined[link_id]:
            locsDefined[link_id].add(child_id)
            lines.append(
                f'        <link:loc xlink:type="locator" xlink:href="{core_xsd}#{child_id}" xlink:label="{child_id}" xlink:title="{child_id}"/>\n')
        count += 1
        arc_id = f'{link_id} {child_id}'
        if not arc_id in arcsDefined[link_id]:
            arcsDefined[link_id].add(arc_id)
            lines.append(
                f'        <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xbrldt:targetRole="http://www.xbrl.jp/audit-data-collection/role{URI}" xlink:from="{link_id}" xlink:to="{child_id}" xlink:title="domain-member: {link_id} to {child_id} in {role_id}" order="{count}"/>\n')
            if DEBUG:
                print(
                    f"domain-member: {link_id} to {child_id} in {role_id} targetRole")
    else:
        if not child_id in locsDefined[link_id]:
            locsDefined[link_id].add(child_id)
            lines.append(
                f'        <link:loc xlink:type="locator" xlink:href="{core_xsd}#{child_id}" xlink:label="{child_id}" xlink:title="{child_id}"/>\n')
        count += 1
        arc_id = f'{link_id} {child_id}'
        if not arc_id in arcsDefined[link_id]:
            arcsDefined[link_id].add(arc_id)
            lines.append(
                f'        <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="{link_id}" xlink:to="{child_id}" xlink:title="domain-member: {link_id} to {child_id}" order="{count}"/>\n')
            if DEBUG:
                print(f"domain-member: {link_id} to {child_id}")
        if child_kind in ['ABIE', 'ACC']:
            grand_children = child['children']
            for grand_child_id in grand_children:
                childMember(link_id, grand_child_id)

def defineHypercube(adc_id, role, n):
    global lines
    global locsDefined
    global arcsDefined
    global targetRefDict
    global referenceDict
    root_id = None
    root_id = adc_id
    root = getRecord(root_id)
    if not root:
        return None
    link_id = role['link_id']
    locsDefined[link_id] = set()
    arcsDefined[link_id] = set()
    URI = role['URI']
    role_id = role['role_id']
    hypercube_id = f"h_{link_id}"
    dimension_id_list = set()
    if DEBUG:
        print(f"** defineHypercube {link_id}")
    if '-' not in link_id:
        root_dimension = f"d_{root_id}"
        dimension_id_list.add(root_dimension)
    else:
        match = re.match(r'^(.*[A-z]{2}[0-9]{2})-([0-9]{2})$', link_id)
        if match:
            root_id = match[1]
        else:
            root_id = link_id
        dims = root_id.split('-')
        for dim in dims:
            dimension = f'd_{dim}'
            dimension_id_list.add(dimension)
    lines.append(
        f'    <link:definitionLink xlink:type="extended" xlink:role="http://www.xbrl.jp/audit-data-collection/role{URI}">\n')
    # all (has-hypercube)
    lines.append(
        f'        <!-- {link_id} all (has-hypercube) {hypercube_id} {role_id} -->\n')
    lines.append(
        f'        <link:loc xlink:type="locator" xlink:href="{core_xsd}#{link_id}" xlink:label="{link_id}" xlink:title="{link_id}"/>\n')
    lines.append(
        f'        <link:loc xlink:type="locator" xlink:href="{core_xsd}#{hypercube_id}" xlink:label="{hypercube_id}" xlink:title="{hypercube_id}"/>\n')
    lines.append(
        f'        <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/all" xlink:from="{link_id}" xlink:to="{hypercube_id}" xlink:title="all (has-hypercube): {link_id} to {hypercube_id}" order="1" xbrldt:closed="true" xbrldt:contextElement="segment"/>\n')
    if DEBUG:
        print(f'all(has-hypercube) {link_id} to {hypercube_id} ')
    # hypercube-dimension
    lines.append('        <!-- hypercube-dimension -->\n')
    count = 0
    for dimension_id in dimension_id_list:
        lines.append(
            f'        <link:loc xlink:type="locator" xlink:href="{core_xsd}#{dimension_id}" xlink:label="{dimension_id}" xlink:title="{dimension_id}"/>\n')
        count += 1
        lines.append(
            f'        <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/hypercube-dimension" xlink:from="{hypercube_id}" xlink:to="{dimension_id}" xlink:title="hypercube-dimension: {hypercube_id} to {dimension_id}" order="{count}"/>\n')
        if DEBUG:
            print(f'hypercube-dimension {hypercube_id} to {dimension_id} ')
    # domain-member
    lines.append('        <!-- domain-member -->\n')
    count = 0
    if 'children' in root and len(root['children']) > 0:
        children = root['children']
        for child_id in children:
            childMember(link_id, child_id)
    # closing tag link:definitionLink
    lines.append('    </link:definitionLink>\n')

if __name__ == '__main__':
    # # Create the parser
    # parser = argparse.ArgumentParser(prog='ADCS_H2xBRL-taxonomy.py',
    #                                  usage='%(prog)s infile -o outfile -e encoding [options] ',
    #                                  description='Audit data collection 定義CSVファイルをxBRLタクソノミに変換')
    # # Add the arguments
    # parser.add_argument('inFile', metavar='infile', type=str,
    #                     help='Audit data collection 定義CSVファイル')
    # parser.add_argument('-o', '--outfile')  #
    # parser.add_argument('-e', '--encoding')  # 'Shift_JIS' 'cp932' 'utf_8'
    # parser.add_argument('-v', '--verbose', action='store_true')
    # parser.add_argument('-d', '--debug', action='store_true')
    # # parse args
    # args = parser.parse_args()
    # in_file = None
    # if args.inFile:
    #     in_file = args.inFile.strip()
    #     in_file = in_file.replace('/', SEP)
    #     in_file = file_path(args.inFile)
    # if not in_file or not os.path.isfile(in_file):
    #     print('入力ADC定義CSVファイルがありません')
    #     sys.exit()
    # adc_file = in_file
    source_file = file_path(source_file)
    name_file   = file_path(name_file)
    # if args.outfile:
    #     out_file = args.outfile.lstrip()
    out_file    = out_file.replace('/', SEP)
    out_file    = file_path(out_file)
    # name_file = re.sub(r'^(.+/)([a-zA-Z]+)\.csv$', r'\1\2_name.csv', out_file)
    # name_file = name_file.replace('/', SEP)
    # name_file = file_path(name_file)
    # xbrl_base = xbrl_base.replace('/', SEP)
    xbrl_base = file_path(xbrl_base)
    if not os.path.isdir(xbrl_base):
        print('タクソノミのディレクトリがありません')
        sys.exit()
    # encoding
    # ncdng = args.encoding
    # if ncdng:
    #     ncdng = ncdng.lstrip()
    # else:
    ncdng = 'utf-8-sig'

    VERBOSE = True # args.verbose
    DEBUG   = True # args.debug

    # adc_file  = file_path(adc_file)
    parentIDs = []
    moduleSet = set()
    classDict = {}  # classDict[classTerm] = adc_id[-4:]
    # ssociatedClassIdDict[class_id].append(associatedClassId)
    associatedClassIdDict = {}
    # ABIE and ACC renmae dict aggrgateDict[adc_id] = module_id + str(module_max).zfill(2)
    aggrgateDict = {}
    adcDict = {}
    adc_records = []
    checkClass = True
    # targetClassTerm = ['GL Header']
    # targetClassIDs = ['GL03']
    targetClassSet = set()
    records0 = []
    header = ['adc_id', 'kind', 'level', 'occurrence', 'classTerm',
              'propertyTerm', 'representation', 'associatedClass', 'description']
    with open(source_file, encoding=ncdng, newline='') as f:
        reader = csv.reader(f)  # , delimiter='\t')
        next(reader)
        SP_ID = ''
        for cols in reader:
            record = {}
            for i in range(len(cols)):
                col = cols[i]
                record[header[i]] = re.sub('\s+', ' ', col).strip()
            records0.append(record)

    dictASBIE = {}
    records = []
    for i in range(len(records0)):
        record = records0[i]
        if 'adc_id' not in record or not record['adc_id']:
            continue
        adc_id = record['adc_id']
        kind   = record['kind']
        level  = int(record['level'])
        for idASBIE, levelASBIE in dictASBIE.items():
            if idASBIE in adc_id and ('ASBIE' != kind or level > levelASBIE):
                continue
        if level > 1 and kind in ['SPCC']:
            continue
        if 'ASBIE' == kind:
            occurrence = record['occurrence']
            if '*' == occurrence[-1]:
                dictASBIE[record['adc_id']] = level
            next_record = records0[1+i]
            next_kind = next_record['kind']
            next_id = next_record['adc_id']
            if next_kind in ['ABIE', 'ACC']:
                next_record['occurrence'] = occurrence
            elif 'SPCC' == next_kind:
                after_the_next = records0[2+i]
                after_the_next_kind = after_the_next['kind']
                if 'ACC' == after_the_next_kind:
                    after_the_next['occurrence'] = occurrence
                else:
                    if VERBOSE:
                        print(f"** IRREGULAR RECORD {after_the_next}")
            else:
                if VERBOSE:
                    print(f"** IRREGULAR RECORD {next_record}")
            continue
        records.append(record)
        adcDict[adc_id] = record

    if DEBUG:
        print([x for x in records0 if 'AP01' in x['adc_id']])

    for record in records:
        adc_id  = record['adc_id']
        kind    = record['kind']
        classID = adc_id[:4]
        if len(kind) > 5 and 'PKBIE' == kind[:5]:
            kind = 'PKBIE'
            record['kind'] = kind
        if not kind in ['ABIE', 'ASBIE']:
            module = record['adc_id'][:2]
            moduleSet.add(module)
        if 'ABIE' == kind:
            SP_ID = ''
        elif kind in ['SPBIE', 'SPCC']:
            continue
        module_id        = adc_id[:2]
        module           = moduleDict[module_id]
        record['module'] = module['name']
        level            = record['level']
        if re.match('[0-9]+', level):
            level = int(level)
        else:
            level = 0
        record['level'] = level
        type = ''
        if kind in ['ABIE', 'RFBIE', 'ACC', 'RFCC']:
            datatype = ''
        else:
            representation = record['representation']
            if representation in representationMap:
                datatype = representationMap[representation]
            else:
                representation = re.sub('[^_]+_', '', representation).strip()
                representation = re.sub('[0-9\-]+', '', representation).strip()
                representation = re.sub('^.*\s', '', representation).strip()
                if representation in representationMap:
                    datatype = representationMap[representation]
                else:
                    datatype = 'Text'
        record['datatype'] = datatype
        occurrence         = record['occurrence']
        record['occMin']   = occurrence[:1]
        record['occMax']   = occurrence[-1:]
        DEN                = getDEN(record)
        record['DEN']      = DEN
        name               = getName(record)
        record['name']     = name

        adc_records.append(record)

        record['parent'] = []
        record['children'] = []
        record['target_id'] = ''
        adcDict[adc_id] = record

    # update adc_id and assign target_id
    targetRefDict = {}
    for i in range(len(adc_records)):
        record = adc_records[i]
        adc_id = record['adc_id']
        kind   = record['kind']
        occurrence = record['occurrence']
        if kind in ['ABIE', 'ACC'] and '*' == occurrence[-1]:
            targetRefDict[adc_id] = adc_id
        adcDict[adc_id] = record

    # Set parent and children
    print('== register parent')
    adcDict = {}
    for i in range(len(adc_records)):
        record = adc_records[i]
        adc_id = record['adc_id']
        kind   = record['kind']
        level  = record['level']
        if 1 == level:
            record['parent']   = []
            record['children'] = []
            parentIDs = ['', adc_id]
        elif kind in ['ABIE', 'ACC']:
            while len(parentIDs) > level:
                parentIDs.pop()
            while len(parentIDs) <= level:
                parentIDs.append('')
            parentIDs[level] = adc_id
            # clone list to avoid unexpected modification
            record['parent'] = parentIDs[:-1][:]
        else:
            # clone list to avoid unexpected modification
            record['parent'] = parentIDs[:]
        adcDict[adc_id] = record
        if len(record['parent']) > 0:
            parent_id = record['parent'][-1]
            adcDict[parent_id]['children'].append(adc_id)

    with open(out_file, 'w', encoding='utf_8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(adc_records[1].keys()))
        writer.writeheader()
        writer.writerows(adc_records)

    name_header = ['en','ja','zh','nl']
    nameDict = {}
    with open(name_file, encoding=ncdng, newline='') as f:
        reader = csv.reader(f)  # , delimiter='\t')
        next(reader)
        for cols in reader:
            record = {}
            for i in range(len(cols)):
                col = cols[i]
                record[name_header[i]] = re.sub('\s+', ' ', col).strip()
            name_en = record['en']
            if name_en not in nameDict:
                nameDict[name_en] = {
                    'ja':record['ja'],
                    'zh':record['zh'],
                    'nl':record['nl']
                }

    roleMap = {}

    for adc_id, record in adcDict.items():
        kind  = record['kind']
        level = record['level']
        den   = getSC_DEN(adc_id)
        if kind in ['ABIE', 'ACC']:
            link_id = adc_id
            den     = getSC_DEN(link_id)
            role_id = f'l_{link_id}'
            URI     = f'/{role_id}'
            roleMap[link_id] = {'adc_id': link_id, 'link_id': link_id,
                                'URI': URI, 'role_id': role_id, 'den': den}

    if DEBUG:
        print(roleMap)
    ###################################
    # core.xsd
    #

    def get_element_datatype(adc_id, type, kind):
        if not type:
            type = 'xbrli:stringItemType'
            if DEBUG:
                print(f'{adc_id} [{kind}] type not defined.')
        elif not 'xbrli:' in type and not 'adc:' in type:
            if not type:
                type = 'xbrli:stringItemType'
                if DEBUG:
                    print(f'{adc_id} [{kind}] type not defined.')
            else:
                type = F'adc:{type}'
        return type

    def defineElement(adc_id, record):
        global lines
        global elementsDefined
        if not adc_id in elementsDefined:
            elementsDefined.add(adc_id)
            if not record:
                print(f'NOT DEFINED {adc_id} record')
                return
            kind = record['kind']
            datatype = record['datatype']
            if datatype in datatypeMap:
                type = datatypeMap[datatype]['adc']
            else:
                type = 'stringItemType'
            if 'ABIE' == kind or adc_id in targetRefDict or adc_id in referenceDict:
                line = f'        <element name="{adc_id}" id="{adc_id}" abstract="true" type="xbrli:stringItemType" nillable="true" substitutionGroup="xbrli:item" xbrli:periodType="instant"/>\n'
            else:
                type = get_element_datatype(adc_id, type, kind)
                line = f'        <element name="{adc_id}" id="{adc_id}" type="{type}" nillable="false" substitutionGroup="xbrli:item" xbrli:periodType="instant"/>\n'
            lines.append(line)

    html_head = [
        '<?xml version="1.0" encoding="UTF-8"?>\n',
        '<!-- (c) 2022 XBRL Japan inc. -->\n',
        '<schema \n',
        '    targetNamespace="http://www.xbrl.jp/audit-data-collection" \n',
        '    elementFormDefault="qualified" \n',
        '    xmlns="http://www.w3.org/2001/XMLSchema" \n',
        '    xmlns:adc="http://www.xbrl.jp/audit-data-collection" \n',
        '    xmlns:xlink="http://www.w3.org/1999/xlink" \n',
        '    xmlns:link="http://www.xbrl.org/2003/linkbase" \n',
        '    xmlns:xbrli="http://www.xbrl.org/2003/instance" \n',
        '    xmlns:xbrldt="http://xbrl.org/2005/xbrldt"> \n',
        '    <import namespace="http://www.xbrl.org/2003/instance" schemaLocation="http://www.xbrl.org/2003/xbrl-instance-2003-12-31.xsd"/>\n',
        '    <import namespace="http://xbrl.org/2005/xbrldt" schemaLocation="http://www.xbrl.org/2005/xbrldt-2005.xsd"/>\n',
        '    <import namespace="http://www.xbrl.org/dtr/type/numeric" schemaLocation="http://www.xbrl.org/dtr/type/numeric-2009-12-16.xsd"/>\n',
        '    <import namespace="http://www.xbrl.org/dtr/type/non-numeric" schemaLocation="http://www.xbrl.org/dtr/type/nonNumeric-2009-12-16.xsd"/>\n']
    lines = html_head
    html_annotation_head = [
        '    <annotation>\n',
        '        <appinfo>\n',
        '            <link:linkbaseRef xlink:type="simple" xlink:role="http://www.xbrl.org/2003/role/labelLinkbaseRef" xlink:arcrole="http://www.w3.org/1999/xlink/properties/linkbase" xlink:href="core-lbl-en.xml"/>\n',
        '            <link:linkbaseRef xlink:type="simple" xlink:role="http://www.xbrl.org/2003/role/presentationLinkbaseRef" xlink:arcrole="http://www.w3.org/1999/xlink/properties/linkbase" xlink:href="core-pre.xml"/>\n',
        '            <link:linkbaseRef xlink:type="simple" xlink:role="http://www.xbrl.org/2003/role/definitionLinkbaseRef" xlink:arcrole="http://www.w3.org/1999/xlink/properties/linkbase" xlink:href="core-def.xml"/>\n',
    ]
    lines += html_annotation_head
    html = [
        '            <!-- \n',
        '                role type\n',
        '            -->\n'
        f'            <link:roleType id="audit-data-collection-role" roleURI="http://www.xbrl.jp/audit-data-collection/role">\n',
        f'                <link:definition>link audit-data-collection</link:definition>\n',
        f'                <link:usedOn>link:definitionLink</link:usedOn>\n',
        f'                <link:usedOn>link:presentationLink</link:usedOn>\n',
        '            </link:roleType>\n',
    ]
    for adc_id, role in roleMap.items():
        role_id = role["role_id"]
        URI = role['URI']
        link_id = role['link_id']
        den = role["den"]
        if re.match(r'^.*[A-z]{2}[0-9]{2}$', adc_id):
            html.append(
                f'            <link:roleType id="{role_id}" roleURI="http://www.xbrl.jp/audit-data-collection/role{URI}">\n')
            html.append(
                f'                <link:definition>{den}</link:definition>\n')
            html.append(
                f'                <link:usedOn>link:definitionLink</link:usedOn>\n')
            html.append('            </link:roleType>\n')
        else:
            source_den = den[:den.index(':')]
            target_den = den[den.index(':')+1:]
            html.append(
                f'            <link:roleType id="{role_id}" roleURI="http://www.xbrl.jp/audit-data-collection/role{URI}">\n')
            html.append(
                f'                <link:definition>{source_den} to {target_den}</link:definition>\n')
            html.append(
                f'                <link:usedOn>link:definitionLink</link:usedOn>\n')
            html.append('            </link:roleType>\n')
    lines += html

    html = [
        '            <!--\n',
        '                description: roleType arcroleType\n',
        '            -->\n'
        '            <link:roleType id="description" roleURI="http://www.xbrl.jp/audit-data-collection/role/description">\n',
        '                <link:definition>description</link:definition>\n',
        '                <link:usedOn>link:label</link:usedOn>\n',
        '            </link:roleType>\n',
        '            <link:arcroleType id="concept-description" cyclesAllowed="undirected" arcroleURI="http://www.xbrl.jp/audit-data-collection/arcrole/concept-description">\n',
        '                <link:definition>concept to description</link:definition>\n',
        '                <link:usedOn>link:labelArc</link:usedOn>\n',
        '            </link:arcroleType >\n',
    ]
    lines += html

    html = [
        '            <!--\n',
        '                primary key: roleType arcroleType\n',
        '            -->\n'
        '            <link:roleType id="primary-key" roleURI="http://www.xbrl.jp/audit-data-collection/role/primary-key">\n',
        '                <link:definition>primary key</link:definition>\n',
        '                <link:usedOn>link:definitionLink</link:usedOn>\n',
        '            </link:roleType>\n',
        '            <link:arcroleType id="concept-primary-key" cyclesAllowed="undirected" arcroleURI="http://www.xbrl.jp/audit-data-collection/arcrole/concept-primary-key">\n',
        '                <link:definition>concept primary key</link:definition>\n',
        '                <link:usedOn>link:definitionArc</link:usedOn>\n',
        '            </link:arcroleType >\n',
    ]
    lines += html

    html = [
        '            <!--\n',
        '                reference identifier: roleType arcroleType\n',
        '            -->\n'
        '            <link:roleType id="reference-identifier" roleURI="http://www.xbrl.jp/audit-data-collection/role/reference-identifier">\n',
        '                <link:definition>reference identifier</link:definition>\n',
        '                <link:usedOn>link:definitionLink</link:usedOn>\n',
        '            </link:roleType>\n',
        '            <link:arcroleType id="concept-reference-identifier" cyclesAllowed="undirected" arcroleURI="http://www.xbrl.jp/audit-data-collection/arcrole/concept-reference-identifier">\n',
        '                <link:definition>concept reference identifier</link:definition>\n',
        '                <link:usedOn>link:definitionArc</link:usedOn>\n',
        '            </link:arcroleType >\n',
    ]
    lines += html

    html = [
        '            <!--\n',
        '                require: roleType\n',
        '            -->\n'
        '            <link:roleType id="require" roleURI="http://www.xbrl.jp/audit-data-collection/role/require">\n',
        '                <link:definition>require</link:definition>\n',
        '                <link:usedOn>link:definitionLink</link:usedOn>\n',
        '            </link:roleType>\n',
    ]
    lines += html

    html_annotation_tail = [
        '        </appinfo>\n',
        '    </annotation>\n'
    ]
    lines += html_annotation_tail

    html_type = [
        '    <!-- typed dimension referenced element -->\n',
        '    <element name="_v" id="_v">\n',
        '        <simpleType>\n',
        '            <restriction base="string"/>\n',
        '        </simpleType>\n',
        '    </element>\n',
        '    <element name="_activity" id="_activity">',
        '        <simpleType>',
        '            <restriction base="string">',
        '                <pattern value="\s*(Created|Approved|LastModified|Entered|Posted)\s*"/>',
        '            </restriction>',
        '        </simpleType>',
        '    </element>'
    ]
    lines += html_type

    html_hypercube = [
        '    <!-- Hypercube -->\n'
    ]
    # Hypercube
    for adc_id, role in roleMap.items():
        link_id = role['link_id']
        html_hypercube.append(
            f'    <element name="h_{link_id}" id="h_{link_id}" substitutionGroup="xbrldt:hypercubeItem" type="xbrli:stringItemType" nillable="true" abstract="true" xbrli:periodType="instant"/>\n')
    lines += html_hypercube

    html_dimension = [
        '    <!-- Dimension -->\n'
    ]
    # Dimension
    for adc_id, role in roleMap.items():
        link_id = role['link_id']
        html_dimension.append(
            f'    <element name="d_{link_id}" id="d_{link_id}" substitutionGroup="xbrldt:dimensionItem" type="xbrli:stringItemType" abstract="true" xbrli:periodType="instant" xbrldt:typedDomainRef="#_v"/>\n')
    lines += html_dimension

    html_itemtype = [
        '    <!-- item type -->\n'
    ]
    # complexType
    complexType = [
        '        <complexType name="stringItemType">\n',
        '            <simpleContent>\n',
        '                <restriction base="xbrli:stringItemType"/>\n',
        '            </simpleContent>\n',
        '        </complexType>\n',
    ]
    html_itemtype += complexType
    for name, type in datatypeMap.items():
        adc = type['adc']
        xbrli = type['xbrli']
        complexType = [
            f'        <complexType name="{adc}">\n',
            '            <simpleContent>\n',
            f'                <restriction base="xbrli:{xbrli}"/>\n',
            '            </simpleContent>\n',
            '        </complexType>\n',
        ]
        html_itemtype += complexType
    lines += html_itemtype
    # element
    lines.append('    <!-- element -->\n')
    elementsDefined = set()
    primaryKeys = {}
    for record in adcDict.values():
        adc_id = record['adc_id']
        kind = record['kind']
        referenced_id = None
        defineElement(adc_id, record)
        if 'PKBIE' == kind:
            primaryKeys[adc_id[:4]] = adc_id

    for link_id, role in roleMap.items():
        if '-' not in link_id:
            continue
        index = link_id.rindex('-')
        adc_id = link_id[1+index:]
        record = getRecord(adc_id)
        if not record:
            defineElement(adc_id, record)

    lines.append('</schema>')

    adc_xsd_file = file_path(f'{xbrl_base}{core_xsd}')
    with open(adc_xsd_file, 'w', encoding=ncdng, newline='') as f:
        f.writelines(lines)
    if VERBOSE:
        print(f'-- {adc_xsd_file}')

    ###################################
    # labelLink en
    #
    def linkLabel(adc_id, name, description):
        global locsDefined
        global definedLabels
        global arcsDefined
        global definedDescs
        global definedDescArcs
        lines.append(f'        <!-- {adc_id} {name} -->\n')
        if not adc_id in locsDefined:
            locsDefined[adc_id] = adc_id
            line = f'        <link:loc xlink:type="locator" xlink:href="{core_xsd}#{adc_id}" xlink:label="{adc_id}" xlink:title="{adc_id}"/>\n'
        else:
            line = f'            <!-- link:loc defined -->\n'
        lines.append(line)
        # name
        if not adc_id in definedLabels:
            definedLabels[adc_id] = adc_id
            line = f'        <link:label xlink:type="resource" xlink:label="label_{adc_id}" xlink:title="label_{adc_id}" id="label_{adc_id}_en" xml:lang="en" xlink:role="http://www.xbrl.org/2003/role/label">{name}</link:label>\n'
            lines.append(line)
            if name in nameDict:
                name_ja = nameDict[name]['ja']
                line = f'        <link:label xlink:type="resource" xlink:label="label_{adc_id}" xlink:title="label_{adc_id}" id="label_{adc_id}_ja" xml:lang="ja" xlink:role="http://www.xbrl.org/2003/role/label">{name_ja}</link:label>\n'
                lines.append(line)
                name_zh = nameDict[name]['zh']
                line = f'        <link:label xlink:type="resource" xlink:label="label_{adc_id}" xlink:title="label_{adc_id}" id="label_{adc_id}_zh" xml:lang="zh" xlink:role="http://www.xbrl.org/2003/role/label">{name_zh}</link:label>\n'
                lines.append(line)
                name_nl = nameDict[name]['nl']
                line = f'        <link:label xlink:type="resource" xlink:label="label_{adc_id}" xlink:title="label_{adc_id}" id="label_{adc_id}_nl" xml:lang="nl" xlink:role="http://www.xbrl.org/2003/role/label">{name_nl}</link:label>\n'
                lines.append(line)
        else:
            line = f'            <!-- link:label http://www.xbrl.org/2003/role/label defined -->\n'
            lines.append(line)
        if not adc_id in arcsDefined:
            arcsDefined[adc_id] = adc_id
            line = f'        <link:labelArc xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label" xlink:from="{adc_id}" xlink:to="label_{adc_id}" xlink:title="label: {adc_id} to label_{adc_id}"/>\n'
        else:
            line = f'            <!-- link:labelArc http://www.xbrl.org/2003/arcrole/concept-label defined -->\n'
        lines.append(line)
        # description
        if description:
            description = description.replace('\\n','&#13;&#10;')
            if not adc_id in definedDescs:
                definedDescs[adc_id] = adc_id
                line = f'        <link:label xlink:type="resource" xlink:label="description_{adc_id}" xlink:title="description_{adc_id}" id="description_{adc_id}" xml:lang="en" xlink:role="http://www.xbrl.jp/audit-data-collection/role/description">{description}</link:label>\n'
            else:
                line = f'            <!-- link:label http://www.xbrl.jp/audit-data-collection/role/description defined -->\n'
            lines.append(line)
            if not adc_id in definedDescArcs:
                definedDescArcs[adc_id] = adc_id
                line = f'        <link:labelArc xlink:type="arc" xlink:arcrole="http://www.xbrl.jp/audit-data-collection/arcrole/concept-description" xlink:from="{adc_id}" xlink:to="description_{adc_id}" xlink:title="label: {adc_id} to label_{adc_id}"/>\n'
            else:
                line = f'            <!-- link:labelArc http://www.xbrl.jp/audit-data-collection/arcrole/concept-description defined -->\n'
            lines.append(line)

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>\n',
        '<!--  (c) 2022 XBRL Japan inc. -->\n',
        '<link:linkbase\n',
        '    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n',
        '    xmlns:link="http://www.xbrl.org/2003/linkbase"\n',
        '    xmlns:xlink="http://www.w3.org/1999/xlink"\n',
        '    xsi:schemaLocation="http://www.xbrl.org/2003/linkbase http://www.xbrl.org/2003/xbrl-linkbase-2003-12-31.xsd">\n',
        f'    <link:roleRef roleURI="http://www.xbrl.jp/audit-data-collection/role/description" xlink:type="simple" xlink:href="{core_xsd}#description"/>\n',
        f'    <link:arcroleRef arcroleURI="http://www.xbrl.jp/audit-data-collection/arcrole/concept-description" xlink:type="simple" xlink:href="{core_xsd}#concept-description"/>\n',
        '    <link:labelLink xlink:type="extended" xlink:role="http://www.xbrl.org/2003/role/link">\n'
    ]
    locsDefined = {}
    arcsDefined = {}
    definedLabels = {}
    definedDescs = {}
    definedDescArcs = {}
    for record in adcDict.values():
        adc_id = record['adc_id']
        kind   = record['kind']
        name   = record['name']
        if 'description' in record:
            description = record['description']
        else:
            description = ''
        linkLabel(adc_id, name, description)

    lines.append('    </link:labelLink>\n')
    lines.append('</link:linkbase>\n')

    adc_label_file = file_path(f'{xbrl_base}{core_label}-en.xml')
    with open(adc_label_file, 'w', encoding=ncdng, newline='') as f:
        f.writelines(lines)
    if VERBOSE:
        print(f'-- {adc_label_file}')

    ###################################
    #   presentationLink
    #
    locsDefined = {}
    arcsDefined = {}
    count = 0

    def linkPresentation(adc_id, children):
        global lines
        global count
        global locsDefined
        global arcsDefined
        if not adc_id:
            return
        record = getRecord(adc_id)
        if not record:
            return
        name = record['name']
        if not adc_id in locsDefined:
            locsDefined[adc_id] = name
            lines.append(f'        <!-- {kind} {adc_id} {name} -->\n')
            lines.append(
                f'        <link:loc xlink:type="locator" xlink:href="{core_xsd}#{adc_id}" xlink:label="{adc_id}" xlink:title="presentation: {adc_id} {name}"/>\n')
        for child_id in children:
            child = getRecord(child_id)
            if not child:
                continue
            child_kind = child['kind']
            child_name = child['name']
            if 'ASBIE' == child_kind:
                if not child_id in locsDefined:
                    locsDefined[child_id] = child_name
                    lines.append(
                        f'        <link:loc xlink:type="locator" xlink:href="{core_xsd}#{child_id}" xlink:label="{child_id}" xlink:title="presentation parent: {child_id} {child_name}"/>\n')
                arc_id = F'{adc_id} {child_id}'
                if not arc_id in arcsDefined and adc_id != child_id:
                    arcsDefined[arc_id] = f'{name} to {child_name}'
                    count += 1
                    lines.append(
                        f'        <link:presentationArc xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child" xlink:from="{adc_id}" xlink:to="{child_id}" order="{count}" xlink:title="presentation: {adc_id} {name} to {child_id} {child_name}"/>\n')
                    if 'children' in child and (len(child['children']) > 0 or child['target_id']):
                        grand_children = child['children'] or [
                            child['target_id']]
                        linkPresentation(child_id, grand_children)
            else:
                if not child_id in locsDefined:
                    locsDefined[child_id] = child_name
                    lines.append(
                        f'        <link:loc xlink:type="locator" xlink:href="{core_xsd}#{child_id}" xlink:label="{child_id}" xlink:title="presentation parent: {child_id} {child_name}"/>\n')
                arc_id = F'{adc_id} {child_id}'
                if not arc_id in arcsDefined and adc_id != child_id:
                    arcsDefined[arc_id] = f'{name} to {child_name}'
                    count += 1
                    lines.append(
                        f'        <link:presentationArc xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child" xlink:from="{adc_id}" xlink:to="{child_id}" order="{count}" xlink:title="presentation: {adc_id} {name} to {child_id} {child_name}"/>\n')
                    if 'children' in child and len(child['children']) > 0:
                        grand_children = child['children']
                        linkPresentation(child_id, grand_children)
        children = None

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>\n',
        '<!--  (c) 2022 XBRL Japan inc. -->\n',
        '<link:linkbase\n',
        '    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n',
        '    xsi:schemaLocation="http://www.xbrl.org/2003/linkbase http://www.xbrl.org/2003/xbrl-linkbase-2003-12-31.xsd"\n',
        '    xmlns:link="http://www.xbrl.org/2003/linkbase"\n',
        '    xmlns:xlink="http://www.w3.org/1999/xlink">\n',
        f'    <link:roleRef roleURI="http://www.xbrl.jp/audit-data-collection/role" xlink:type="simple" xlink:href="{core_xsd}#audit-data-collection-role"/>\n'
    ]
    locsDefined = {}
    arcsDefined = {}
    lines.append(
        '    <link:presentationLink xlink:type="extended" xlink:role="http://www.xbrl.jp/audit-data-collection/role">\n')
    records = [x for x in records if 'ABIE' == x['kind']]
    for record in adcDict.values():
        adc_id = record['adc_id']
        kind = record['kind']
        count = 0
        children = record['children']
        linkPresentation(adc_id, children)
    lines.append('    </link:presentationLink>\n')
    lines.append('</link:linkbase>\n')

    adc_presentation_file = file_path(f'{xbrl_base}{core_presentation}.xml')
    with open(adc_presentation_file, 'w', encoding=ncdng, newline='') as f:
        f.writelines(lines)
    if VERBOSE:
        print(f'-- {adc_presentation_file}')

    ###################################
    # definitionLink
    #
    locsDefined = {}
    arcsDefined = {}
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>\n',
        '<!--(c) 2022 XBRL Japan inc. -->\n',
        '<link:linkbase\n',
        '    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n',
        '    xsi:schemaLocation="http://www.xbrl.org/2003/linkbase http://www.xbrl.org/2003/xbrl-linkbase-2003-12-31.xsd"\n',
        '    xmlns:link="http://www.xbrl.org/2003/linkbase"\n',
        '    xmlns:xbrldt="http://xbrl.org/2005/xbrldt"\n',
        '    xmlns:xlink="http://www.w3.org/1999/xlink">\n'
    ]
    lines.append('    <!-- roleRef -->\n')
    for role in roleMap.values():
        role_id = role["role_id"]
        link_id = role['link_id']
        URI = f"/{role_id}"
        lines.append(
            f'    <link:roleRef roleURI="http://www.xbrl.jp/audit-data-collection/role{URI}" xlink:type="simple" xlink:href="{core_xsd}#{role_id}"/>\n')
    html = [
        f'    <link:roleRef roleURI="http://www.xbrl.jp/audit-data-collection/role/primary-key" xlink:type="simple" xlink:href="{core_xsd}#primary-key"/>\n',
        f'    <link:roleRef roleURI="http://www.xbrl.jp/audit-data-collection/role/reference-identifier" xlink:type="simple" xlink:href="{core_xsd}#reference-identifier"/>\n',
        f'    <link:roleRef roleURI="http://www.xbrl.jp/audit-data-collection/role/require" xlink:type="simple" xlink:href="{core_xsd}#require"/>\n',
        '    <!-- arcroleRef -->\n',
        '    <link:arcroleRef arcroleURI="http://xbrl.org/int/dim/arcrole/all" xlink:type="simple" xlink:href="http://www.xbrl.org/2005/xbrldt-2005.xsd#all"/>\n',
        '    <link:arcroleRef arcroleURI="http://xbrl.org/int/dim/arcrole/domain-member" xlink:type="simple" xlink:href="http://www.xbrl.org/2005/xbrldt-2005.xsd#domain-member"/>\n',
        '    <link:arcroleRef arcroleURI="http://xbrl.org/int/dim/arcrole/hypercube-dimension" xlink:type="simple" xlink:href="http://www.xbrl.org/2005/xbrldt-2005.xsd#hypercube-dimension"/>\n',
        '    <link:arcroleRef arcroleURI="http://xbrl.org/int/dim/arcrole/dimension-domain" xlink:type="simple" xlink:href="http://www.xbrl.org/2005/xbrldt-2005.xsd#dimension-domain"/>\n',
        f'    <link:arcroleRef arcroleURI="http://www.xbrl.jp/audit-data-collection/arcrole/concept-primary-key" xlink:type="simple" xlink:href="{core_xsd}#concept-primary-key"/>\n',
        f'    <link:arcroleRef arcroleURI="http://www.xbrl.jp/audit-data-collection/arcrole/concept-reference-identifier" xlink:type="simple" xlink:href="{core_xsd}#concept-reference-identifier"/>\n',
    ]
    lines += html

    for adc_id, role in roleMap.items():
        defineHypercube(adc_id, role, 2)

    lines.append('</link:linkbase>\n')

    adc_definition_file = file_path(f'{xbrl_base}{core_definition}.xml')
    with open(adc_definition_file, 'w', encoding=ncdng, newline='') as f:
        f.writelines(lines)
    if VERBOSE:
        print(f'-- {adc_definition_file}')

    print('** END **')
