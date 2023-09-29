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

xbrl_source        = 'data/base/'
xbrl_source        = xbrl_source.replace('/', SEP)
core_head          = 'corehead.txt'
primarykey_file    = 'primarykey.csv'

xbrl_base          = 'data/xbrl/'
xbrl_base          = xbrl_base.replace('/', SEP)
core_xsd           = 'core.xsd'
core_label         = 'core-lbl'
core_presentation  = 'core-pre'
core_definition    = 'core-def'
core_reference     = 'core-ref'
# core_for_Card      = 'core-for-Card'
# core_for_Mandatory = 'core-for-Mandatory'

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

targetTables    = ['GL02','GL03']

duplicateNames  = set()
names           = set()
adcDict         = {}
targetRefDict   = {}
associationDict = {}
referenceDict   = {}
sourceRefDict   = {}
locsDefined     = {}
arcsDefined     = {}
locsDefined     = {}
alias           = {}
targets         = {}
roleMap         = None
primaryKeys     = set()

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

def sme_xpath_to_title(camel_case_str):
    camel_case_str = camel_case_str.replace('SME','')
    camel_case_str = camel_case_str.replace('CIILB','')
    camel_case_str = camel_case_str.replace('CIIH','')
    camel_case_str = camel_case_str.replace('CIIL','')
    camel_case_str = camel_case_str.replace('CI','')
    camel_case_str = camel_case_str.replace('Subordinate','')
    camel_case_str = camel_case_str.replace('Specified','')
    camel_case_str = camel_case_str.replace('Trade','')
    camel_case_str = camel_case_str.replace('SupplyChain','')
    camel_case_str = camel_case_str.replace('@','')
    words          = re.sub('([a-z0-9])([A-Z])', r'\1 \2', camel_case_str)
    words          = words.split(' ')
    # title_case_str = words.title()
    title_case_str = ' '.join(
        [word if word=='ID' else word[0].upper() + word[1:].lower() for word in words]
    )
    title_case_str = title_case_str.replace('Referenced Referenced','Referenced')
    title_case_str = title_case_str.replace('Reference Referenced','Referenced')
    title_case_str = title_case_str.replace('Identification ID','ID')
    return title_case_str

# def getName(adc_id):
#     record = getRecord(adc_id)
#     if record:
#         return record['name']
#     return ''

# def getDEN(adc_id):
#     record = getRecord(adc_id)
#     if record:
#         den = record['DEN']
#         return den.replace('_','')
#     return ''

def getRecord(adc_id):
    if adc_id in adcDict:
        record = adcDict[adc_id]
    else:
        record = None
    return record

def getParent(adc_id):
    if adc_id in adcDict:
        parent = adcDict[adc_id]
    else:
        parent = None
    return parent

def getChildren(adc_id):
    record = getRecord(adc_id)
    if record:
        return record['children']
    return []

def checkAssociation(child_id,link_id,lines,source_id=None):
    global count
    child      = getRecord(child_id)
    child_kind = child['kind']
    if 'n'==child['card'] and child_id in targetRefDict:
        # targetRole
        role_record = roleRecord(child)
        role_id     = role_record['role_id']
        URI         = role_record['URI']
        if DEBUG: print(f'domain-member: {link_id} to {child_id} order={count} in {role_id} targetRole="http://www.xbrl.jp/japan-core/role{URI}')
        lines.append(f'\t\t<!-- {child_id} targetRole {role_id} -->\n')
        if not child_id in locsDefined[link_id]:
            locsDefined[link_id].add(child_id)
            lines.append(f'\t\t<link:loc xlink:type="locator" xlink:href="{core_xsd}#{child_id}" xlink:label="{child_id}" xlink:title="{child_id}"/>\n')
        count += 1
        arc_id = f'{link_id} {child_id}'
        if not arc_id in arcsDefined[link_id]:
            arcsDefined[link_id].add(arc_id)
            lines.append(f'\t\t<link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xbrldt:targetRole="http://www.xbrl.jp/japan-core/role{URI}" xlink:from="{link_id}" xlink:to="{child_id}" xlink:title="domain-member: {link_id} to {child_id} in {role_id}" order="{count}"/>\n')
    else:
        if 'Aggregation'==child_kind and '1'==child['card']:
            if 'children' in child and len(child['children']) > 0:
                if DEBUG: print(f'domain-member: {link_id} to {child_id} order={count}')
                if not child_id in locsDefined[link_id]:
                    locsDefined[link_id].add(child_id)
                    lines.append(f'\t\t<link:loc xlink:type="locator" xlink:href="{core_xsd}#{child_id}" xlink:label="{child_id}" xlink:title="{child_id}"/>\n')
                count += 1
                arc_id = f'{link_id} {child_id}'
                if not arc_id in arcsDefined[link_id]:
                    arcsDefined[link_id].add(arc_id)
                    lines.append(f'\t\t<link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="{link_id}" xlink:to="{child_id}" xlink:title="domain-member: {link_id} to {child_id}" order="{count}"/>\n')
                grand_children =  child['children']
                for grand_child_id in grand_children:
                    lines = checkAssociation(grand_child_id,link_id,lines,child_id)
        else:
            if not source_id:
                source_id = link_id
            if DEBUG: print(f'domain-member: {source_id} to {child_id} order={count}')
            if not child_id in locsDefined[link_id]:
                locsDefined[link_id].add(child_id)
                lines.append(f'\t\t<link:loc xlink:type="locator" xlink:href="{core_xsd}#{child_id}" xlink:label="{child_id}" xlink:title="{child_id}"/>\n')
            count += 1
            arc_id = f'{source_id} {child_id}'
            if not arc_id in arcsDefined[link_id]:
                arcsDefined[link_id].add(arc_id)
                lines.append(f'\t\t<link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="{source_id}" xlink:to="{child_id}" xlink:title="domain-member: {source_id} to {child_id}" order="{count}"/>\n')
    return lines

def defineHypercube(adc_id):
    global lines
    global locsDefined
    global arcsDefined
    global targetRefDict
    global referenceDict
    root_id = None
    root_id = adc_id
    root    = getRecord(root_id)
    if not root:
        print(f'** {root_id} is not defined.')
        return None
    role                 = roleRecord(root)
    link_id              = role['link_id']
    locsDefined[link_id] = set()
    arcsDefined[link_id] = set()
    URI                  = role['URI']
    role_id              = role['role_id']
    hypercube_id         = f"h_{link_id}"
    dimension_id_list    = set()
    source_id            = None
    origin_id            = None
    if 'n'!=root['card'] or root_id in ROOT_IDs:
        root_dimension = f"d_{root_id}"
        dimension_id_list.add(root_dimension)
    else:
        root_dimension_id = f'd_{root_id}'
        dimension_id_list.add(root_dimension_id)
        semPath           = root['semPath']
        source_id         = semPath.strip('/').split('/')[-2] #link_id[:LEN_KEY]
        source            = getRecord(source_id)
        if 'n'==source['card']:
            source_dimension  = f'd_{source_id}'
            dimension_id_list.add(source_dimension)
    lines.append(f'\t<link:definitionLink xlink:type="extended" xlink:role="http://www.xbrl.jp/japan-core/role{URI}">\n')
    # all (has-hypercube)
    lines.append(f'\t\t<!-- {link_id} all (has-hypercube) {hypercube_id} {role_id} -->\n')
    lines.append(f'\t\t<link:loc xlink:type="locator" xlink:href="{core_xsd}#{link_id}" xlink:label="{link_id}" xlink:title="{link_id}"/>\n')
    lines.append(f'\t\t<link:loc xlink:type="locator" xlink:href="{core_xsd}#{hypercube_id}" xlink:label="{hypercube_id}" xlink:title="{hypercube_id}"/>\n')
    lines.append(f'\t\t<link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/all" xlink:from="{link_id}" xlink:to="{hypercube_id}" xlink:title="all (has-hypercube): {link_id} to {hypercube_id}" order="1" xbrldt:closed="true" xbrldt:contextElement="scenario"/>\n')
    if DEBUG:
        print(f'all(has-hypercube) {link_id} to {hypercube_id} ')
    # hypercube-dimension
    lines.append('\t\t<!-- hypercube-dimension -->\n')
    count = 0
    for dimension_id in dimension_id_list:
        lines.append(f'\t\t<link:loc xlink:type="locator" xlink:href="{core_xsd}#{dimension_id}" xlink:label="{dimension_id}" xlink:title="{dimension_id}"/>\n')
        count += 1
        lines.append(f'\t\t<link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/hypercube-dimension" xlink:from="{hypercube_id}" xlink:to="{dimension_id}" xlink:title="hypercube-dimension: {hypercube_id} to {dimension_id}" order="{count}"/>\n')
        if DEBUG:
            print(f'hypercube-dimension {hypercube_id} to {dimension_id} ')
    # domain-member
    lines.append('\t\t<!-- domain-member -->\n')
    if 'children' in root and len(root['children']) > 0:
        children = root['children']
        for child_id in children:
            lines = checkAssociation(child_id,link_id,lines)
    lines.append('\t</link:definitionLink>\n')

def lookupModule(class_id):
    module = None
    prefix = class_id[:2]
    if 'NC'==prefix:   module = 'Invoice'
    elif 'BS'==prefix: module = 'Base'
    elif 'GL'==prefix: module = 'GL'
    elif 'CM'==prefix: module = 'Common'
    return module

def roleRecord(record):
    adc_id      = record['adc_id']
    link_id     = adc_id
    role_id     = f'link_{link_id}'
    URI         = f'/{role_id}'
    role_record = {'adc_id':adc_id, 'link_id':link_id, 'URI':URI, 'role_id':role_id}
    return role_record

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
        type = record['datatype'] if 'datatype' in record and record['datatype'] else ''
        if DEBUG: print(f'define {adc_id} [{kind}]')
        if 'Aggregation'==kind:# or adc_id in targetRefDict or adc_id in referenceDict:
            line = f'\t<element name="{adc_id}" id="{adc_id}" abstract="true" type="xbrli:stringItemType" nillable="true" substitutionGroup="xbrli:item" xbrli:periodType="instant"/>\n'
        else:
            type = get_element_datatype(adc_id,type,kind)
            line = f'\t<element name="{adc_id}" id="{adc_id}" type="{type}" nillable="false" substitutionGroup="xbrli:item" xbrli:periodType="instant"/>\n'
        lines.append(line)

# def lookupPrimarykey(link_id):
#     source_id = link_id[:LEN_KEY]
#     adc_id = link_id[-LEN_KEY:]
#     children = [record for record in records if adc_id==record['adc_id'][:LEN_KEY]]
#     for child in children:
#         child_kind = child['kind']
#         child_id   = child['adc_id']
#         # child_id =f'{source_id}-{child_id}'
#         defineElement(child_id,child)
#         if 'IDBIE'==child_kind:
#             primaryKeys[link_id] = child_id
#     if link_id in primaryKeys:
#         return primaryKeys[link_id]
#     return None

def linkLabelTerm(adc_id,term,lang):
    global locsDefined
    global definedLabels
    global arcsDefined
    global definedDescs
    global definedDescArcs
    lines.append(f'\t\t<!-- {adc_id} {term} -->\n')
    if not adc_id in locsDefined:
        locsDefined[adc_id] = adc_id
        line = f'\t\t<link:loc xlink:type="locator" xlink:href="{core_xsd}#{adc_id}" xlink:label="{adc_id}" xlink:title="{adc_id}"/>\n'
    else:
        line = f'\t\t\t<!-- link:loc defined -->\n'
    lines.append(line)
    # term
    if not adc_id in definedLabels:
        definedLabels[adc_id] = adc_id
        line = f'\t\t<link:label xlink:type="resource" xlink:label="label_{adc_id}" xlink:title="label_{adc_id}" id="label_{adc_id}" xml:lang="{lang}" xlink:role="http://www.xbrl.org/2003/role/label">{term}</link:label>\n'
    else:
        line = f'\t\t\t<!-- link:label http://www.xbrl.org/2003/role/label defined -->\n'
    lines.append(line)
    if not adc_id in arcsDefined:
        arcsDefined[adc_id] = adc_id
        line = f'\t\t<link:labelArc xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label" xlink:from="{adc_id}" xlink:to="label_{adc_id}" xlink:title="label: {adc_id} to label_{adc_id}"/>\n'
    else:
        line = f'\t\t\t<!-- link:labelArc http://www.xbrl.org/2003/arcrole/concept-label defined -->\n'
    lines.append(line)

def linkLabel(adc_id,name,desc,lang):
    global locsDefined
    global definedLabels
    global arcsDefined
    global definedDescs
    global definedDescArcs
    lines.append(f'\t\t<!-- {adc_id} {name} -->\n')
    if not adc_id in locsDefined:
        locsDefined[adc_id] = adc_id
        line = f'\t\t<link:loc xlink:type="locator" xlink:href="{core_xsd}#{adc_id}" xlink:label="{adc_id}" xlink:title="{adc_id}"/>\n'
    else:
        line = f'\t\t\t<!-- link:loc defined -->\n'
    lines.append(line)
    # name
    if not adc_id in definedLabels:
        definedLabels[adc_id] = adc_id
        line = f'\t\t<link:label xlink:type="resource" xlink:label="label_{adc_id}" xlink:title="label_{adc_id}" id="label_{adc_id}" xml:lang="{lang}" xlink:role="http://www.xbrl.org/2003/role/label">{name}</link:label>\n'
    else:
        line = f'\t\t\t<!-- link:label http://www.xbrl.org/2003/role/label defined -->\n'
    lines.append(line)
    if not adc_id in arcsDefined:
        arcsDefined[adc_id] = adc_id
        line = f'\t\t<link:labelArc xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label" xlink:from="{adc_id}" xlink:to="label_{adc_id}" xlink:title="label: {adc_id} to label_{adc_id}"/>\n'
    else:
        line = f'\t\t\t<!-- link:labelArc http://www.xbrl.org/2003/arcrole/concept-label defined -->\n'
    lines.append(line)
    # desc
    if desc and name != desc:
        if not adc_id in definedDescs:
            definedDescs[adc_id] = adc_id
            line = f'\t\t<link:label xlink:type="resource" xlink:label="description_{adc_id}" xlink:title="description_{adc_id}" id="description_{adc_id}" xml:lang="{lang}" xlink:role="http://www.xbrl.jp/japan-core/role/description">{desc}</link:label>\n'
        else:
            line = f'\t\t\t<!-- link:label http://www.xbrl.jp/japan-core/role/description defined -->\n'
        lines.append(line)
        if not adc_id in definedDescArcs:
            definedDescArcs[adc_id] = adc_id
            line = f'\t\t<link:labelArc xlink:type="arc" xlink:arcrole="http://www.xbrl.jp/japan-core/arcrole/concept-description" xlink:from="{adc_id}" xlink:to="description_{adc_id}" xlink:title="label: {adc_id} to label_{adc_id}"/>\n'
        else:
            line = f'\t\t\t<!-- link:labelArc http://www.xbrl.jp/japan-core/arcrole/concept-description defined -->\n'
        lines.append(line)

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
    name = record['property']
    if not adc_id in locsDefined:
        locsDefined[adc_id] = name
        lines.append(f'\t\t<!-- {kind} {adc_id} {name} -->\n')
        lines.append(f'\t\t<link:loc xlink:type="locator" xlink:href="{core_xsd}#{adc_id}" xlink:label="{adc_id}" xlink:title="presentation: {adc_id} {name}"/>\n')
    for child_id in children:
        child = getRecord(child_id)
        child_kind = child['kind']
        child_name = child['property']
        if 'Aggregation'==child_kind:
            target_id = child_id
            if not target_id in locsDefined:
                locsDefined[target_id] = child_name
                lines.append(f'\t\t<link:loc xlink:type="locator" xlink:href="{core_xsd}#{target_id}" xlink:label="{target_id}" xlink:title="presentation parent: {target_id} {child_name}"/>\n')
            arc_id = F'{adc_id} {target_id}'
            if not arc_id in arcsDefined and adc_id!=target_id:
                arcsDefined[arc_id] = f'{name} to {child_name}'
                count += 1
                lines.append(f'\t\t<link:presentationArc xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child" xlink:from="{adc_id}" xlink:to="{target_id}" order="{count}" xlink:title="presentation: {adc_id} {name} to {target_id} {child_name}"/>\n')
                if 'children' in child and len(child['children']) > 0:
                    grand_children = child['children']
                    linkPresentation(target_id,grand_children,n+1)
        else:
            if not child_id in locsDefined:
                locsDefined[child_id] = child_name
                lines.append(f'\t\t<link:loc xlink:type="locator" xlink:href="{core_xsd}#{child_id}" xlink:label="{child_id}" xlink:title="presentation parent: {child_id} {child_name}"/>\n')
            arc_id = F'{adc_id} {child_id}'
            if not arc_id in arcsDefined and adc_id!=child_id:
                arcsDefined[arc_id] = f'{name} to {child_name}'
                count += 1
                lines.append(f'\t\t<link:presentationArc xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child" xlink:from="{adc_id}" xlink:to="{child_id}" order="{count}" xlink:title="presentation: {adc_id} {name} to {child_id} {child_name}"/>\n')
                if 'children' in child and len(child['children']) > 0:
                    grand_children = child['children']
                    linkPresentation(child_id,grand_children,n+1)
    children = None

def escape_text(str):
    if not str:
        return ''
    escaped = str.replace('<','&lt;')
    escaped = escaped.replace('>','&gt;')
    return escaped

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
    core_file = in_file
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
    # 1. japan_core.csv -> schema
    ROOT_IDs  = ['JC00']
    records   = []
    core_file = file_path(core_file)
    adcDict   = {}
    classDict = {}
    associonDict = {}

    # header = ['semSort','group','adc_id','class_id','field_id','level','occurrence','term','kind','class','propertyTerm','representation','associatedClass','desc','UN_CCL_ID','smeKind','smeSeq','smeID','smeTerm','smeDesc','smeDefault','smeOccur','smeLevel','smeXPath','pintSort','pintID','pintOccur','pintLevel','pintTerm','pintTermJA','pintDesc','pintDescJA','pintDefault','pintXPath']
    header = ['semSort','select','Semantic_Path','adc_id','ObjectClass','card','Property','Representation','AssociatedClass','ReferencedClass','SMEconsolidatedSeq','Part_consolidated','UN_CCL_Idconsolidated','Kind_consolidated','DENconsolidated1','DENconsolidated2','DENconsolidated3','DENconsolidated4','DENconsolidated5','DENconsolidated6','DENconsolidated7','DENconsolidated8','DENconsolidated9','DENconsolidated10','Term_consolidated','Definition_consolidated','Card_consolidated','SMEsingleSqe','Part_single','UN_CCL_Idsingle','Kind_single','DENsingle1','DENsingle2','DENsingle3','DENsingle4','DENsingle5','DENsingle6','DENsingle7','DENsingle8','DENsingle9','DENsingle10','Term_single','Definition_single','Card_single','Fixed_Value_SME','SME_XPath','SME_Xpath0','JP-PINT_SynSort','JP-PINT_ID','Level','Term_ja','Business_Term','Aligned_Cardinality','JP-PINT_datatype','JP-PINT_Fixed_Value','JP-PINT_Xpath']
    # header  = ['semSort','select','semPath','adc_id','objectClass','card','property','representation','associatedClass','referencedClass']
    with open(core_file, encoding='utf-8-sig', newline='') as f:
        reader = csv.reader(f)
        next(reader)
        for cols in reader:
            record = {}
            for i in range(len(header)):
                col = cols[i]
                record[header[i]] = col.strip()
            adc_id          = record['adc_id']
            if not adc_id:
                continue
            semSort            = record['semSort']
            semPath            = record['Semantic_Path']
            objectClass        = record['ObjectClass']
            card               = record['card']
            property           = record['Property']
            representation     = record['Representation']
            associatedClass    = record['AssociatedClass']
            referencedClass    = record['ReferencedClass']

            SMESeq             = record['SMEconsolidatedSeq']
            UN_CCL_Id          = record['UN_CCL_Idconsolidated']
            kindSme            = record['Kind_consolidated']
            termSme_ja         = record['Term_consolidated']
            definitionSme_ja   = record['Definition_consolidated']
            cardSme            = record['Card_consolidated']
            fixedValueSme      = record['Fixed_Value_SME']
            xPathSme           = record['SME_XPath']

            jp_pintSynSort     = record['JP-PINT_SynSort']
            jp_pintID          = record['JP-PINT_ID']
            jp_pintLevel       = record['Level']
            jp_pintTerm_ja     = record['Term_ja']
            jp_pintTerm        = record['Business_Term']
            jp_pintCardinality = record['Aligned_Cardinality']
            jp_pintdatatype    = record['JP-PINT_datatype']
            jp_pintFixed_Value = record['JP-PINT_Fixed_Value']
            jp_pintXpath       = record['JP-PINT_Xpath']

            data = {}
            data['semSort']         = semSort
            data['semPath']         = semPath
            data['adc_id']          = adc_id
            data['objectClass']     = objectClass
            data['card']            = card
            data['property']        = property
            data['associatedClass'] = associatedClass
            if representation in datatypeMap:
                data['datatype'] = f"adc:{datatypeMap[representation]['adc']}"
            kind = 'Aggregation' if card in ['1','n'] else 'Attribute'
            data['kind'] = kind
            parent       = None
            class_id     = None
            if 'Aggregation'==kind:
                data['children']   = []
                if '/' in semPath[1:]:
                    parent = semPath[:semPath.rindex('/')]
                    parent = parent[1+parent.rindex('/'):]
                    data['parent'] = parent
                    adcDict[parent]['children'].append(adc_id)
                    if not associatedClass:
                        data['associatedClass'] = adc_id
                    associonDict[adc_id] = data
            else:
                parent = adc_id[:-(1+LEN_NUM)]
                data['parent'] = parent
                adcDict[parent]['children'].append(adc_id)
            level            = len(semPath.strip('/').split('/'))
            data['level']    = level
            data['class_id'] = class_id
            #SME Common EDI
            xPathSme = xPathSme.replace(' ','')
            xPs      = xPathSme.strip('/').split('/')
            termSme1 = xPs[-1]
            termSme1 = sme_xpath_to_title(termSme1)
            if len(xPs) > 1:
                termSme0 = xPs[-2]
                termSme0 = sme_xpath_to_title(termSme0)
                termSme  = f'{termSme0} {termSme1}'
            else:
                termSme = termSme1
            print(termSme)
            data['seqSme']         = SMESeq
            data['idSme']          = UN_CCL_Id
            data['kindSme']        = kindSme
            data['termSme']        = termSme
            data['termSme_ja']     = termSme_ja
            data['defSme_ja']      = definitionSme_ja
            data['cardSme']        = cardSme
            data['fixedValueSme']  = fixedValueSme
            data['xPathSme']       = xPathSme
            # JP PINT
            data['seqPint']        = jp_pintSynSort
            data['idPint']         = jp_pintID
            data['levelPint']      = jp_pintLevel
            data['termPint_ja']    = jp_pintTerm_ja
            data['termPint']       = jp_pintTerm
            data['cardPint']       = jp_pintCardinality
            data['fixedValuePint'] = jp_pintFixed_Value
            data['xPathPint']      = jp_pintXpath

            adcDict[adc_id]  = data
            records.append(data)

    print(records)

    targetRefDict = {}   # child-parent
    for adc_id, record in adcDict.items():
        if 'Aggregation'==record['kind'] and 'n'==record['card'] and 'children' in record:
            children = record['children']
            for child_id in children:
                child = getRecord(child_id)
                if 'Aggregation'==child['kind']:
                    targetRefDict[child_id] = adc_id

    roleMap = {}
    for adc_id,record in adcDict.items():
        if 'Aggregation'==record['kind'] and 'n'==record['card']:
            roleMap[adc_id] = roleRecord(record)

    ###################################
    # core.xsd
    #
    html_head = [
        '<?xml version="1.0" encoding="UTF-8"?>\n',
        '<!-- (c) 2022 XBRL Japan  inc. -->\n',
        '<schema \n',
        '\ttargetNamespace="http://www.xbrl.jp/japan-core" \n',
        '\telementFormDefault="qualified" \n',
        '\tattributeFormDefault="unqualified" \n',
        '\txmlns="http://www.w3.org/2001/XMLSchema" \n',
        '\txmlns:adc="http://www.xbrl.jp/japan-core" \n',
        '\txmlns:xlink="http://www.w3.org/1999/xlink" \n',
        '\txmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" \n',
        '\txmlns:xl="http://www.xbrl.org/2003/XLink" \n',
        '\txmlns:xbrli="http://www.xbrl.org/2003/instance" \n',
        '\txmlns:link="http://www.xbrl.org/2003/linkbase" \n',
        '\txmlns:nonnum="http://www.xbrl.org/dtr/type/non-numeric" \n',
        '\txmlns:num="http://www.xbrl.org/dtr/type/numeric" \n',
        '\txmlns:xbrldt="http://xbrl.org/2005/xbrldt" \n',
        '\txmlns:label="http://xbrl.org/2008/label" \n',
        '\txmlns:reference="http://xbrl.org/2008/reference">\n',
        '\t<import namespace="http://www.xbrl.org/2003/instance" schemaLocation="http://www.xbrl.org/2003/xbrl-instance-2003-12-31.xsd"/>\n',
        '\t<import namespace="http://www.xbrl.org/2003/linkbase" schemaLocation="http://www.xbrl.org/2003/xbrl-linkbase-2003-12-31.xsd"/>\n',
        '\t<import namespace="http://xbrl.org/2005/xbrldt" schemaLocation="http://www.xbrl.org/2005/xbrldt-2005.xsd"/>\n',
        '\t<import namespace="http://www.xbrl.org/dtr/type/numeric" schemaLocation="http://www.xbrl.org/dtr/type/numeric-2009-12-16.xsd"/>\n',
        '\t<import namespace="http://www.xbrl.org/dtr/type/non-numeric" schemaLocation="http://www.xbrl.org/dtr/type/nonNumeric-2009-12-16.xsd"/>\n',
        '\t<import namespace="http://xbrl.org/2008/label" schemaLocation="http://www.xbrl.org/2008/generic-label.xsd"/>\n',
        '\t<import namespace="http://xbrl.org/2008/reference" schemaLocation="http://www.xbrl.org/2008/generic-reference.xsd"/> \n',
    ]
    lines = html_head

    html_annotation_head = [
        '\t<annotation>\n',
        '\t\t<appinfo>\n',
        '\t\t\t<link:linkbaseRef xlink:type="simple" xlink:role="http://www.xbrl.org/2003/role/labelLinkbaseRef" xlink:arcrole="http://www.w3.org/1999/xlink/properties/linkbase" xlink:href="core-lbl-ja.xml"/>\n',
        '\t\t\t<link:linkbaseRef xlink:type="simple" xlink:role="http://www.xbrl.org/2003/role/labelLinkbaseRef" xlink:arcrole="http://www.w3.org/1999/xlink/properties/linkbase" xlink:href="core-lbl-en.xml"/>\n',
        '\t\t\t<link:linkbaseRef xlink:type="simple" xlink:role="http://www.xbrl.org/2003/role/presentationLinkbaseRef" xlink:arcrole="http://www.w3.org/1999/xlink/properties/linkbase" xlink:href="core-pre.xml"/>\n',
        '\t\t\t<link:linkbaseRef xlink:type="simple" xlink:role="http://www.xbrl.org/2003/role/definitionLinkbaseRef" xlink:arcrole="http://www.w3.org/1999/xlink/properties/linkbase" xlink:href="core-def.xml"/>\n',
        '\t\t\t<!-- reference -->\n',
        '\t\t\t<link:linkbaseRef xlink:type="simple" xlink:role="http://www.xbrl.org/2003/role/referenceLinkbaseRef" xlink:arcrole="http://www.w3.org/1999/xlink/properties/linkbase" xlink:href="core-ref-sme.xml"/> \n',
        '\t\t\t<link:linkbaseRef xlink:type="simple" xlink:role="http://www.xbrl.org/2003/role/referenceLinkbaseRef" xlink:arcrole="http://www.w3.org/1999/xlink/properties/linkbase" xlink:href="core-ref-jp-pint.xml"/> \n'
        # '\t\t\t<!-- formula -->\n',
        # '\t\t\t<link:linkbaseRef xlink:type="simple" xlink:arcrole="http://www.w3.org/1999/xlink/properties/linkbase" xlink:href="core-for-Mandatory-Base.xml"/> \n',
        # '\t\t\t<link:linkbaseRef xlink:type="simple" xlink:arcrole="http://www.w3.org/1999/xlink/properties/linkbase" xlink:href="core-for-Mandatory-GL.xml"/> \n',
        # '\t\t\t<link:linkbaseRef xlink:type="simple" xlink:arcrole="http://www.w3.org/1999/xlink/properties/linkbase" xlink:href="core-for-Mandatory-O2C.xml"/> \n',
        # '\t\t\t<link:linkbaseRef xlink:type="simple" xlink:arcrole="http://www.w3.org/1999/xlink/properties/linkbase" xlink:href="core-for-Mandatory-P2P.xml"/> \n',
        # '\t\t\t<link:linkbaseRef xlink:type="simple" xlink:arcrole="http://www.w3.org/1999/xlink/properties/linkbase" xlink:href="core-for-Mandatory-Core.xml"/> \n',
        # '\t\t\t<link:linkbaseRef xlink:type="simple" xlink:arcrole="http://www.w3.org/1999/xlink/properties/linkbase" xlink:href="core-for-Card-Base.xml"/> \n',
        # '\t\t\t<link:linkbaseRef xlink:type="simple" xlink:arcrole="http://www.w3.org/1999/xlink/properties/linkbase" xlink:href="core-for-Card-GL.xml"/> \n',
        # '\t\t\t<link:linkbaseRef xlink:type="simple" xlink:arcrole="http://www.w3.org/1999/xlink/properties/linkbase" xlink:href="core-for-Card-O2C.xml"/> \n',
        # '\t\t\t<link:linkbaseRef xlink:type="simple" xlink:arcrole="http://www.w3.org/1999/xlink/properties/linkbase" xlink:href="core-for-Card-P2P.xml"/> \n',
        # '\t\t\t<link:linkbaseRef xlink:type="simple" xlink:arcrole="http://www.w3.org/1999/xlink/properties/linkbase" xlink:href="core-for-Card-Core.xml"/> \n',
    ]
    lines += html_annotation_head

    html = [
        '\t\t\t<!-- \n',
        '\t\t\t\trole type\n',
        '\t\t\t-->\n'
        f'\t\t\t<link:roleType id="japan-core-role" roleURI="http://www.xbrl.jp/japan-core/role">\n',
        f'\t\t\t\t<link:definition>link japan-core</link:definition>\n',
        f'\t\t\t\t<link:usedOn>link:definitionLink</link:usedOn>\n',
        f'\t\t\t\t<link:usedOn>link:presentationLink</link:usedOn>\n',
        '\t\t\t</link:roleType>\n',
    ]
    for adc_id,role in roleMap.items():
        role_id = role["role_id"]
        URI     = role['URI']
        link_id = role['link_id']
        html.append(f'\t\t\t<link:roleType id="{role_id}" roleURI="http://www.xbrl.jp/japan-core/role{URI}">\n')
        # html.append(f'\t\t\t\t<link:definition>{source_den} to {target_den}</link:definition>\n')
        html.append(f'\t\t\t\t<link:usedOn>link:definitionLink</link:usedOn>\n')
        html.append('\t\t\t</link:roleType>\n')
    lines += html

    html = [
        '\t\t\t<!--\n',
        '\t\t\t\tdescription: roleType arcroleType\n',
        '\t\t\t-->\n'
        '\t\t\t<link:roleType id="description" roleURI="http://www.xbrl.jp/japan-core/role/description">\n',
        '\t\t\t\t<link:definition>description</link:definition>\n',
        '\t\t\t\t<link:usedOn>link:label</link:usedOn>\n',
        '\t\t\t</link:roleType>\n',
        '\t\t\t<link:arcroleType id="concept-description" cyclesAllowed="undirected" arcroleURI="http://www.xbrl.jp/japan-core/arcrole/concept-description">\n',
        '\t\t\t\t<link:definition>concept to description</link:definition>\n',
        '\t\t\t\t<link:usedOn>link:labelArc</link:usedOn>\n',
        '\t\t\t</link:arcroleType >\n',
    ]
    lines += html

    html = [
        '\t\t\t<!--\n',
        '\t\t\t\tprimary key: roleType arcroleType\n',
        '\t\t\t-->\n'
        '\t\t\t<link:roleType id="primary-key" roleURI="http://www.xbrl.jp/japan-core/role/primary-key">\n',
        '\t\t\t\t<link:definition>primary key</link:definition>\n',
        '\t\t\t\t<link:usedOn>link:definitionLink</link:usedOn>\n',
        '\t\t\t</link:roleType>\n',
        '\t\t\t<link:arcroleType id="concept-primary-key" cyclesAllowed="undirected" arcroleURI="http://www.xbrl.jp/japan-core/arcrole/concept-primary-key">\n',
        '\t\t\t\t<link:definition>concept primary key</link:definition>\n',
        '\t\t\t\t<link:usedOn>link:definitionArc</link:usedOn>\n',
        '\t\t\t</link:arcroleType >\n',
    ]
    lines += html

    html = [
        '\t\t\t<!--\n',
        '\t\t\t\treference identifier: roleType arcroleType\n',
        '\t\t\t-->\n'
        '\t\t\t<link:roleType id="reference-identifier" roleURI="http://www.xbrl.jp/japan-core/role/reference-identifier">\n',
        '\t\t\t\t<link:definition>reference identifier</link:definition>\n',
        '\t\t\t\t<link:usedOn>link:definitionLink</link:usedOn>\n',
        '\t\t\t</link:roleType>\n',
        '\t\t\t<link:arcroleType id="concept-reference-identifier" cyclesAllowed="undirected" arcroleURI="http://www.xbrl.jp/japan-core/arcrole/concept-reference-identifier">\n',
        '\t\t\t\t<link:definition>concept reference identifier</link:definition>\n',
        '\t\t\t\t<link:usedOn>link:definitionArc</link:usedOn>\n',
        '\t\t\t</link:arcroleType >\n',
    ]
    lines += html

    html = [
        '\t\t\t<!--\n',
        '\t\t\t\trequire: roleType\n',
        '\t\t\t-->\n'
        '\t\t\t<link:roleType id="require" roleURI="http://www.xbrl.jp/japan-core/role/require">\n',
        '\t\t\t\t<link:definition>require</link:definition>\n',
        '\t\t\t\t<link:usedOn>link:definitionLink</link:usedOn>\n',
        '\t\t\t</link:roleType>\n',
    ]
    lines += html

    html_annotation_tail = [
        '\t\t</appinfo>\n',
        '\t</annotation>\n'
    ]
    lines += html_annotation_tail

    html_type = [
        '\t<!-- typed dimension referenced element -->\n',
        '\t<element name="_v" id="_v">\n',
        '\t\t<simpleType>\n',
        '\t\t\t<restriction base="string"/>\n',
        '\t\t</simpleType>\n',
        '\t</element>\n',
        '\t<element name="_activity" id="_activity">\n',
        '\t\t<simpleType>\n',
        '\t\t\t<restriction base="string">\n',
        '\t\t\t\t<pattern value="\s*(Created|Approved|LastModified|Entered|Posted)\s*"/>\n',
        '\t\t\t</restriction>\n',
        '\t\t</simpleType>\n',
        '\t</element>\n'
    ]
    lines += html_type

    html_part_type = [
        '\t<!-- reference part element -->\n',
        '\t<!-- semantic-model -->\n',
        '\t<element name="id" type="string" substitutionGroup="link:part"/>\n',
        '\t<element name="semantic_sort" type="string" substitutionGroup="link:part"/>\n',
        '\t<element name="section" type="string" substitutionGroup="link:part"/>\n',
        '\t<element name="cardinality" type="string" substitutionGroup="link:part"/>\n',
        '\t<element name="aligned_cardinality" type="string" substitutionGroup="link:part"/>\n',
        '\t<element name="semantic_datatype" type="string" substitutionGroup="link:part"/>\n',
        '\t<element name="business_term" type="string" substitutionGroup="link:part"/>\n',
        '\t<element name="business_term_ja" type="string" substitutionGroup="link:part"/>\n',
        '\t<element name="description" type="string" substitutionGroup="link:part"/>\n',
        '\t<element name="description_ja" type="string" substitutionGroup="link:part"/>\n',
        '\t<element name="example" type="string" substitutionGroup="link:part"/>\n',
        '\t<element name="xpath" type="string" substitutionGroup="link:part"/>\n',
        '\t<!-- syntax-binding -->\n',
        '\t<element name="element" type="string" substitutionGroup="link:part"/>\n',
        '\t<element name="syntax_sort" type="string" substitutionGroup="link:part"/>\n',
        '\t<element name="syntax_cardinality" type="string" substitutionGroup="link:part"/>\n',
        '\t<element name="parent_xpath" type="string" substitutionGroup="link:part"/>\n',
        '\t<element name="syntax_parent_sort" type="string" substitutionGroup="link:part"/>\n',
        '\t<element name="syntax_parent_cardinality" type="string" substitutionGroup="link:part"/>\n',
    ]
    lines += html_part_type

    # Hypercube
    html_hypercube = [
        '\t<!-- Hypercube -->\n'
    ]
    for adc_id,role in roleMap.items():
        link_id = role['link_id']
        html_hypercube.append(f'\t<element name="h_{link_id}" id="h_{link_id}" substitutionGroup="xbrldt:hypercubeItem" type="xbrli:stringItemType" nillable="true" abstract="true" xbrli:periodType="instant"/>\n')
    lines += html_hypercube

    # Dimension
    html_dimension = [
        '\t<!-- Dimension -->\n'
    ]
    for adc_id,role in roleMap.items():
        link_id = role['link_id']
        html_dimension.append(f'\t<element name="d_{link_id}" id="d_{link_id}" substitutionGroup="xbrldt:dimensionItem" type="xbrli:stringItemType" abstract="true" xbrli:periodType="instant" xbrldt:typedDomainRef="#_v"/>\n')
    lines += html_dimension

    # item complexType
    html_itemtype = [
        '\t<!-- item type -->\n'
    ]
    complexType = [
        '\t<complexType name="stringItemType">\n',
        '\t\t<simpleContent>\n',
        '\t\t\t<restriction base="xbrli:stringItemType"/>\n',
        '\t\t</simpleContent>\n',
        '\t</complexType>\n',
    ]
    html_itemtype += complexType
    for name,type in datatypeMap.items():
        adc = type['adc']
        xbrli = type['xbrli']
        complexType = [
            f'\t<complexType name="{adc}">\n',
            '\t\t<simpleContent>\n',
            f'\t\t\t<restriction base="xbrli:{xbrli}"/>\n',
            '\t\t</simpleContent>\n',
            '\t</complexType>\n',
        ]
        html_itemtype += complexType
    lines += html_itemtype

    # element
    lines.append('\t<!-- element -->\n')
    elementsDefined = set()
    primaryKeys = {}
    for adc_id,record in adcDict.items():
        defineElement(adc_id,record)
        
    lines.append('</schema>')

    adc_xsd_file = file_path(f'{xbrl_base}/{core_xsd}')
    with open(adc_xsd_file, 'w', encoding='utf-8-sig', newline='') as f:
        f.writelines(lines)
    if VERBOSE:
        print(f'-- {adc_xsd_file}')

    ###################################
    # labelLink en
    #
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>\n',
        '<!--  (c) 2023 XBRL Japan inc. -->\n',
        '<link:linkbase\n',
        '\txmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n',
        '\txmlns:link="http://www.xbrl.org/2003/linkbase"\n',
        '\txmlns:xlink="http://www.w3.org/1999/xlink"\n',
        '\txsi:schemaLocation="http://www.xbrl.org/2003/linkbase http://www.xbrl.org/2003/xbrl-linkbase-2003-12-31.xsd">\n',
        f'\t<!--link:roleRef roleURI="http://www.xbrl.jp/japan-core/role/description" xlink:type="simple" xlink:href="{core_xsd}#description"/>\n',
        f'\t<link:arcroleRef arcroleURI="http://www.xbrl.jp/japan-core/arcrole/concept-description" xlink:type="simple" xlink:href="{core_xsd}#concept-description"/-->\n',
        '\t<link:labelLink xlink:type="extended" xlink:role="http://www.xbrl.org/2003/role/link">\n'
    ]
    # locsDefined = {}
    # arcsDefined = {}
    # definedLabels = {}
    # for adc_id,record in adcDict.items():
    #     kind = record['kind']
    #     if 'Aggregation'==kind:
    #         term = getRecord(record['associatedClass'])['property'] if record['associatedClass'] else record['property']
    #     elif 'Attribute'==kind:
    #         term = record['property'] # titleCase(record['propertyTerm'])
    #     if len(term) > 0:
    #         linkLabelTerm(adc_id,term,'ja')

    # # for adc_id,referenced_id in targetRefDict.items():
    # #     record = getRecord(referenced_id)
    # #     name = record['name']
    # #     if len(name) > 0:
    # #         linkLabelTerm(adc_id,name,'en')
    # #         adc_id = f'{adc_id[:LEN_KEY]}-{referenced_id}'
    # #         linkLabelTerm(adc_id,name,'en')

    lines.append('\t</link:labelLink>\n')
    lines.append('</link:linkbase>\n')

    adc_label_file = file_path(f'{xbrl_base}/{core_label}-en.xml')
    with open(adc_label_file, 'w', encoding='utf-8-sig', newline='') as f:
        f.writelines(lines)
    if VERBOSE:
        print(f'-- {adc_label_file}')

    ###################################
    # labelLink ja
    #
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>\n',
        '<!--  (c) 2023 XBRL Japan inc. -->\n',
        '<link:linkbase\n',
        '\txmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n',
        '\txmlns:link="http://www.xbrl.org/2003/linkbase"\n',
        '\txmlns:xlink="http://www.w3.org/1999/xlink"\n',
        '\txsi:schemaLocation="http://www.xbrl.org/2003/linkbase http://www.xbrl.org/2003/xbrl-linkbase-2003-12-31.xsd">\n',
        f'\t<link:roleRef roleURI="http://www.xbrl.jp/japan-core/role/description" xlink:type="simple" xlink:href="{core_xsd}#description"/>\n',
        f'\t<link:arcroleRef arcroleURI="http://www.xbrl.jp/japan-core/arcrole/concept-description" xlink:type="simple" xlink:href="{core_xsd}#concept-description"/>\n',
        '\t<link:labelLink xlink:type="extended" xlink:role="http://www.xbrl.org/2003/role/link">\n'
    ]
    locsDefined = {}
    arcsDefined = {}
    definedLabels = {}
    definedDescs = {}
    definedDescArcs = {}

    for adc_id,record in adcDict.items():
        kind = record['kind']
        name = record['property']
        desc = record['desc'] if 'desc' in record else None
        if len(name) > 0:
            linkLabel(adc_id,name,desc,'ja')

    lines.append('\t</link:labelLink>\n')
    lines.append('</link:linkbase>\n')

    adc_label_file = file_path(f'{xbrl_base}/{core_label}-ja.xml')
    with open(adc_label_file, 'w', encoding='utf-8-sig', newline='') as f:
        f.writelines(lines)
    if VERBOSE:
        print(f'-- {adc_label_file}')

    ###################################
    #   presentationLink
    #
    locsDefined = {}
    arcsDefined = {}
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>\n',
        '<!--  (c) 2023 XBRL Japan inc. -->\n',
        '<link:linkbase\n',
        '\txmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n',
        '\txsi:schemaLocation="http://www.xbrl.org/2003/linkbase http://www.xbrl.org/2003/xbrl-linkbase-2003-12-31.xsd"\n',
        '\txmlns:link="http://www.xbrl.org/2003/linkbase"\n',
        '\txmlns:xlink="http://www.w3.org/1999/xlink">\n',
        f'\t<link:roleRef roleURI="http://www.xbrl.jp/japan-core/role" xlink:type="simple" xlink:href="{core_xsd}#japan-core-role"/>\n',
        '\t<link:presentationLink xlink:type="extended" xlink:role="http://www.xbrl.jp/japan-core/role">\n',
    ]
    locsDefined = {}
    arcsDefined = {}
    # for record in [x for x in records if 'ABIE'==x['kind']]:
    record = [x for x in records if 'Aggregation'==x['kind']][0]
    adc_id = record['adc_id']
    kind   = record['kind']
    count  = 0
    children = record['children']
    linkPresentation(adc_id,children,1)

    lines.append('\t</link:presentationLink>\n')
    lines.append('</link:linkbase>\n')

    adc_presentation_file = file_path(f'{xbrl_base}/{core_presentation}.xml')
    with open(adc_presentation_file, 'w', encoding='utf-8-sig', newline='') as f:
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
        '<!--(c) 2023 XBRL Japan inc. -->\n',
        '<link:linkbase\n',
        '\txmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n',
        '\txsi:schemaLocation="http://www.xbrl.org/2003/linkbase http://www.xbrl.org/2003/xbrl-linkbase-2003-12-31.xsd"\n',
        '\txmlns:link="http://www.xbrl.org/2003/linkbase"\n',
        '\txmlns:xbrldt="http://xbrl.org/2005/xbrldt"\n',
        '\txmlns:xlink="http://www.w3.org/1999/xlink">\n'
    ]
    lines.append('\t<!-- roleRef -->\n')

    for role in roleMap.values():
        role_id = role["role_id"]
        link_id = role['link_id']
        URI = f"/{role_id}"
        lines.append(f'\t<link:roleRef roleURI="http://www.xbrl.jp/japan-core/role{URI}" xlink:type="simple" xlink:href="{core_xsd}#{role_id}"/>\n')
    html = [
        f'\t<link:roleRef roleURI="http://www.xbrl.jp/japan-core/role/primary-key" xlink:type="simple" xlink:href="{core_xsd}#primary-key"/>\n',
        f'\t<link:roleRef roleURI="http://www.xbrl.jp/japan-core/role/reference-identifier" xlink:type="simple" xlink:href="{core_xsd}#reference-identifier"/>\n',
        f'\t<link:roleRef roleURI="http://www.xbrl.jp/japan-core/role/require" xlink:type="simple" xlink:href="{core_xsd}#require"/>\n',
        '\t<!-- arcroleRef -->\n',
        '\t<link:arcroleRef arcroleURI="http://xbrl.org/int/dim/arcrole/all" xlink:type="simple" xlink:href="http://www.xbrl.org/2005/xbrldt-2005.xsd#all"/>\n',
        '\t<link:arcroleRef arcroleURI="http://xbrl.org/int/dim/arcrole/domain-member" xlink:type="simple" xlink:href="http://www.xbrl.org/2005/xbrldt-2005.xsd#domain-member"/>\n',
        '\t<link:arcroleRef arcroleURI="http://xbrl.org/int/dim/arcrole/hypercube-dimension" xlink:type="simple" xlink:href="http://www.xbrl.org/2005/xbrldt-2005.xsd#hypercube-dimension"/>\n',
        '\t<link:arcroleRef arcroleURI="http://xbrl.org/int/dim/arcrole/dimension-domain" xlink:type="simple" xlink:href="http://www.xbrl.org/2005/xbrldt-2005.xsd#dimension-domain"/>\n',
        f'\t<link:arcroleRef arcroleURI="http://www.xbrl.jp/japan-core/arcrole/concept-primary-key" xlink:type="simple" xlink:href="{core_xsd}#concept-primary-key"/>\n',
        f'\t<link:arcroleRef arcroleURI="http://www.xbrl.jp/japan-core/arcrole/concept-reference-identifier" xlink:type="simple" xlink:href="{core_xsd}#concept-reference-identifier"/>\n',
    ]
    lines += html

    for adc_id,role in roleMap.items():
        count = 0
        defineHypercube(adc_id)

    lines.append('</link:linkbase>\n')

    adc_definition_file = file_path(f'{xbrl_base}/{core_definition}.xml')
    with open(adc_definition_file, 'w', encoding='utf-8-sig', newline='') as f:
        f.writelines(lines)
    if VERBOSE:
        print(f'-- {adc_definition_file}')

    ###################################
    # referenceLink SME Common EDI
    #
    lines = []
    html = [
        '<?xml version="1.0" encoding="UTF-8"?>\n',
        '<!--  (c) 2023 XBRL Japan inc. -->\n',
        '<link:linkbase\n',
        '\txmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n',
        '\txmlns:adc="http://www.xbrl.jp/japan-core"\n',
        '\txmlns:link="http://www.xbrl.org/2003/linkbase"\n',
        '\txmlns:xlink="http://www.w3.org/1999/xlink"\n',
        '\txsi:schemaLocation="http://www.xbrl.org/2003/linkbase http://www.xbrl.org/2003/xbrl-linkbase-2003-12-31.xsd http://www.xbrl.jp/japan-core core.xsd">\n',
        '\t<link:referenceLink xlink:type="extended" xlink:role="http://www.xbrl.org/2003/role/link">\n'
    ]
    lines += html

    for record in adcDict.values():
        adc_id        = record['adc_id']
        seqSme        = record['seqSme'] # '1'
        idSme         = record['idSme'] # ''
        kindSme       = record['kindSme'] # 'MA'
        termSme       = record['termSme'] # 'Invoice'
        termSme_ja    = record['termSme_ja'] # '統合請求書'
        defSme_ja     = record['defSme_ja'] # '受注者が発注者に交付する統合請求文書（メッセージ）'
        cardSme       = record['cardSme'] if '-'!=record['cardSme'] else '' # '－'
        fixedValueSme = record['fixedValueSme'] # ''
        xPathSme      = record['xPathSme'] # '/SMEInvoice'
        html = [
            f'\t\t<!-- {adc_id} {termSme} --> \n',
            f'\t\t<link:loc xlink:type="locator" xlink:href="core.xsd#{adc_id}" xlink:label="{adc_id}"/> \n',
            f'\t\t<link:referenceArc xlink:type="arc" xlink:from="{adc_id}" xlink:to="{adc_id}_REF" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-reference"/> \n',
            f'\t\t<link:reference xlink:type="resource" xlink:label="{adc_id}_REF" xlink:role="http://www.xbrl.org/2003/role/definitionRef"> \n',
            f'\t\t\t<adc:id>{adc_id}</adc:id> \n',
            f'\t\t\t<!--adc:cardinality>1..1</adc:cardinality--> \n',
            f'\t\t\t<adc:business_term>{termSme}</adc:business_term> \n',
            f'\t\t\t<adc:business_term_ja>{termSme_ja}</adc:business_term_ja> \n',
            f'\t\t\t<adc:xpath>{xPathSme}</adc:xpath> \n',
            f'\t\t</link:reference> \n',
            f'\t\t<link:reference xlink:type="resource" xlink:label="{adc_id}_REF" xlink:role="http://www.xbrl.org/2003/role/presentationRef"> \n',
            f'\t\t\t<adc:element>{xPathSme}</adc:element> \n',
            f'\t\t\t<adc:syntax_sort>{seqSme}</adc:syntax_sort> \n',
            f'\t\t\t<adc:syntax_cardinality>{cardSme}</adc:syntax_cardinality> \n',
            f'\t\t</link:reference> \n',
            f'\t\t<link:reference xlink:type="resource" xlink:label="{adc_id}_REF" xlink:role="http://www.xbrl.org/2003/role/commentaryRef"> \n',
            f'\t\t\t<!--adc:description>Commercial invoice</adc:description--> \n',
            f'\t\t\t<adc:description_ja>{defSme_ja}</adc:description_ja> \n',
            f'\t\t</link:reference> \n'
        ]
        lines += html

    lines.append('</link:referenceLink> \n')
    lines.append('</link:linkbase> \n')

    adc_referemce_file_sme = file_path(f'{xbrl_base}/{core_reference}-sme.xml')
    with open(adc_referemce_file_sme, 'w', encoding='utf-8-sig', newline='') as f:
        f.writelines(lines)
    if VERBOSE:
        print(f'-- {adc_referemce_file_sme}')

    ###################################
    # referenceLink SME Common JP PINT
    #
    lines = []
    html = [
        '<?xml version="1.0" encoding="UTF-8"?>\n',
        '<!--  (c) 2023 XBRL Japan inc. -->\n',
        '<link:linkbase\n',
        '\txmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n',
        '\txmlns:adc="http://www.xbrl.jp/japan-core"\n',
        '\txmlns:link="http://www.xbrl.org/2003/linkbase"\n',
        '\txmlns:xlink="http://www.w3.org/1999/xlink"\n',
        '\txsi:schemaLocation="http://www.xbrl.org/2003/linkbase http://www.xbrl.org/2003/xbrl-linkbase-2003-12-31.xsd http://www.xbrl.jp/japan-core core.xsd">\n',
        '\t<link:referenceLink xlink:type="extended" xlink:role="http://www.xbrl.org/2003/role/link">\n'
    ]
    lines += html

    for record in adcDict.values():
        adc_id         = record['adc_id']
        seqPint        = record['seqPint'] # '1'
        idPint         = record['idPint'] # ''
        levelPint      = record['levelPint'] # ''
        termPint_ja    = record['termPint_ja'] # '請求書'
        termPint       = record['termPint'] # ''
        cardPint       = record['cardPint'] # ''
        fixedValuePint = record['fixedValuePint'] # ''
        xPathPint      = record['xPathPint'] # ''
        html = [
            f'\t\t<!-- {adc_id} {termPint} --> \n',
            f'\t\t<link:loc xlink:type="locator" xlink:href="core.xsd#{adc_id}" xlink:label="{adc_id}"/> \n',
            f'\t\t<link:referenceArc xlink:type="arc" xlink:from="{adc_id}" xlink:to="{adc_id}_REF" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-reference"/> \n',
            f'\t\t<link:reference xlink:type="resource" xlink:label="{adc_id}_REF" xlink:role="http://www.xbrl.org/2003/role/definitionRef"> \n',
            f'\t\t\t<adc:id>{adc_id}</adc:id> \n',
            f'\t\t\t<!--adc:cardinality>1..1</adc:cardinality--> \n',
            f'\t\t\t<adc:business_term>{termPint}</adc:business_term> \n',
            f'\t\t\t<adc:business_term_ja>{termPint_ja}</adc:business_term_ja> \n',
            f'\t\t\t<adc:xpath>{xPathPint}</adc:xpath> \n',
            f'\t\t</link:reference> \n',
            f'\t\t<link:reference xlink:type="resource" xlink:label="{adc_id}_REF" xlink:role="http://www.xbrl.org/2003/role/presentationRef"> \n',
            f'\t\t\t<adc:element>{xPathPint}</adc:element> \n',
            f'\t\t\t<adc:syntax_sort>{seqPint}</adc:syntax_sort> \n',
            f'\t\t\t<adc:syntax_cardinality>{cardPint}</adc:syntax_cardinality> \n',
            f'\t\t</link:reference> \n',
            f'\t\t<link:reference xlink:type="resource" xlink:label="{adc_id}_REF" xlink:role="http://www.xbrl.org/2003/role/commentaryRef"> \n',
            f'\t\t\t<!--adc:description>Commercial invoice</adc:description--> \n',
            f'\t\t\t<!--adc:description_ja>defPint_ja</adc:description_ja--> \n',
            f'\t\t</link:reference>\n'
        ]
        lines += html

    lines.append('\t</link:referenceLink>\n')
    lines.append('</link:linkbase> \n')

    adc_referemce_file_jp_pint = file_path(f'{xbrl_base}/{core_reference}-jp-pint.xml')
    with open(adc_referemce_file_jp_pint, 'w', encoding='utf-8-sig', newline='') as f:
        f.writelines(lines)
    if VERBOSE:
        print(f'-- {adc_referemce_file_jp_pint}')

    print('** END **')