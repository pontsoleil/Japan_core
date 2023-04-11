#!/usr/bin/env python3
# coding: utf-8
#
# generate Audit Data Collection xBRL-GD Taxonomy fron CSV file and header files
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

# from jsonschema import validate
from cgi import print_directory
# from distutils.debug import DEBUG
# import json
# from pyrsistent import b
import argparse
import os
# import yaml
import sys
import csv
import re
# import hashlib
# import datetime

DEBUG = False
VERBOSE = True
SEP = os.sep

LEN_KEY = 4
LEN_NUM = 2

xbrl_source = 'data/base/'
xbrl_source = xbrl_source.replace('/', SEP)
core_head = 'corehead.txt'
primarykey_file = 'primarykey.csv'

xbrl_base = 'data/xbrl/'
# xbrl_base = xbrl_base.replace('/', SEP)
core_xsd = 'core.xsd'
core_label = 'core-lbl'
core_presentation = 'core-pre'
core_definition = 'core-def'
core_for_Card = 'core-for-Card'
core_for_Mandatory = 'core-for-Mandatory'

# shared_yaml = None

datatypeMap = {
    'Amount': {
        'adc':'amountItemType',
        'xbrli':'monetaryItemType'},
    'Binary Object': {
        'adc':'binaryObjectItemType',
        'xbrli':'stringItemType'},
    'Code': {
        'adc':'codeItemType',
        'xbrli':'tokenItemType'},
    'Date': {
        'adc':'dateItemType',
        'xbrli':'dateItemType'},
    'Document Reference': {
        'adc':'documentReferenceItemType',
        'xbrli':'tokenItemType'},
    'Identifier': {
        'adc':'identifierItemType',
        'xbrli':'tokenItemType'},
    'Indicator': {
        'adc':'indicatorItemType',
        'xbrli':'booleanItemType'},
    'Text': {
        'adc':'textItemType',
        'xbrli':'stringItemType'},
    'Time': {
        'adc':'timeItemType',
        'xbrli':'timeItemType'},
    'Percentage': {
        'adc':'percentageItemType',
        'xbrli':'pureItemType'},
    'Quantity': {
        'adc':'quantityItemType',
        'xbrli':'intItemType'},
    'Unit Price Amount': {
        'adc':'unitPriceAmountItemType',
        'xbrli':'monetaryItemType'},
 }

abbreviationMap = {
    'ACC':'Account',
    'ADJ':'Adjustment',
    'BAS':'Base',
    'BEG':'Beginning',
    'CUR':'Currency',
    'CUS':'Customer',
    'FOB':'Free On Board',
    'FS':'Financial Statement',
    'INV':'Inventory',
    'IT':'Information Technology',
    'JE':'Journal Entry',
    'NUM':'Number',
    'ORG':'Organization',
    'PK':'Primary Key',
    'PO':'Purchase Order',
    'PPE':'Property, Plant and Equipment',
    'PRV':'Province',
    'PUR':'Purchase',
    'REF':'Reference Identifier',
    'RFC':'Request For Comments',
    'SAL':'Sales',
    'TIN':'Tax Identification Number',
    'TRX':'Transactional',
    'UOM':'Unit of Measurement',
    'WIP':'Work In Progress'
}

targetTables = ['GL02','GL03']

duplicateNames = set()
names = set()
adcDict = {}
targetRefDict = {}
associationDict = {}
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
        pathname = pathname.replace('/',SEP)
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

def titleCase(text):
    text = text.replace('ID', 'Identification Identifier')
    # ChatGPT 2023-04-10 modified by Nobu
    # Example Camel case string
    camel_case_str = text# "exampleCamelCaseString"
    # Use regular expression to split the string at each capital letter
    split_str = re.findall('[A-Z][a-z]*[_]?', camel_case_str)
    # Join the split string with a space and capitalize each word
    title_case_str = ' '.join([x.capitalize() for x in split_str])
    title_case_str = title_case_str.replace('Identification Identifier','ID')
    return title_case_str

# snake concatenate
def SC(term):
    if not term:
        return ''
    terms = term.split(' ')
    name = '_'.join(terms)
    return name

def getName(adc_id):
    record = getRecord(adc_id)
    if record:
        return record['name']
    return ''

def getDEN(adc_id):
    record = getRecord(adc_id)
    if record:
        return record['DEN']
    return ''

def getLC3_DEN(adc_id):
    den = getDEN(adc_id)
    if den:
        den = den[:den.find('.')]
        return LC3(den)
    return ''

# def getClassName(adc_id):
#     den = getDEN(adc_id)
#     if den:
#         cn = den[1+LEN_KEY:den.find('.')]
#         return cn
#     return ''

def getRecord(adc_id):
    if adc_id in adcDict:
        record = adcDict[adc_id]
    else:
        target_id = adc_id[-LEN_KEY:]
        if target_id in adcDict:
            record = adcDict[target_id] #2023-02-06
        else:
            record = None
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
    if record:
        return record['children']
    return []

def defineHypercube(adc_id, role,n):
    global lines
    global locsDefined
    global arcsDefined
    global targetRefDict
    global referenceDict
    root_id = None
    root_id = adc_id
    root = getRecord(root_id)
    if not root:
        print(f'** {root_id} is not defined.')
        return None
    anchor_id = None
    link_id = role['link_id']
    locsDefined[link_id] = set()
    arcsDefined[link_id] = set()
    URI = role['URI']
    role_id = role['role_id']
    hypercube_id = f"h_{link_id}"
    dimension_id_list = set()
    source_id = None
    origin_id = None
    if LEN_KEY==len(adc_id):
        root_dimension = f"d_{root_id}"
        dimension_id_list.add(root_dimension)
    elif 1+2*LEN_KEY==len(adc_id):
        root_id = link_id[-LEN_KEY:]
        root_dimension_id = f'd_{root_id}'
        dimension_id_list.add(root_dimension_id)
        root = getRecord(root_id)
        source_id = link_id[:LEN_KEY]
        source_dimension = f'd_{source_id}'
        dimension_id_list.add(source_dimension)
        # anchor_id = [x for x in sourceRefDict[root_id]['source'] if source_id==x[:LEN_KEY]][0]
        if source_id in sourceRefDict:
            origin = sourceRefDict[source_id]
            origin_id = origin['source'][0]
            origin_id = origin_id[:LEN_KEY]
            anchor_id = f'{origin_id}-{anchor_id}'
            origin_dimension = f'd_{origin_id}'
            dimension_id_list.add(origin_dimension)
    lines.append(f'    <link:definitionLink xlink:type="extended" xlink:role="http://www.xbrl.jp/audit-data-collection/role{URI}">\n')
    # all (has-hypercube)
    lines.append(f'        <!-- {link_id} all (has-hypercube) {hypercube_id} {role_id} -->\n')
    lines.append(f'        <link:loc xlink:type="locator" xlink:href="{core_xsd}#{link_id}" xlink:label="{link_id}" xlink:title="{link_id}"/>\n')
    lines.append(f'        <link:loc xlink:type="locator" xlink:href="{core_xsd}#{hypercube_id}" xlink:label="{hypercube_id}" xlink:title="{hypercube_id}"/>\n')
    lines.append(f'        <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/all" xlink:from="{link_id}" xlink:to="{hypercube_id}" xlink:title="all (has-hypercube): {link_id} to {hypercube_id}" order="1" xbrldt:closed="true" xbrldt:contextElement="scenario"/>\n')
    if DEBUG:
        print(f'all(has-hypercube) {link_id} to {hypercube_id} ')
    # hypercube-dimension
    lines.append('        <!-- hypercube-dimension -->\n')
    count = 0
    for dimension_id in dimension_id_list:
        lines.append(f'        <link:loc xlink:type="locator" xlink:href="{core_xsd}#{dimension_id}" xlink:label="{dimension_id}" xlink:title="{dimension_id}"/>\n')
        count += 1
        lines.append(f'        <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/hypercube-dimension" xlink:from="{hypercube_id}" xlink:to="{dimension_id}" xlink:title="hypercube-dimension: {hypercube_id} to {dimension_id}" order="{count}"/>\n')
        if DEBUG:
            print(f'hypercube-dimension {hypercube_id} to {dimension_id} ')
    # domain-member
    lines.append('        <!-- domain-member -->\n')
    count = 0
    if 'children' in root and len(root['children']) > 0:
        children =  root['children']
        for child_id in children:
            # alias_id = not link_id[:LEN_KEY] in child_id and f"{link_id[:LEN_KEY]}-{child_id}" or child_id
            # alias_id = child_id
            child = getRecord(child_id)#[-8:])
            child_kind = child['kind']
            if child_id in targetRefDict:
                if 'ASBIE'!=child_kind or 'n'!=child['occMax']:
                    if not child_id in locsDefined[link_id]:
                        locsDefined[link_id].add(child_id)
                        lines.append(f'        <link:loc xlink:type="locator" xlink:href="{core_xsd}#{child_id}" xlink:label="{child_id}" xlink:title="{child_id}"/>\n')
                    count += 1
                    arc_id = f'{link_id} {child_id}'
                    if not arc_id in arcsDefined[link_id]:
                        arcsDefined[link_id].add(arc_id)
                        lines.append(f'        <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="{link_id}" xlink:to="{child_id}" xlink:title="domain-member: {link_id} to {child_id}" order="{count}"/>\n')
                # targetRole
                # target_id = targetRefDict[child_id]
                # role_id = f'link_{child_id[:LEN_KEY]}-{target_id}'
                role_id = f'link_{child_id}'
                URI = f'/{role_id}'
                lines.append(f'        <!-- {child_id} targetRole {role_id} -->\n')
                if not target_id in locsDefined[link_id]:
                    locsDefined[link_id].add(child_id)
                    lines.append(f'        <link:loc xlink:type="locator" xlink:href="{core_xsd}#{child_id}" xlink:label="{child_id}" xlink:title="{child_id}"/>\n')
                    # lines.append(f'        <link:loc xlink:type="locator" xlink:href="{core_xsd}#{target_id}" xlink:label="{target_id}" xlink:title="{target_id}"/>\n')
                count += 1
                arc_id = f'{link_id} {child_id}'
                # arc_id = f'{link_id} {target_id}'
                if not arc_id in arcsDefined[link_id]:
                    arcsDefined[link_id].add(arc_id)
                    lines.append(f'        <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xbrldt:targetRole="http://www.xbrl.jp/audit-data-collection/role{URI}" xlink:from="{link_id}" xlink:to="{child_id}" xlink:title="domain-member: {link_id} to {child_id} in {role_id}" order="{count}"/>\n')
                    # lines.append(f'        <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xbrldt:targetRole="http://www.xbrl.jp/audit-data-collection/role{URI}" xlink:from="{link_id}" xlink:to="{target_id}" xlink:title="domain-member: {link_id} to {target_id} in {role_id}" order="{count}"/>\n')
            else:
                if 'ASBIE'==child_kind and '1'==child['occMax']:
                    # targetRole
                    # target_id = child_id[-LEN_KEY:]
                    # role_id = f'link_{child_id[:LEN_KEY]}-{target_id}'
                    role_id = f'link_{child_id}'
                    URI = f'/{role_id}'
                    lines.append(f'        <!-- {child_id} targetRole {role_id} -->\n')
                    if not child_id in locsDefined[link_id]:
                        locsDefined[link_id].add(child_id)
                        lines.append(f'        <link:loc xlink:type="locator" xlink:href="{core_xsd}#{child_id}" xlink:label="{child_id}" xlink:title="{child_id}"/>\n')
                    # if not target_id in locsDefined[link_id]:
                    #     locsDefined[link_id].add(target_id)
                    #     lines.append(f'        <link:loc xlink:type="locator" xlink:href="{core_xsd}#{target_id}" xlink:label="{target_id}" xlink:title="{target_id}"/>\n')
                    count += 1
                    arc_id = f'{link_id} {child_id}'
                    # arc_id = f'{link_id} {target_id}'
                    if not arc_id in arcsDefined[link_id]:
                        arcsDefined[link_id].add(arc_id)
                        lines.append(f'        <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xbrldt:targetRole="http://www.xbrl.jp/audit-data-collection/role{URI}" xlink:from="{link_id}" xlink:to="{child_id}" xlink:title="domain-member: {link_id} to {child_id} in {role_id}" order="{count}"/>\n')
                        # lines.append(f'        <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xbrldt:targetRole="http://www.xbrl.jp/audit-data-collection/role{URI}" xlink:from="{link_id}" xlink:to="{target_id}" xlink:title="domain-member: {link_id} to {target_id} in {role_id}" order="{count}"/>\n')
                else:
                    if not child_id in locsDefined[link_id]:
                        locsDefined[link_id].add(child_id)
                        lines.append(f'        <link:loc xlink:type="locator" xlink:href="{core_xsd}#{child_id}" xlink:label="{child_id}" xlink:title="{child_id}"/>\n')
                    count += 1
                    arc_id = f'{link_id} {child_id}'
                    if not arc_id in arcsDefined[link_id]:
                        arcsDefined[link_id].add(arc_id)
                        lines.append(f'        <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="{link_id}" xlink:to="{child_id}" xlink:title="domain-member: {link_id} to {child_id}" order="{count}"/>\n')

                    # if not child_id in associationDict:
                    #     print(f'** {child_id} not in associationDict')
                    #     continue
                    # association_id = associationDict[child_id]
                    # association = getRecord(association_id)
                    # grand_children = association['children']
                    # for grand_child_id in grand_children:
                    #     grand_alias_id = not link_id[:LEN_KEY] in grand_child_id and f"{link_id[:LEN_KEY]}-{grand_child_id}" or grand_child_id
                    #     if not grand_alias_id in locsDefined[link_id]:
                    #         locsDefined[link_id].add(grand_alias_id)
                    #         lines.append(f'        <link:loc xlink:type="locator" xlink:href="{core_xsd}#{grand_alias_id}" xlink:label="{grand_alias_id}" xlink:title="{grand_alias_id}"/>\n')
                    #     count += 1
                    #     arc_id = f'{alias_id} {grand_alias_id}'
                    #     if not arc_id in arcsDefined[link_id]:
                    #         arcsDefined[link_id].add(arc_id)
                    #         lines.append(f'        <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="{alias_id}" xlink:to="{grand_alias_id}" xlink:title="domain-member: {alias_id} to {grand_alias_id}" order="{count}"/>\n')                    

    lines.append('    </link:definitionLink>\n')

def addChild(parent_id_list,adc_id):
    record = getRecord(adc_id)
    if not record:
        return
    parent = getParent(parent_id_list)
    if not parent:
        return
    if not adc_id in adcDict:
        print(adc_id)
    if not 'children' in parent:
        parent['children'] = []
    if not adc_id in parent['children']:
        parent['children'].append(adc_id)
        if DEBUG:
            print(f'   {parent_id_list} add {adc_id}')
    return adc_id

def addChildren(parent_id_list,adc_id):
    global targetRefDict
    global referenceDict
    record = getRecord(adc_id)
    if not record:
        return
    kind = record['kind']
    ref_id = None
    targetRef_id = None
    if kind in ['IDBIE','BBIE']:
        if DEBUG: print(f'(a) addChild( {parent_id_list}, {adc_id} )[{kind}]{getDEN(adc_id)}({adc_id})')
        addChild(parent_id_list,adc_id)
    elif 'RFBIE'==kind:
        if DEBUG: print(f'(a) addChild( {parent_id_list}, {adc_id} )[{kind}]{getDEN(adc_id)}({adc_id})')
        addChild(parent_id_list,adc_id)
    elif 'ABIE'==kind:
        if adc_id in associationDict:
            ref_id = associationDict[adc_id]
            if DEBUG: print(f'(b) addChild ( {parent_id_list}, {adc_id} )<{kind}>{getDEN(ref_id)}({ref_id})')
        elif adc_id in targetRefDict:
            targetRef_id =  targetRefDict[adc_id]
            if DEBUG: print(f'(c) addChild ( {parent_id_list}, {adc_id} )<{kind}>{getDEN(targetRef_id)}({targetRef_id})')
    elif 'ASBIE'==kind:# and 'n'==record['occMax']:
        record2 = None
        if adc_id in associationDict:
            ref_id = associationDict[adc_id]
            record2 = getRecord(ref_id)
            if DEBUG: print(f'(c) addChild( {parent_id_list}, {adc_id} )<{kind}>{getDEN(ref_id)}({ref_id})')
            addChild(parent_id_list,adc_id)
            parent_id_list += [adc_id]
        elif adc_id in targetRefDict:
            targetRef_id = targetRefDict[adc_id]
            record2 = getRecord(targetRef_id)
            if DEBUG: print(f'(c) addChild( {parent_id_list}, {adc_id} )<{kind}>{getDEN(targetRef_id)}({targetRef_id})')
            addChild(parent_id_list,adc_id)
            parent_id_list += [adc_id]
        else:
            associatedClass = record['associatedClass']
            for adc2_id,record2 in adcDict.items():
                if associatedClass==record2['class']:
                    targetRefDict[adc_id] = adc2_id
                    targetRef_id = adc2_id
                    addChild(parent_id_list,adc_id)
                    break
        if not record2 or not 'children' in record2:
            print(f'-ERROR- addChildren [{kind}] {adc_id}')
        children = record2['children']
        children0 = [x for x in children]
        for child_id in children0:
            child = getRecord(child_id)
            child_kind = child['kind']
            if 'ABIE'==child_kind:
                if DEBUG: print(f'(d) NOT ( {parent_id_list}, {child_id} )<{child_kind}>{getDEN(child_id)}({child_id})')
            if 'ASBIE'==child_kind:# and 'n'==child['occMax']:
                if DEBUG: print(f'(e)*addChildren( {parent_id_list}, {child_id} )<{child_kind}>{getDEN(child_id)}({child_id})')
                addChildren(parent_id_list,child_id)
            else:
                if not adc_id in parent_id_list: parent_id_list += [adc_id]
                if DEBUG: print(f'(f) addChild( {parent_id_list}, {child_id} )[{child_kind}]{getDEN(child_id)}({child_id})')
                addChild(parent_id_list,child_id)
    parent_id_list.pop()
    return adc_id

if __name__ == '__main__':
    # Create the parser
    parser = argparse.ArgumentParser(prog='ADCS_H2xBRL-taxonomy.py',
                                     usage='%(prog)s infile -o outfile -e encoding [options] ',
                                     description='Audit data collection 定義CSVファイルをxBRLタクソノミに変換')
    # Add the arguments
    parser.add_argument('inFile', metavar='infile', type=str, help='Audit data collection 定義CSVファイル')
    parser.add_argument('-o', '--outfile')  # core.xsd
    parser.add_argument('-e', '--encoding') # 'Shift_JIS' 'cp932' 'utf_8'
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-d', '--debug', action='store_true')

    args = parser.parse_args()
    in_file = None
    if args.inFile:
        in_file = args.inFile.strip()
        in_file = in_file.replace('/', SEP)
        in_file = file_path(args.inFile)
    if not in_file or not os.path.isfile(in_file):
        print('入力ADC定義CSVファイルがありません')
        sys.exit()
    adc_file = in_file
    if args.outfile:
        out_file = args.outfile.lstrip()
        out_file = out_file.replace('/', SEP)
        out_file = file_path(out_file)
        xbrl_base = os.path.dirname(out_file)
    xbrl_base = xbrl_base.replace('/', SEP)
    if not os.path.isdir(xbrl_base):
        print('タクソノミのディレクトリがありません')
        sys.exit()

    ncdng = args.encoding
    if ncdng:
        ncdng = ncdng.lstrip()
    else:
        ncdng = 'UTF-8'
    VERBOSE = args.verbose
    DEBUG = args.debug

    # ====================================================================
    # 1. audit_data_collection.csv -> schema
    def lookupModule(table_id):
        module = None
        prefix = table_id[:2]
        if 'NC'==prefix: module = 'Invoice'
        elif 'BS'==prefix: module = 'Base'
        elif 'GL'==prefix: module = 'GL'
        elif 'CM'==prefix: module = 'Common'
        return module

    records = []
    adc_file = file_path(adc_file)
    tableDict = {}
    classDict = {}
    asbieDict = {}

    # header = ['no','module','core_id','kind','table_id','class','level','occurrence','field_id','propertyTerm','representationQualifier','representation','associatedClass','datatype','term','desc']
    header = ['semSort','group','core_id','table_id','field_id','level','occurrence','term','kind','class','propertyTerm','representation','associatedClass','desc','UN_CCL_ID','smeKind','smeSeq','smeID','smeTerm','smeDesc','smeDefault','smeOccur','smeLevel','smeXPath','pintSort','pintID','pintOccur.','pintLevel','pintTerm','pintTermJA','pintDesc','pintDescJA','pintDefault','pintXPath']
    with open(adc_file, encoding='utf-8', newline='') as f:
        reader = csv.reader(f)#, delimiter='\t')
        next(reader)
        for cols in reader:
            record = {}
            for i in range(len(cols)):
                col = cols[i]
                record[header[i]] = col.strip()
            if not 'module' in record:
                record['module'] = 'Invoice'
            kind = record['kind']
            if not kind in ['ABIE','ASBIE']:
                module = record['module']
                cls = record['class']
                cls = titleCase(cls)
                if len(cls) > 0:
                    table_id = record['table_id']
                    tableDict[cls] = table_id
                    classDict[table_id] = cls

    with open(adc_file, encoding='utf-8', newline='') as f:
        reader = csv.reader(f)#, delimiter='\t')
        next(reader)
        this_class = None
        this_table_id = None
        for cols in reader:
            record = {}
            for i in range(len(cols)):
                col = cols[i]
                record[header[i]] = col.strip()
            if not 'module' in record:
                record['module'] = 'Invoice'
            adc_id = ''
            name = ''
            type = ''
            if not record['core_id']:
                continue
            kind = record['kind']
            cls = record['class']
            cls = titleCase(cls)
            term = record['term']
            occurrence = record['occurrence']
            if LEN_KEY==len(occurrence):
                record['occMin'] = occurrence[0]
                record['occMax'] = occurrence[-1]
            # if len(kind) > 1+LEN_KEY and 'IDBIE' == kind[:1+LEN_KEY]:
            #     kind = 'IDBIE'
            # record['kind'] = kind
            level = record['level']
            if re.match('[0-9]+',level):
                level = int(level)
            else:
                level = 0
            record['level'] = level
            if 'ABIE'==kind:
                adc_id = record['table_id']
            elif 'ASBIE'==kind:# and 'n'==record['occMax']:
                associatedClass = record['associatedClass']
                associatedClass = titleCase(associatedClass)
                adc_id = f"{record['table_id']}-{tableDict[associatedClass]}"
            else:
                adc_id = f"{record['table_id']}-{record['field_id'].zfill(2)}"
            # if kind == 'ABIE':
            #     record['parent'] = []
            #     parentIDs = [adc_id]
            # else:
            #     record['parent'] = parentIDs
            record['children'] = []
            record['adc_id'] = adc_id
            if 'ABIE'==kind:                
                DEN = f'{cls}. Details'
                record['DEN'] = DEN
                if adc_id in adcDict:
                    if DEBUG: print(f'** Duplicate {adc_id} is already in adcDict.')
                    continue
                record['name'] = titleCase(term)
                record['type'] = ''
                adcDict[adc_id] = record
                this_class = cls
                this_table_id = table_id
            else:
                propertyTerm = record['propertyTerm']
                propertyTerm = titleCase(propertyTerm)
                if kind in ['RFBIE','ASBIE']:
                    associatedClass = record['associatedClass']
                    associatedClass = titleCase(associatedClass)
                    DEN = f'{cls}. {propertyTerm}. {associatedClass}'
                else:
                    representationQualifier = ''
                    if'representationQualifier' in record:
                        representationQualifier = record['representationQualifier']
                        representationQualifier = titleCase(representationQualifier)
                    representation = record['representation']
                    representation = titleCase(representation)
                    if representationQualifier:
                        DEN = f'{cls}. {propertyTerm}. {representationQualifier}_ {representation}'
                    else:
                        DEN = f'{cls}. {propertyTerm}. {representation}'                
                record['DEN'] = DEN                
                # if level > 0:
                #     parent_id = parentIDs[level-1]
                # else:
                #     parent_id = ''
                record['name'] = term# propertyTerm
                representation = record['representation']                
                # if datatype in ['PK','REF']:
                #     type = datatypeMap['Identifier']['adc']
                # el
                if representation in datatypeMap:
                    type = datatypeMap[representation]['adc']
                else:
                    type = 'stringItemType'
                record['type'] = type
                # if parent_id and not adc_id in adcDict[parent_id]['children']:
                #     adcDict[parent_id]['children'].append(adc_id)
                #     if 1+2*LEN_KEY==len(parent_id):
                #         parent_id2 = parent_id[-LEN_KEY:]
                #         if 0==len(adcDict[parent_id2]['parent']):
                #             adcDict[parent_id2]['parent'] = parentIDs[:level-1]
                #         if not adc_id in adcDict[parent_id2]['children']:
                #             adcDict[parent_id2]['children'].append(adc_id)
                # adcDict[adc_id] = record
                # if 'ASBIE' == kind:
                #     while len(parentIDs) > level:
                #         parentIDs.pop()
                #     while len(parentIDs) <= level:
                #         parentIDs.append('')
                #     parentIDs[level] = adc_id
            if adc_id:
                adcDict[adc_id] = record
                records.append(record)
            if 'ASBIE' == kind and len(adc_id) == 1+2*LEN_KEY:
                d = {}
                for i in range(len(cols)):
                    col = cols[i]
                    d[header[i]] = ''
                table_id = adc_id[-LEN_KEY:]
                # d['no'] = record['no']
                d['module'] = lookupModule(table_id)
                d['kind'] = 'ABIE'
                d['level'] = level
                d['adc_id'] = table_id
                d['table_id'] = table_id
                d['class'] = classDict[table_id]
                d['field_id'] = '0'
                d['occurrence'] = '--'
                d['occMin'] = '-'
                d['occMax'] = '-'
                d['parent'] = []
                # d['children'] = []
                cls = d['class']
                cls = titleCase(cls)
                d['name'] = cls
                d['DEN'] = f'{cls}. Details'  
                adcDict[table_id] = d
                records.append(d)

    parentIDs = ['']*8
    for record in records:
        adc_id = record['adc_id']
        kind = record['kind']
        level = record['level']
        # if re.match('[0-9]+',level):
        #     level = int(level)
        # else:
        #     level = 0
        # record['level'] = level
        if 'ASBIE' == kind:
            # while len(parentIDs) > level:
            #     parentIDs.pop()
            # while len(parentIDs) <= level:
            #     parentIDs.append('')
            parentIDs[level] = adc_id
        if kind == 'ABIE':
            # record['parent'] = []
            parentIDs[level] = adc_id
        # else:
        #     record['parent'] = parentIDs[:level]
        if level > 0:
            parent_id = parentIDs[level-1]
        else:
            parent_id = ''
        record['parent'] = parentIDs[:level]
        if DEBUG: print(f'adcDict[{adc_id}][parent]={record["parent"]}')
        record['children'] = []
        adcDict[adc_id] = record
        if parent_id and not adc_id in adcDict[parent_id]['children'] and len(parent_id) > LEN_KEY:
            adcDict[parent_id]['children'].append(adc_id)
            # if 1+2*LEN_KEY==len(parent_id):
            #     parent_id2 = parent_id[-LEN_KEY:]
            #     if 0==len(adcDict[parent_id2]['parent']):
            #         adcDict[parent_id2]['parent'] = parentIDs[:level-1]
            #     if not adc_id in adcDict[parent_id2]['children']:
            #         adcDict[parent_id2]['children'].append(adc_id)

        

    targetRefDict = {}   # parent-child
    associationDict = {} # associatedClass
    for adc_id, record in adcDict.items():
        kind = record['kind']
        if not 'ABIE'==kind:
            continue
        # if not adc_id in targetTables and 'Core'!=record['module']: continue
        if DEBUG:
            print(f"=== {record['DEN']}")
        if 'children' in record:
            children = record['children']
            children0 = [x for x in children]
            for child_id in children0:
                child = getRecord(child_id)
                abieID = None
                idbieID = None
                if not child:
                    continue
                kind = child['kind']
                # if len(kind) > 1+LEN_KEY and 'IDBIE' == kind[:1+LEN_KEY]:
                #     kind = 'IDBIE'
                # if kind in ['BBIE','IDBIE','RFBIE']:
                #     continue
                    # if DEBUG: print(f'=1= addChild( {[adc_id]}, {child_id} )[{kind}]{getDEN(child_id)}')
                    # addChild([adc_id],child_id)
                    # if 'RFBIE'==kind:
                    #     if not child_id in referenceDict:
                    #         associatedClass = child['associatedClass']
                    #         idAs = [k for k,v in adcDict.items() if associatedClass==v['class'] and 'ABIE'==v['kind']]
                    #         if len(idAs) > 0:
                    #             abieID = idAs[0]
                    #         else:
                    #             if DEBUG: print(f'=X= NOT found associatedClass of ( {[adc_id]}, {child_id} )[{kind}]{getDEN(child_id)}({child_id})')
                    #             continue
                    #         idIs = [k for k,v in adcDict.items() if associatedClass==v['class'] and 'IDBIE'==v['kind']]
                    #         if len(idIs) > 0:
                    #             idbieID = idIs[0]
                    #         assocChildren = [k for k,v in adcDict.items() if associatedClass==v['class'] and 'ABIE'!=v['kind']]
                    #         for adc2_id in assocChildren:
                    #             record2 = adcDict[adc2_id]
                    #             if not child_id in referenceDict:
                    #                 referenceDict[child_id] = {}
                    #             referenceDict[child_id]['ABIE'] = abieID
                    #             referenceDict[child_id]['IDBIE'] = idbieID
                # el
                if 'ASBIE'==kind:# and 'n'==child['occMax']:
                    associatedClass = titleCase(child['associatedClass'])
                    # abieID = [k for k,v in adcDict.items() if associatedClass==v['class'] and 'ABIE'==v['kind']]
                    idAs = [k for k,v in adcDict.items() if associatedClass==v['class'] and 'ABIE'==v['kind']]
                    if len(idAs) > 0:
                        abieID = idAs[0]
                    else:
                        if DEBUG: print(f'=X= NOT found associatedClass of ( {[adc_id]}, {child_id} )[{kind}]{getDEN(child_id)}({child_id})')
                        continue
                    idIs = [k for k,v in adcDict.items() if associatedClass==v['class'] and 'IDBIE'==v['kind']]
                    if len(idIs) > 0:
                        idbieID = idIs[0]
                    if not child_id in referenceDict:
                        referenceDict[child_id] = {}
                    if abieID:
                        referenceDict[child_id]['ABIE']  = abieID
                    else:
                        print('** ABIE not defined.')
                    if idbieID:
                        referenceDict[child_id]['IDBIE'] = idbieID                    
                    if 'n' == child['occMax']:
                        targetRefDict[child_id] = abieID
                        if DEBUG: print(f'=2= {child_id} targetRef {abieID}')
                    else:
                        associationDict[child_id] = abieID
                        if DEBUG: print(f'=2= {child_id} associationDict {abieID}')
                    record2 = adcDict[abieID]
                    kind2 = record2['kind']
        #         elif DEBUG: print(f'=X= NOT ( {[adc_id]}, {child_id} )[{kind}]{getDEN(child_id)}({child_id})')
        # elif DEBUG: print(f'=X= NOT ( {[adc_id]}, {child_id} )[{kind}]{getDEN(child_id)}({child_id})')

    sourceRefDict = {}
    for source_id,target_id in targetRefDict.items():
        if not target_id in sourceRefDict:
            den = getLC3_DEN(target_id)
            sourceRefDict[target_id] = {'den':den, 'source':[]}
        sourceRefDict[target_id]['source'].append(source_id)

    repeatables = {}
    for adc_id, record in adcDict.items():
        kind = record['kind']
        if 'ABIE'==kind:
            continue
        if 'occMax' in record and 'n' == record['occMax']:
            parent_id = record['parent'][-1]
            if DEBUG: print(f"{adc_id} max occurence:{record['occMax']} parent:{parent_id}")
            if not parent_id in repeatables:
                den = getLC3_DEN(parent_id)
                repeatables[parent_id] = {'den':den, 'source':[]}
            repeatables[parent_id]['source'].append(adc_id)

    if DEBUG:
        print(repeatables)

    roleMap = {}

    for adc_id,record in adcDict.items():
        den = getLC3_DEN(adc_id)
        if 'ABIE'==record['kind'] and not adc_id in roleMap:
            link_id = adc_id
            den = getLC3_DEN(link_id)
            role_id = f'link_{link_id}'
            URI = f'/{role_id}'
            roleMap[link_id] = {'adc_id':link_id,'link_id':link_id,'URI':URI,'role_id':role_id,'den':den}

    for adc_id,target_id in targetRefDict.items():
        source_id = adc_id[:LEN_KEY]
        link_id = f'{source_id}-{target_id}'
        if link_id not in roleMap and source_id!=target_id:
            source_den = getLC3_DEN(source_id)
            target_den = getLC3_DEN(target_id)
            den = f'{source_den}-{target_den}'
            role_id = f'link_{link_id}'
            URI = f'/{role_id}'
            roleMap[link_id] = {'adc_id':adc_id,'link_id':link_id,'URI':URI,'role_id':role_id,'den':den}

    for adc_id,association in referenceDict.items():
        source_id = adc_id[:LEN_KEY]
        association_id = association['ABIE']
        link_id = f'{source_id}-{association_id}'
        if link_id not in roleMap and source_id!=association_id:
            source_den = getLC3_DEN(source_id)
            association_den = getLC3_DEN(association_id)
            den = f'{source_den}-{association_den}'
            role_id = f'link_{link_id}'
            URI = f'/{role_id}'
            roleMap[link_id] = {'adc_id':adc_id,'link_id':link_id,'URI':URI,'role_id':role_id,'den':den}

    ###################################
    # core.xsd
    #
    def get_element_datatype(adc_id,type,kind):
        if not type:
            type = 'xbrli:stringItemType'
            if DEBUG: print(f'{adc_id} [{kind}] type not defined.')
        elif not 'xbrli:' in type and not 'adc:'in type:
            if not type:
                type = 'xbrli:stringItemType'
                if DEBUG: print(f'{adc_id} [{kind}] type not defined.')
            else:
                type=F'adc:{type}'
        return type

    def defineElement(adc_id,record):
        global lines
        global elementsDefined
        if not adc_id in elementsDefined:
            elementsDefined.add(adc_id)
            if not record:
                print(f'NOT DEFINED {adc_id} record')
                return
            kind = record['kind']
            type = 'type' in record and record['type']  or ''
            if 'ABIE'==kind or adc_id in targetRefDict or adc_id in referenceDict:
                line = f'        <element name="{adc_id}" id="{adc_id}" abstract="true" type="xbrli:stringItemType" nillable="true" substitutionGroup="xbrli:item" xbrli:periodType="instant"/>\n'
            else:
                type = get_element_datatype(adc_id,type,kind)
                line = f'        <element name="{adc_id}" id="{adc_id}" type="{type}" nillable="false" substitutionGroup="xbrli:item" xbrli:periodType="instant"/>\n'
            lines.append(line) 

    def lookupPrimarykey(link_id):
        source_id = link_id[:LEN_KEY]
        adc_id = link_id[-LEN_KEY:]
        children = [record for record in records if adc_id==record['adc_id'][:LEN_KEY]]
        for child in children:
            child_kind = child['kind']
            child_id = child['adc_id']
            child_id =f'{source_id}-{child_id}'
            defineElement(child_id,child)
            if 'IDBIE'==child_kind:
                primaryKeys[link_id] = child_id
        if link_id in primaryKeys:
            return primaryKeys[link_id]
        return None

    html_head = [
        '<?xml version="1.0" encoding="UTF-8"?>\n',
        '<!-- (c) 2022 XBRL Japan  inc. -->\n',
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
        '            <link:linkbaseRef xlink:type="simple" xlink:role="http://www.xbrl.org/2003/role/labelLinkbaseRef" xlink:arcrole="http://www.w3.org/1999/xlink/properties/linkbase" xlink:href="core-lbl-ja.xml"/>\n',
        '            <link:linkbaseRef xlink:type="simple" xlink:role="http://www.xbrl.org/2003/role/labelLinkbaseRef" xlink:arcrole="http://www.w3.org/1999/xlink/properties/linkbase" xlink:href="core-lbl-en.xml"/>\n',
        '            <link:linkbaseRef xlink:type="simple" xlink:role="http://www.xbrl.org/2003/role/presentationLinkbaseRef" xlink:arcrole="http://www.w3.org/1999/xlink/properties/linkbase" xlink:href="core-pre.xml"/>\n',
        '            <link:linkbaseRef xlink:type="simple" xlink:role="http://www.xbrl.org/2003/role/definitionLinkbaseRef" xlink:arcrole="http://www.w3.org/1999/xlink/properties/linkbase" xlink:href="core-def.xml"/>\n',
        # '            <!-- formula -->\n',
        # '            <link:linkbaseRef xlink:type="simple" xlink:arcrole="http://www.w3.org/1999/xlink/properties/linkbase" xlink:href="core-for-Mandatory-Base.xml"/> \n',
        # '            <link:linkbaseRef xlink:type="simple" xlink:arcrole="http://www.w3.org/1999/xlink/properties/linkbase" xlink:href="core-for-Mandatory-GL.xml"/> \n',
        # '            <link:linkbaseRef xlink:type="simple" xlink:arcrole="http://www.w3.org/1999/xlink/properties/linkbase" xlink:href="core-for-Mandatory-O2C.xml"/> \n',
        # '            <link:linkbaseRef xlink:type="simple" xlink:arcrole="http://www.w3.org/1999/xlink/properties/linkbase" xlink:href="core-for-Mandatory-P2P.xml"/> \n',
        # '            <link:linkbaseRef xlink:type="simple" xlink:arcrole="http://www.w3.org/1999/xlink/properties/linkbase" xlink:href="core-for-Mandatory-Core.xml"/> \n',
        # '            <link:linkbaseRef xlink:type="simple" xlink:arcrole="http://www.w3.org/1999/xlink/properties/linkbase" xlink:href="core-for-Card-Base.xml"/> \n',
        # '            <link:linkbaseRef xlink:type="simple" xlink:arcrole="http://www.w3.org/1999/xlink/properties/linkbase" xlink:href="core-for-Card-GL.xml"/> \n',
        # '            <link:linkbaseRef xlink:type="simple" xlink:arcrole="http://www.w3.org/1999/xlink/properties/linkbase" xlink:href="core-for-Card-O2C.xml"/> \n',
        # '            <link:linkbaseRef xlink:type="simple" xlink:arcrole="http://www.w3.org/1999/xlink/properties/linkbase" xlink:href="core-for-Card-P2P.xml"/> \n',
        # '            <link:linkbaseRef xlink:type="simple" xlink:arcrole="http://www.w3.org/1999/xlink/properties/linkbase" xlink:href="core-for-Card-Core.xml"/> \n',
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
    for adc_id,role in roleMap.items():
        role_id = role["role_id"]
        URI = role['URI']
        link_id = role['link_id']
        den = role["den"]
        if LEN_KEY==len(adc_id):
            html.append(f'            <link:roleType id="{role_id}" roleURI="http://www.xbrl.jp/audit-data-collection/role{URI}">\n')
            html.append(f'                <link:definition>{den}</link:definition>\n')
            html.append(f'                <link:usedOn>link:definitionLink</link:usedOn>\n')
            html.append('            </link:roleType>\n')
        else:
            source_den = den[:den.index('-')]
            target_den = den[den.index('-')+1:]
            html.append(f'            <link:roleType id="{role_id}" roleURI="http://www.xbrl.jp/audit-data-collection/role{URI}">\n')
            html.append(f'                <link:definition>{source_den} to {target_den}</link:definition>\n')
            html.append(f'                <link:usedOn>link:definitionLink</link:usedOn>\n')
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
    for adc_id,role in roleMap.items():
        link_id = role['link_id']
        html_hypercube.append(f'    <element name="h_{link_id}" id="h_{link_id}" substitutionGroup="xbrldt:hypercubeItem" type="xbrli:stringItemType" nillable="true" abstract="true" xbrli:periodType="instant"/>\n')
    lines += html_hypercube

    html_dimension = [
        '    <!-- Dimension -->\n'
    ]
    # Dimension
    for adc_id,role in roleMap.items():
        link_id = role['link_id']
        html_dimension.append(f'    <element name="d_{link_id}" id="d_{link_id}" substitutionGroup="xbrldt:dimensionItem" type="xbrli:stringItemType" abstract="true" xbrli:periodType="instant" xbrldt:typedDomainRef="#_v"/>\n')
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
    for name,type in datatypeMap.items():
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
        defineElement(adc_id,record)
        if 'IDBIE'==kind:
            primaryKeys[adc_id[:LEN_KEY]] = adc_id
        if 'ASBIE'==kind and 'n'==record['occMax']:
            if adc_id in referenceDict:
                referenced_id = referenceDict[adc_id]['ABIE']
            elif adc_id in targetRefDict:
                referenced_id = targetRefDict[adc_id]
            else:
                associatedClass = record['associatedClass']
                associatedClass = titleCase(associatedClass)
                referenced_id = None
                for adc2_id,record2 in adcDict.items():
                    cls = titleCase(record2['class'])
                    if associatedClass==cls:#record2['class']:
                        referenced_id = f'{adc_id[:LEN_KEY]}-{adc2_id}'
                        defineElement(referenced_id,record2)
                        # break
            # if referenced_id:
            #     record2 = getRecord(referenced_id[-LEN_KEY:])
            #     if 'children' in record2:
            #         children = record2['children']
            #         for child_id in children:
            #             child = getRecord(child_id)
            #             referenced_id = f'{adc_id[:LEN_KEY]}-{child_id}'
            #             defineElement(referenced_id,child)
        
    for link_id,role in roleMap.items():
        if LEN_KEY==len(link_id):
            continue
        adc_id = link_id[-LEN_KEY:]
        record = getRecord(adc_id)
        defineElement(link_id,record)
        lookupPrimarykey(link_id)

    # for adc_id,target_id in targetRefDict.items():
    #     link_id = f'{source_id}-{target_id}'
    #     if not link_id in primaryKeys:
    #         primary_key = lookupPrimarykey(link_id)
            # primaryKeys[link_id] = primary_key
            # if DEBUG:
            #     print(f'NOT DEFINED primary key {primary_key} in {link_id}')

    # for adc_id,target_id in associationDict.items():
    #     link_id = f'{source_id}-{target_id}'
    #     if not link_id in primaryKeys:
    #         primary_key = lookupPrimarykey(link_id)
            # primaryKeys[link_id] = primary_key
            # if DEBUG:
            #     print(f'NOT DEFINED primary key {primary_key} in {link_id}')

    lines.append('</schema>')

    adc_xsd_file = file_path(f'{xbrl_base}/{core_xsd}')
    with open(adc_xsd_file, 'w', encoding='utf_8', newline='') as f:
        f.writelines(lines)
    if VERBOSE:
        print(f'-- {adc_xsd_file}')

    ###################################
    # labelLink en
    #
    def linkLabelTerm(adc_id,term,lang):
        global locsDefined
        global definedLabels
        global arcsDefined
        global definedDescs
        global definedDescArcs
        lines.append(f'        <!-- {adc_id} {term} -->\n')
        if not adc_id in locsDefined:
            locsDefined[adc_id] = adc_id
            line = f'        <link:loc xlink:type="locator" xlink:href="{core_xsd}#{adc_id}" xlink:label="{adc_id}" xlink:title="{adc_id}"/>\n'
        else:
            line = f'            <!-- link:loc defined -->\n'
        lines.append(line)
        # term
        if not adc_id in definedLabels:
            definedLabels[adc_id] = adc_id
            line = f'        <link:label xlink:type="resource" xlink:label="label_{adc_id}_{lang}" xlink:title="label_{adc_id}_{lang}" id="label_{adc_id}_{lang}" xml:lang="{lang}" xlink:role="http://www.xbrl.org/2003/role/label">{term}</link:label>\n'
        else:
            line = f'            <!-- link:label http://www.xbrl.org/2003/role/label defined -->\n'
        lines.append(line)
        if not adc_id in arcsDefined:
            arcsDefined[adc_id] = adc_id
            line = f'        <link:labelArc xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label" xlink:from="{adc_id}" xlink:to="label_{adc_id}_{lang}" xlink:title="label: {adc_id} to label_{adc_id}_{lang}"/>\n'
        else:
            line = f'            <!-- link:labelArc http://www.xbrl.org/2003/arcrole/concept-label defined -->\n'
        lines.append(line)

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>\n',
        '<!--  (c) 2022 XBRL Japan inc. -->\n',
        '<link:linkbase\n',
        '    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n',
        '    xmlns:link="http://www.xbrl.org/2003/linkbase"\n',
        '    xmlns:xlink="http://www.w3.org/1999/xlink"\n',
        '    xsi:schemaLocation="http://www.xbrl.org/2003/linkbase http://www.xbrl.org/2003/xbrl-linkbase-2003-12-31.xsd">\n',
        f'    <!--link:roleRef roleURI="http://www.xbrl.jp/audit-data-collection/role/description" xlink:type="simple" xlink:href="{core_xsd}#description"/>\n',
        f'    <link:arcroleRef arcroleURI="http://www.xbrl.jp/audit-data-collection/arcrole/concept-description" xlink:type="simple" xlink:href="{core_xsd}#concept-description"/-->\n',
        '    <link:labelLink xlink:type="extended" xlink:role="http://www.xbrl.org/2003/role/link">\n'
    ]
    locsDefined = {}
    arcsDefined = {}
    definedLabels = {}
    for record in adcDict.values():
        adc_id = record['adc_id']
        kind = record['kind']
        if 'ABIE'==kind:
            term = titleCase(record['class'])
        elif 'ASBIE'==kind:
            term = record['associatedClass']
        elif 'BBIE'==kind:
            term = titleCase(record['propertyTerm'])
        if len(term) > 0:
            linkLabelTerm(adc_id,term,'en')

    for adc_id,referenced_id in targetRefDict.items():
        record = getRecord(referenced_id)
        name = record['name']
        if len(name) > 0:
            linkLabelTerm(adc_id,name,'en')
            adc_id = f'{adc_id[:LEN_KEY]}-{referenced_id}'
            linkLabelTerm(adc_id,name,'en')

    lines.append('    </link:labelLink>\n')
    lines.append('</link:linkbase>\n')

    adc_label_file = file_path(f'{xbrl_base}/{core_label}-en.xml')
    with open(adc_label_file, 'w', encoding='utf_8', newline='') as f:
        f.writelines(lines)
    if VERBOSE:
        print(f'-- {adc_label_file}')

    ###################################
    # labelLink ja
    #
    def linkLabel(adc_id,name,desc,lang):
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
            line = f'        <link:label xlink:type="resource" xlink:label="label_{adc_id}_{lang}" xlink:title="label_{adc_id}_{lang}" id="label_{adc_id}_{lang}" xml:lang="{lang}" xlink:role="http://www.xbrl.org/2003/role/label">{name}</link:label>\n'
        else:
            line = f'            <!-- link:label http://www.xbrl.org/2003/role/label defined -->\n'
        lines.append(line)
        if not adc_id in arcsDefined:
            arcsDefined[adc_id] = adc_id
            line = f'        <link:labelArc xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label" xlink:from="{adc_id}" xlink:to="label_{adc_id}_{lang}" xlink:title="label: {adc_id} to label_{adc_id}_{lang}"/>\n'
        else:
            line = f'            <!-- link:labelArc http://www.xbrl.org/2003/arcrole/concept-label defined -->\n'
        lines.append(line)
        # desc
        if name != desc:
            if not adc_id in definedDescs:
                definedDescs[adc_id] = adc_id
                line = f'        <link:label xlink:type="resource" xlink:label="description_{adc_id}_{lang}" xlink:title="description_{adc_id}_{lang}" id="description_{adc_id}_{lang}" xml:lang="{lang}" xlink:role="http://www.xbrl.jp/audit-data-collection/role/description">{desc}</link:label>\n'
            else:
                line = f'            <!-- link:label http://www.xbrl.jp/audit-data-collection/role/description defined -->\n'
            lines.append(line)
            if not adc_id in definedDescArcs:
                definedDescArcs[adc_id] = adc_id
                line = f'        <link:labelArc xlink:type="arc" xlink:arcrole="http://www.xbrl.jp/audit-data-collection/arcrole/concept-description" xlink:from="{adc_id}" xlink:to="description_{adc_id}_{lang}" xlink:title="label: {adc_id} to label_{adc_id}_{lang}"/>\n'
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
        kind = record['kind']
        name = record['name']
        desc = record['desc']
        if len(name) > 0 or len(desc) > 0:
            linkLabel(adc_id,name,desc,'ja')
            if 'ASBIE'==kind:# and 'n'==record['occMax']:
                if adc_id in referenceDict:
                    referenced_id = referenceDict[adc_id]['ABIE']
                elif adc_id in targetRefDict:
                    referenced_id = targetRefDict[adc_id]
                else:
                    associatedClass = record['associatedClass']
                    referenced_id = None
                    for adc2_id,record2 in adcDict.items():
                        if associatedClass==record2['class']:
                            referenced_id = f'{adc_id[:LEN_KEY]}-{adc2_id}'
                            linkLabel(referenced_id,name,desc,'ja')
                            break

    for adc_id,referenced_id in targetRefDict.items():
        record = getRecord(referenced_id)
        name = record['name']
        desc = record['desc']
        if len(name) > 0 or len(desc) > 0:
            linkLabel(adc_id,name,desc,'ja')
            adc_id = f'{adc_id[:LEN_KEY]}-{referenced_id}'
            linkLabel(adc_id,name,desc,'ja')

    lines.append('    </link:labelLink>\n')
    lines.append('</link:linkbase>\n')

    adc_label_file = file_path(f'{xbrl_base}/{core_label}-ja.xml')
    with open(adc_label_file, 'w', encoding='utf_8', newline='') as f:
        f.writelines(lines)
    if VERBOSE:
        print(f'-- {adc_label_file}')

    ###################################
    #   presentationLink
    #
    locsDefined = {}
    arcsDefined = {}
    def linkPresentation(adc_id,children,n):
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
            lines.append(f'        <link:loc xlink:type="locator" xlink:href="{core_xsd}#{adc_id}" xlink:label="{adc_id}" xlink:title="presentation: {adc_id} {name}"/>\n')
        for child_id in children:
            # childDefined[child_id] = name
            child = getRecord(child_id)
            child_kind = child['kind']
            child_name = child['name']
            level = child['level']
            if level != n:
                continue
            if 'ASBIE'==child_kind:# and 'n'==child['occMax']:# and child_id in targetRefDict:
                target_id = child_id
                if not target_id in locsDefined:
                    locsDefined[target_id] = child_name
                    lines.append(f'        <link:loc xlink:type="locator" xlink:href="{core_xsd}#{target_id}" xlink:label="{target_id}" xlink:title="presentation parent: {target_id} {child_name}"/>\n')
                arc_id = F'{adc_id} {target_id}'
                if not arc_id in arcsDefined and adc_id!=target_id:
                    arcsDefined[arc_id] = f'{name} to {child_name}'
                    count += 1
                    lines.append(f'        <link:presentationArc xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child" xlink:from="{adc_id}" xlink:to="{target_id}" order="{count}" xlink:title="presentation: {adc_id} {name} to {target_id} {child_name}"/>\n')
                    if 'children' in child and len(child['children']) > 0:
                        grand_children = child['children']
                        # grand_children = [c for c in grand_children if c not in childDefined]
                        linkPresentation(target_id,grand_children,n+1)
            else:
                if not child_id in locsDefined:
                    locsDefined[child_id] = child_name
                    lines.append(f'        <link:loc xlink:type="locator" xlink:href="{core_xsd}#{child_id}" xlink:label="{child_id}" xlink:title="presentation parent: {child_id} {child_name}"/>\n')
                arc_id = F'{adc_id} {child_id}'
                if not arc_id in arcsDefined and adc_id!=child_id:
                    arcsDefined[arc_id] = f'{name} to {child_name}'
                    count += 1
                    lines.append(f'        <link:presentationArc xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child" xlink:from="{adc_id}" xlink:to="{child_id}" order="{count}" xlink:title="presentation: {adc_id} {name} to {child_id} {child_name}"/>\n')
                    if 'children' in child and len(child['children']) > 0:
                        grand_children = child['children']
                        # grand_children = [c for c in grand_children if c not in childDefined]
                        linkPresentation(child_id,grand_children,n+1)
        children = None
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>\n',
        '<!--  (c) 2022 XBRL Japan inc. -->\n',
        '<link:linkbase\n',
        '    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n',
        '    xsi:schemaLocation="http://www.xbrl.org/2003/linkbase http://www.xbrl.org/2003/xbrl-linkbase-2003-12-31.xsd"\n',
        '    xmlns:link="http://www.xbrl.org/2003/linkbase"\n',
        '    xmlns:xlink="http://www.w3.org/1999/xlink">\n',
        f'    <link:roleRef roleURI="http://www.xbrl.jp/audit-data-collection/role" xlink:type="simple" xlink:href="{core_xsd}#audit-data-collection-role"/>\n',
        '    <link:presentationLink xlink:type="extended" xlink:role="http://www.xbrl.jp/audit-data-collection/role">\n',
    ]
    locsDefined = {}
    arcsDefined = {}
    # for record in [x for x in records if 'ABIE'==x['kind']]:
    record = [x for x in records if 'ABIE'==x['kind']][0]
    adc_id = record['adc_id']
    kind = record['kind']
    count = 0
    children = record['children']
    linkPresentation(adc_id,children,1)
       
    lines.append('    </link:presentationLink>\n')
    lines.append('</link:linkbase>\n')

    adc_presentation_file = file_path(f'{xbrl_base}/{core_presentation}.xml')
    with open(adc_presentation_file, 'w', encoding='utf_8', newline='') as f:
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
        lines.append(f'    <link:roleRef roleURI="http://www.xbrl.jp/audit-data-collection/role{URI}" xlink:type="simple" xlink:href="{core_xsd}#{role_id}"/>\n')
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

    for adc_id,role in roleMap.items():
        defineHypercube(adc_id, role, 2)

    lines.append('</link:linkbase>\n')

    adc_definition_file = file_path(f'{xbrl_base}/{core_definition}.xml')
    with open(adc_definition_file, 'w', encoding='utf_8', newline='') as f:
        f.writelines(lines)
    if VERBOSE:
        print(f'-- {adc_definition_file}')

    print('** END **')