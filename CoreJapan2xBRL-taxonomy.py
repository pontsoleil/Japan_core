#!/usr/bin/env python3
# coding: utf-8
#
# generate Core Japan xBRL-GD Taxonomy fron core_japan.csv
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
# from cgi import print_directory
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

xbrl_source = 'source/'
xbrl_source = xbrl_source.replace('/', SEP)
# core_head = 'corehead.txt'
# primarykey_file = 'primarykey.csv'

xbrl_base = 'taxonomy/H/'
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
    'Itermtifier': {
        'adc':'itermtifierItemType',
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
    'REF':'Reference Itermtifier',
    'RFC':'Request For Comments',
    'SAL':'Sales',
    'TIN':'Tax Itermtification Number',
    'TRX':'Transactional',
    'UOM':'Unit of Measurement',
    'WIP':'Work In Progress'
}

targetTables = ['GL02','GL03']

duplicateNames = set()
names = set()
coreDict = {}
targetRefDict = {}
associationDict = {}
referenceDict = {}
childRefDict = {}
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

# # lower camel case concatenate
# def LC3(term):
#     if not term:
#         return ''
#     terms = term.split(' ')
#     name = ''
#     for i in range(len(terms)):
#         if i == 0:
#             if 'TAX' == terms[i]:
#                 name += terms[i].lower()
#             elif len(terms[i]) > 0:
#                 name += terms[i][0].lower() + terms[i][1:]
#         else:
#             name += terms[i][0].upper() + terms[i][1:]
#     return name

# # snake concatenate
# def SC(term):
#     if not term:
#         return ''
#     terms = term.split(' ')
#     name = '_'.join(terms)
#     return name

def getTerm(core_id):
    if core_id in coreDict:
        record = coreDict[core_id]
        return record['term']
    return ''

# def getTerm(core_id):
#     if core_id in coreDict:
#         record = coreDict[core_id]
#         return record['term']
#     return ''

# def getLC3_term(core_id):
#     term = getTerm(core_id)
#     if term:
#         term = term[:term.find('.')]
#         return LC3(term)
#     return ''

# def getClassName(core_id):
#     term = getTerm(core_id)
#     if term:
#         cn = term[5:term.find('.')]
#         return cn
#     return ''

# def coreDict[core_id]:
#     if core_id in coreDict:
#         record = coreDict[core_id]
#     else:
#         target_id = core_id[-4:]
#         record = coreDict[target_id] #2023-02-06
#     return record

def getParent(parent_id_list):
    parent_id = parent_id_list[-1]
    if parent_id in coreDict:
        parent = coreDict[parent_id]
    else:
        parent = None
    return parent

def getChildren(core_id):
    if core_id in coreDict:
        record = coreDict[core_id]
        return record['children']
    return []

def defineHypercube(core_id, role,n):
    global lines
    global locsDefined
    global arcsDefined
    global targetRefDict
    global referenceDict
    root_id = None
    root_id = core_id
    # if not root_id in coreDict:
    #     print(f'** {root_id} is not defined.')
    #     return None    
    # root = coreDict[root_id]
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
    if -1==core_id.find('_'):
        root = coreDict[root_id]
        root_dimension = f"d_{root_id}"
        dimension_id_list.add(root_dimension)
    else:#if 9==len(core_id):
        root_id = link_id[1+link_id.find('_'):]# link_id[5:]
        root_dimension_id = f'd_{root_id}'
        dimension_id_list.add(root_dimension_id)
        root = coreDict[root_id]
        source_id = link_id[:link_id.find('_')]# link_id[:4]
        source_dimension = f'd_{source_id}'
        dimension_id_list.add(source_dimension)
        # anchor_id = [x for x in childRefDict[root_id]['source'] if source_id==x][0]
        if source_id in childRefDict:
            origin = childRefDict[source_id]
            origin_id = origin['source'][0]
            # origin_id = origin_id[:4]
            # anchor_id = f'{origin_id}_{source_id}'
            origin_dimension = f'd_{origin_id}'
            dimension_id_list.add(origin_dimension)
    lines.append(f'    <link:definitionLink xlink:type="extended" xlink:role="http://www.xbrl.jp/core-japan/role{URI}">\n')
    # all (has-hypercube)
    lines.append(f'        <!-- {link_id} all (has-hypercube) {hypercube_id} {role_id} -->\n')
    lines.append(f'        <link:loc xlink:type="locator" xlink:href="{core_xsd}#{link_id}" xlink:label="{link_id}" xlink:title="{link_id}"/>\n')
    lines.append(f'        <link:loc xlink:type="locator" xlink:href="{core_xsd}#{hypercube_id}" xlink:label="{hypercube_id}" xlink:title="{hypercube_id}"/>\n')
    lines.append(f'        <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/all" xlink:from="{link_id}" xlink:to="{hypercube_id}" xlink:title="all (has-hypercube): {link_id} to {hypercube_id}" order="1" xbrldt:closed="true" xbrldt:contextElement="segment"/>\n')
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
            # alias_id = not link_id[:4] in child_id and f"{link_id[:4]}-{child_id}" or child_id
            alias_id = child_id
            child = coreDict[child_id]#[-8:]]
            child_kind = child['id'][:3]
            if child_id in targetRefDict:
                if 'JBG'!=child_kind or 'n'!=child['card'][-1:]:
                    if not alias_id in locsDefined[link_id]:
                        locsDefined[link_id].add(alias_id)
                        lines.append(f'        <link:loc xlink:type="locator" xlink:href="{core_xsd}#{alias_id}" xlink:label="{alias_id}" xlink:title="{alias_id}"/>\n')
                    count += 1
                    arc_id = f'{link_id} {alias_id}'
                    if not arc_id in arcsDefined[link_id]:
                        arcsDefined[link_id].add(arc_id)
                        lines.append(f'        <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="{link_id}" xlink:to="{alias_id}" xlink:title="domain-member: {link_id} to {alias_id}" order="{count}"/>\n')
                # targetRole
                target_id = targetRefDict[child_id]
                target_id = f'{target_id}_{child_id}'
                role_id = f'link_{target_id}'
                URI = f'/{role_id}'
                lines.append(f'        <!-- {child_id} targetRole {role_id} -->\n')
                if not target_id in locsDefined[link_id]:
                    locsDefined[link_id].add(target_id)
                    lines.append(f'        <link:loc xlink:type="locator" xlink:href="{core_xsd}#{target_id}" xlink:label="{target_id}" xlink:title="{target_id}"/>\n')
                count += 1
                arc_id = f'{link_id} {target_id}'
                if not arc_id in arcsDefined[link_id]:
                    arcsDefined[link_id].add(arc_id)
                    lines.append(f'        <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xbrldt:targetRole="http://www.xbrl.jp/core-japan/role{URI}" xlink:from="{link_id}" xlink:to="{target_id}" xlink:title="domain-member: {link_id} to {target_id} in {role_id}" order="{count}"/>\n')
            else:
                if 'JBG'==child_kind and '1'==child['card'][-1:]:
                    # targetRole
                    target_id = child_id
                    target_id = f'{target_id}_{child_id}'
                    role_id = f'link_{target_id}'
                    URI = f'/{role_id}'
                    lines.append(f'        <!-- {child_id} targetRole {role_id} -->\n')
                    if not target_id in locsDefined[link_id]:
                        locsDefined[link_id].add(target_id)
                        lines.append(f'        <link:loc xlink:type="locator" xlink:href="{core_xsd}#{target_id}" xlink:label="{target_id}" xlink:title="{target_id}"/>\n')
                    count += 1
                    arc_id = f'{link_id} {target_id}'
                    if not arc_id in arcsDefined[link_id]:
                        arcsDefined[link_id].add(arc_id)
                        lines.append(f'        <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xbrldt:targetRole="http://www.xbrl.jp/core-japan/role{URI}" xlink:from="{link_id}" xlink:to="{target_id}" xlink:title="domain-member: {link_id} to {target_id} in {role_id}" order="{count}"/>\n')
                else:
                    if not alias_id in locsDefined[link_id]:
                        locsDefined[link_id].add(alias_id)
                        lines.append(f'        <link:loc xlink:type="locator" xlink:href="{core_xsd}#{alias_id}" xlink:label="{alias_id}" xlink:title="{alias_id}"/>\n')
                    count += 1
                    arc_id = f'{link_id} {alias_id}'
                    if not arc_id in arcsDefined[link_id]:
                        arcsDefined[link_id].add(arc_id)
                        lines.append(f'        <link:definitionArc xlink:type="arc" xlink:arcrole="http://xbrl.org/int/dim/arcrole/domain-member" xlink:from="{link_id}" xlink:to="{alias_id}" xlink:title="domain-member: {link_id} to {alias_id}" order="{count}"/>\n')

    lines.append('    </link:definitionLink>\n')

# def addChild(parent_id_list,core_id):
#     record = coreDict[core_id]
#     if not record:
#         return
#     parent = getParent(parent_id_list)
#     if not parent:
#         return
#     if not core_id in coreDict:
#         print(core_id)
#     if not 'children' in parent:
#         parent['children'] = []
#     if not core_id in parent['children']:
#         parent['children'].append(core_id)
#     if DEBUG:
#         print(f'   {parent_id_list} add {core_id}')
#     return core_id

# def addChildren(parent_id_list,core_id):
#     global targetRefDict
#     global referenceDict
#     record = coreDict[core_id]
#     if not record:
#         return
#     kind = record['kind']
#     ref_id = None
#     targetRef_id = None
#     if kind in ['IDBIE','BBIE']:
#         if DEBUG: print(f'(a) addChild( {parent_id_list}, {core_id} )[{kind}]{core_id}({core_id})')
#         addChild(parent_id_list,core_id)
#     elif 'RFBIE'==kind:
#         if DEBUG: print(f'(a) addChild( {parent_id_list}, {core_id} )[{kind}]{core_id}({core_id})')
#         addChild(parent_id_list,core_id)
#     elif 'ABIE'==kind:
#         if core_id in associationDict:
#             ref_id = associationDict[core_id]
#             if DEBUG: print(f'(b) addChild ( {parent_id_list}, {core_id} )<{kind}>{ref_id}({ref_id})')
#         elif core_id in targetRefDict:
#             targetRef_id =  targetRefDict[core_id]
#             if DEBUG: print(f'(c) addChild ( {parent_id_list}, {core_id} )<{kind}>{targetRef_id}({targetRef_id})')
#     elif 'ASBIE'==kind:# and 'n'==record['occMax']:
#         record2 = None
#         if core_id in associationDict:
#             ref_id = associationDict[core_id]
#             record2 = coreDict[ref_id]
#             if DEBUG: print(f'(c) addChild( {parent_id_list}, {core_id} )<{kind}>{ref_id}({ref_id})')
#             addChild(parent_id_list,core_id)
#             parent_id_list += [core_id]
#         elif core_id in targetRefDict:
#             targetRef_id = targetRefDict[core_id]
#             record2 = coreDict[targetRef_id]
#             if DEBUG: print(f'(c) addChild( {parent_id_list}, {core_id} )<{kind}>{targetRef_id}({targetRef_id})')
#             addChild(parent_id_list,core_id)
#             parent_id_list += [core_id]
#         else:
#             associatedClass = record['associatedClass']
#             for adc2_id,record2 in coreDict.items():
#                 if associatedClass==record2['class']:
#                     targetRefDict[core_id] = adc2_id
#                     targetRef_id = adc2_id
#                     addChild(parent_id_list,core_id)
#                     break
#         if not record2 or not 'children' in record2:
#             print(f'-ERROR- addChildren [{kind}] {core_id}')
#         children = record2['children']
#         children0 = [x for x in children]
#         for child_id in children0:
#             child = coreDict[child_id]
#             child_kind = child['kind']
#             if 'ABIE'==child_kind:
#                 if DEBUG: print(f'(d) NOT ( {parent_id_list}, {child_id} )<{child_kind}>{child_id}({child_id})')
#             if 'ASBIE'==child_kind:# and 'n'==child['occMax']:
#                 if DEBUG: print(f'(e)*addChildren( {parent_id_list}, {child_id} )<{child_kind}>{child_id}({child_id})')
#                 addChildren(parent_id_list,child_id)
#             else:
#                 if not core_id in parent_id_list: parent_id_list += [core_id]
#                 if DEBUG: print(f'(f) addChild( {parent_id_list}, {child_id} )[{child_kind}]{child_id}({child_id})')
#                 addChild(parent_id_list,child_id)
#     parent_id_list.pop()
#     return core_id

if __name__ == '__main__':
    # Create the parser
    parser = argparse.ArgumentParser(prog='CoreJapan2xBRL-taxonomy.py',
                                     usage='%(prog)s infile -o outfile -e encoding [options] ',
                                     description='Core Japan Invoice 定義CSVファイルをxBRLタクソノミに変換')
    # Add the arguments
    parser.add_argument('inFile', metavar='infile', type=str, help='Audit data collection 定義CSVファイル')
    parser.add_argument('-o', '--outfile')  # core.xsd
    parser.add_argument('-e', '--encoding') # 'Shift_JIS' 'cp932' 'utf-8'
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-d', '--debug', action='store_true')

    args = parser.parse_args()
    in_file = None
    if args.inFile:
        in_file = args.inFile.strip()
        in_file = in_file.replace('/', SEP)
        in_file = file_path(args.inFile)
    if not in_file or not os.path.isfile(in_file):
        print('入力定義CSVファイルがありません')
        sys.exit()
    core_japan_file = in_file
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
    # 1. core_japan.csv -> schema

    records = []
    core_japan_file = file_path(core_japan_file)
    parentIDs = []
    tableDict = {}
    classDict = {}
    asbieDict = {}
    # header = ['no','module','kind','table_id','class','level','occurrence','field_id','propertyTerm','representationQualifier','representation','associatedClass','datatype','desc','type','entity','attribute','domain','refClass','refProperty','tag']
    header = ['semSort','group','id','level','card','term','desc','datatype','UN_CCL_ID','kind','smeSort','smeID','smeTerm','smeDesc','smeDefault','smeCard','smeLevel','smeXPath','pintSort','pintID','pintCard.','Level','pintTerm','pintTerm_ja','pintDesc','pintDesc_ja','pintDefault','pintDdatatype','pintXPath']
    
    with open(core_japan_file, encoding='utf-8', newline='') as f:
        reader = csv.reader(f)#, delimiter='\t')
        next(reader)
        for cols in reader:
            record = {}
            for i in range(len(cols)):
                col = cols[i]                
                record[header[i]] = col.strip()
            records.append(record)

    parentIDs = ['']*8
    childIDs = {}
    for record in records:
        core_id = record['id']
        coreDict[core_id] = record
        parentID = None
        level = record['level']
        if ''==level:
            level = 0
            parentID = 'JBG-00'
            # parentIDs[level] = core_id
            coreDict[core_id]['parent'] = [parentID]
            if not parentID in childIDs:
                childIDs[parentID] = []
            if core_id:
                childIDs[parentID].append(core_id)
        else:
            level = int(level)
            parentIDs[level] = core_id
        if not parentID in parentIDs:
            childIDs[parentID] = []
        parentIDlist = parentIDs[:level]
        coreDict[core_id]['parent'] = parentIDlist
        if len(parentIDlist) > 0:
            parentID = parentIDlist[-1:][0]
            if not parentID in childIDs:
                childIDs[parentID] = []
            childIDs[parentID].append(core_id)

    for core_id, record in coreDict.items():
         if core_id in childIDs:
            coreDict[core_id]['children'] = childIDs[core_id]

    targetRefDict = {}   # parent-child
    childRefDict = {}
    for core_id, record in coreDict.items():
        if 'children' in record:
            children = record['children']
            for child_id in children:
                child = coreDict[child_id]
                if not child:
                    continue
                referenceDict[child_id] = core_id          
                if child['card']:
                    if 'n' == child['card'][-1]:
                        targetRefDict[child_id] = child['parent']
                        if DEBUG: print(f'=2= {child_id} targetRef {child["parent"]}')
                    else:
                        associationDict[child_id] = child['parent']
                        if DEBUG: print(f'=3= {child_id} associationDict {child["parent"]}')

    # targetRefDict = {}   # parent-child
    childRefDict = {}
    for core_id, record in coreDict.items():
        term = record['term']
        if 'parent' in record and len(record['parent']) > 0:
            parent_id = record['parent'][-1]
            targetRefDict[core_id] = parent_id
            if not parent_id in childRefDict:
                 childRefDict[parent_id] = {'term':term, 'source':[]}
            childRefDict[parent_id]['source'].append(core_id)

    repeatables = {}
    for core_id, record in coreDict.items():
        card = record['card']
        if 'JBG'==core_id[:3] and 'n'==card[-1:] and 'children' in record:
            repeatables[core_id] = {}
            repeatables[core_id]['source'] = record['children']

    if DEBUG:
        print(repeatables)

    roleMap = {}

    for id,record in coreDict.items():
        term = record['term']
        if 'JBG'==id[:3]:
            link_id = id
            role_id = f'link_{link_id}'
            URI = f'/{role_id}'
            roleMap[link_id] = {'core_id':link_id,'link_id':link_id,'URI':URI,'role_id':role_id,'term':term}

    for core_id,parent_id in targetRefDict.items():
        link_id = f'{parent_id}_{core_id}'
        if link_id not in roleMap:
            core_term = getTerm(core_id)
            parent_term = getTerm(parent_id)
            term = f'{parent_term}_{core_term}'
            role_id = f'link_{link_id}'
            URI = f'/{role_id}'
            roleMap[link_id] = {'core_id':core_id,'link_id':link_id,'URI':URI,'role_id':role_id,'term':term}

    ###################################
    # core.xsd
    #
    def get_element_datatype(type):
        if type in datatypeMap:
            datatype = datatypeMap[type]['xbrli']
            datatype = f'xbrli:{datatype}'
        else:
            datatype = 'xbrli:stringItemType'
        return datatype

    def defineElement(core_id,record):
        global lines
        global elementsDefined
        if not core_id in elementsDefined:
            elementsDefined.add(core_id)
            if not record:
                print(f'NOT DEFINED {core_id} record')
                return
            kind = core_id[:3]
            type =  record['datatype']
            if 'JBG'==kind:
                line = f'        <element name="{core_id}" id="{core_id}" abstract="true" type="xbrli:stringItemType" nillable="true" substitutionGroup="xbrli:item" xbrli:periodType="instant"/>\n'
            else:
                type = get_element_datatype(type)
                line = f'        <element name="{core_id}" id="{core_id}" type="{type}" nillable="false" substitutionGroup="xbrli:item" xbrli:periodType="instant"/>\n'
            lines.append(line) 

    html_head = [
        '<?xml version="1.0" encoding="UTF-8"?>\n',
        '<!-- (c) 2022 XBRL Japan  inc. -->\n',
        '<schema \n',
        '    targetNamespace="http://www.xbrl.jp/core-japan" \n',
        '    elementFormDefault="qualified" \n',
        '    xmlns="http://www.w3.org/2001/XMLSchema" \n',
        '    xmlns:adc="http://www.xbrl.jp/core-japan" \n',
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
        f'            <link:roleType id="audit-data-collection-role" roleURI="http://www.xbrl.jp/core-japan/role">\n',
        f'                <link:definition>link audit-data-collection</link:definition>\n',
        f'                <link:usedOn>link:definitionLink</link:usedOn>\n',
        f'                <link:usedOn>link:presentationLink</link:usedOn>\n',
        '            </link:roleType>\n',
    ]
    for core_id,role in roleMap.items():
        role_id = role["role_id"]
        URI = role['URI']
        link_id = role['link_id']
        term = role["term"]
        if '_' in term:
            parent_term = term[:term.index('_')]
            core_term = term[term.index('_')+1:]
            html.append(f'            <link:roleType id="{role_id}" roleURI="http://www.xbrl.jp/core-japan/role{URI}">\n')
            html.append(f'                <link:definition>{parent_term} to {core_term}</link:definition>\n')
            html.append(f'                <link:usedOn>link:definitionLink</link:usedOn>\n')
            html.append('            </link:roleType>\n')
        else:
            html.append(f'            <link:roleType id="{role_id}" roleURI="http://www.xbrl.jp/core-japan/role{URI}">\n')
            html.append(f'                <link:definition>{term}</link:definition>\n')
            html.append(f'                <link:usedOn>link:definitionLink</link:usedOn>\n')
            html.append('            </link:roleType>\n')
    lines += html

    html = [
        '            <!--\n',
        '                description: roleType arcroleType\n',
        '            -->\n'
        '            <link:roleType id="description" roleURI="http://www.xbrl.jp/core-japan/role/description">\n',
        '                <link:definition>description</link:definition>\n',
        '                <link:usedOn>link:label</link:usedOn>\n',
        '            </link:roleType>\n',
        '            <link:arcroleType id="concept-description" cyclesAllowed="undirected" arcroleURI="http://www.xbrl.jp/core-japan/arcrole/concept-description">\n',
        '                <link:definition>concept to description</link:definition>\n',
        '                <link:usedOn>link:labelArc</link:usedOn>\n',
        '            </link:arcroleType >\n',
    ]
    lines += html

    html = [
        '            <!--\n',
        '                primary key: roleType arcroleType\n',
        '            -->\n'
        '            <link:roleType id="primary-key" roleURI="http://www.xbrl.jp/core-japan/role/primary-key">\n',
        '                <link:definition>primary key</link:definition>\n',
        '                <link:usedOn>link:definitionLink</link:usedOn>\n',
        '            </link:roleType>\n',
        '            <link:arcroleType id="concept-primary-key" cyclesAllowed="undirected" arcroleURI="http://www.xbrl.jp/core-japan/arcrole/concept-primary-key">\n',
        '                <link:definition>concept primary key</link:definition>\n',
        '                <link:usedOn>link:definitionArc</link:usedOn>\n',
        '            </link:arcroleType >\n',
    ]
    lines += html

    html = [
        '            <!--\n',
        '                reference itermtifier: roleType arcroleType\n',
        '            -->\n'
        '            <link:roleType id="reference-itermtifier" roleURI="http://www.xbrl.jp/core-japan/role/reference-itermtifier">\n',
        '                <link:definition>reference itermtifier</link:definition>\n',
        '                <link:usedOn>link:definitionLink</link:usedOn>\n',
        '            </link:roleType>\n',
        '            <link:arcroleType id="concept-reference-itermtifier" cyclesAllowed="undirected" arcroleURI="http://www.xbrl.jp/core-japan/arcrole/concept-reference-itermtifier">\n',
        '                <link:definition>concept reference itermtifier</link:definition>\n',
        '                <link:usedOn>link:definitionArc</link:usedOn>\n',
        '            </link:arcroleType >\n',
    ]
    lines += html

    html = [
        '            <!--\n',
        '                require: roleType\n',
        '            -->\n'
        '            <link:roleType id="require" roleURI="http://www.xbrl.jp/core-japan/role/require">\n',
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
    for core_id,role in roleMap.items():
        link_id = role['link_id']
        html_hypercube.append(f'    <element name="h_{link_id}" id="h_{link_id}" substitutionGroup="xbrldt:hypercubeItem" type="xbrli:stringItemType" nillable="true" abstract="true" xbrli:periodType="instant"/>\n')
    lines += html_hypercube

    html_dimension = [
        '    <!-- Dimension -->\n'
    ]
    # Dimension
    for core_id,role in roleMap.items():
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
    for record in coreDict.values():
        core_id = record['id']
        # kind = core_id[:3] #record['kind']
        # referenced_id = None
        if core_id:
            defineElement(core_id,record)

    for core_id,parent_id in targetRefDict.items():
        referenced_id = f'{parent_id}_{core_id}'
        parent = coreDict[parent_id]
        defineElement(referenced_id,parent)
        
    lines.append('</schema>')

    core_japan_xsd_file = file_path(f'{xbrl_base}/{core_xsd}')
    with open(core_japan_xsd_file, 'w', encoding='utf_8', newline='') as f:
        f.writelines(lines)
    if VERBOSE:
        print(f'-- {core_japan_xsd_file}')

    ###################################
    # labelLink en
    #
    def linkLabel(core_id,name,Desc):
        global locsDefined
        global definedLabels
        global arcsDefined
        global definedDescs
        global definedDescArcs
        if not core_id:
            return
        lines.append(f'        <!-- {core_id} {name} -->\n')
        if not core_id in locsDefined:
            locsDefined[core_id] = core_id
            line = f'        <link:loc xlink:type="locator" xlink:href="{core_xsd}#{core_id}" xlink:label="{core_id}" xlink:title="{core_id}"/>\n'
        else:
            line = f'            <!-- link:loc defined -->\n'
        lines.append(line)
        # name
        if not core_id in definedLabels:
            definedLabels[core_id] = core_id
            line = f'        <link:label xlink:type="resource" xlink:label="label_{core_id}" xlink:title="label_{core_id}" id="label_{core_id}" xml:lang="en" xlink:role="http://www.xbrl.org/2003/role/label">{name}</link:label>\n'
        else:
            line = f'            <!-- link:label http://www.xbrl.org/2003/role/label defined -->\n'
        lines.append(line)
        if not core_id in arcsDefined:
            arcsDefined[core_id] = core_id
            line = f'        <link:labelArc xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label" xlink:from="{core_id}" xlink:to="label_{core_id}" xlink:title="label: {core_id} to label_{core_id}"/>\n'
        else:
            line = f'            <!-- link:labelArc http://www.xbrl.org/2003/arcrole/concept-label defined -->\n'
        lines.append(line)
        # Desc
        if name != Desc:
            if not core_id in definedDescs:
                definedDescs[core_id] = core_id
                line = f'        <link:label xlink:type="resource" xlink:label="description_{core_id}" xlink:title="description_{core_id}" id="description_{core_id}" xml:lang="en" xlink:role="http://www.xbrl.jp/core-japan/role/description">{Desc}</link:label>\n'
            else:
                line = f'            <!-- link:label http://www.xbrl.jp/core-japan/role/description defined -->\n'
            lines.append(line)
            if not core_id in definedDescArcs:
                definedDescArcs[core_id] = core_id
                line = f'        <link:labelArc xlink:type="arc" xlink:arcrole="http://www.xbrl.jp/core-japan/arcrole/concept-description" xlink:from="{core_id}" xlink:to="description_{core_id}" xlink:title="label: {core_id} to label_{core_id}"/>\n'
            else:
                line = f'            <!-- link:labelArc http://www.xbrl.jp/core-japan/arcrole/concept-description defined -->\n'
            lines.append(line)

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>\n',
        '<!--  (c) 2022 XBRL Japan inc. -->\n',
        '<link:linkbase\n',
        '    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n',
        '    xmlns:link="http://www.xbrl.org/2003/linkbase"\n',
        '    xmlns:xlink="http://www.w3.org/1999/xlink"\n',
        '    xsi:schemaLocation="http://www.xbrl.org/2003/linkbase http://www.xbrl.org/2003/xbrl-linkbase-2003-12-31.xsd">\n',
        f'    <link:roleRef roleURI="http://www.xbrl.jp/core-japan/role/description" xlink:type="simple" xlink:href="{core_xsd}#description"/>\n',
        f'    <link:arcroleRef arcroleURI="http://www.xbrl.jp/core-japan/arcrole/concept-description" xlink:type="simple" xlink:href="{core_xsd}#concept-description"/>\n',
        '    <link:labelLink xlink:type="extended" xlink:role="http://www.xbrl.org/2003/role/link">\n'
    ]
    locsDefined = {}
    arcsDefined = {}
    definedLabels = {}
    definedDescs = {}
    definedDescArcs = {}
    for record in coreDict.values():
        core_id = record['id']
        kind = core_id[:3]
        term = record['term']
        Desc = record['desc']
        linkLabel(core_id,term,Desc)

    for core_id,referenced_id in targetRefDict.items():
        record = coreDict[referenced_id]
        term = record['term']
        Desc = record['desc']
        linkLabel(core_id,term,Desc)

    lines.append('    </link:labelLink>\n')
    lines.append('</link:linkbase>\n')

    core_japan_label_file = file_path(f'{xbrl_base}/{core_label}-en.xml')
    with open(core_japan_label_file, 'w', encoding='utf_8', newline='') as f:
        f.writelines(lines)
    if VERBOSE:
        print(f'-- {core_japan_label_file}')

    ###################################
    #   presentationLink
    #
    locsDefined = {}
    arcsDefined = {}
    def linkPresentation(core_id,children,n):
        global lines
        global count
        global locsDefined
        global arcsDefined
        if not core_id: 
            return
        record = coreDict[core_id]
        if not record:
            return
        term = record['term']
        if not core_id in locsDefined:
            locsDefined[core_id] = term
            lines.append(f'        <!-- {kind} {core_id} {term} -->\n')
            lines.append(f'        <link:loc xlink:type="locator" xlink:href="{core_xsd}#{core_id}" xlink:label="{core_id}" xlink:title="presentation: {core_id} {term}"/>\n')
        for child_id in children:
            child = coreDict[child_id]
            child_term = child['term']
            level = child['level']
            if level != n:
                continue
            if child_id in targetRefDict:
                target_id = child_id
                if not target_id in locsDefined:
                    locsDefined[target_id] = child_term
                    lines.append(f'        <link:loc xlink:type="locator" xlink:href="{core_xsd}#{target_id}" xlink:label="{target_id}" xlink:title="presentation parent: {target_id} {child_term}"/>\n')
                arc_id = F'{core_id} {target_id}'
                if not arc_id in arcsDefined and core_id!=target_id:
                    arcsDefined[arc_id] = f'{term} to {child_term}'
                    count += 1
                    lines.append(f'        <link:presentationArc xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child" xlink:from="{core_id}" xlink:to="{target_id}" order="{count}" xlink:title="presentation: {core_id} {term} to {target_id} {child_term}"/>\n')
                    if 'children' in child and len(child['children']) > 0:
                        grand_children = child['children']
                        # grand_children = [c for c in grand_children if c not in childDefined]
                        linkPresentation(target_id,grand_children,n+1)
            else:
                if not child_id in locsDefined:
                    locsDefined[child_id] = child_term
                    lines.append(f'        <link:loc xlink:type="locator" xlink:href="{core_xsd}#{child_id}" xlink:label="{child_id}" xlink:title="presentation parent: {child_id} {child_term}"/>\n')
                arc_id = F'{core_id} {child_id}'
                if not arc_id in arcsDefined and core_id!=child_id:
                    arcsDefined[arc_id] = f'{term} to {child_term}'
                    count += 1
                    lines.append(f'        <link:presentationArc xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child" xlink:from="{core_id}" xlink:to="{child_id}" order="{count}" xlink:title="presentation: {core_id} {term} to {child_id} {child_term}"/>\n')
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
        f'    <link:roleRef roleURI="http://www.xbrl.jp/core-japan/role" xlink:type="simple" xlink:href="{core_xsd}#audit-data-collection-role"/>\n',
        '    <link:presentationLink xlink:type="extended" xlink:role="http://www.xbrl.jp/core-japan/role">\n',
    ]
    locsDefined = {}
    arcsDefined = {}
    # for record in [x for x in records if 'ABIE'==x['kind']]:
    record = [x for x in records if 'JBG'==x['id'][:3]][0]
    core_id = record['id']
    # kind = record['id'][:3]
    count = 0
    children = record['children']
    linkPresentation(core_id,children,2)
       
    lines.append('    </link:presentationLink>\n')
    lines.append('</link:linkbase>\n')

    core_japan_presentationl_file = file_path(f'{xbrl_base}/{core_presentation}.xml')
    with open(core_japan_presentationl_file, 'w', encoding='utf_8', newline='') as f:
        f.writelines(lines)
    if VERBOSE:
        print(f'-- {core_japan_presentationl_file}')

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
        lines.append(f'    <link:roleRef roleURI="http://www.xbrl.jp/core-japan/role{URI}" xlink:type="simple" xlink:href="{core_xsd}#{role_id}"/>\n')
    html = [
        f'    <link:roleRef roleURI="http://www.xbrl.jp/core-japan/role/primary-key" xlink:type="simple" xlink:href="{core_xsd}#primary-key"/>\n',
        f'    <link:roleRef roleURI="http://www.xbrl.jp/core-japan/role/reference-itermtifier" xlink:type="simple" xlink:href="{core_xsd}#reference-itermtifier"/>\n',
        f'    <link:roleRef roleURI="http://www.xbrl.jp/core-japan/role/require" xlink:type="simple" xlink:href="{core_xsd}#require"/>\n',
        '    <!-- arcroleRef -->\n',
        '    <link:arcroleRef arcroleURI="http://xbrl.org/int/dim/arcrole/all" xlink:type="simple" xlink:href="http://www.xbrl.org/2005/xbrldt-2005.xsd#all"/>\n',
        '    <link:arcroleRef arcroleURI="http://xbrl.org/int/dim/arcrole/domain-member" xlink:type="simple" xlink:href="http://www.xbrl.org/2005/xbrldt-2005.xsd#domain-member"/>\n',
        '    <link:arcroleRef arcroleURI="http://xbrl.org/int/dim/arcrole/hypercube-dimension" xlink:type="simple" xlink:href="http://www.xbrl.org/2005/xbrldt-2005.xsd#hypercube-dimension"/>\n',
        '    <link:arcroleRef arcroleURI="http://xbrl.org/int/dim/arcrole/dimension-domain" xlink:type="simple" xlink:href="http://www.xbrl.org/2005/xbrldt-2005.xsd#dimension-domain"/>\n',
        f'    <link:arcroleRef arcroleURI="http://www.xbrl.jp/core-japan/arcrole/concept-primary-key" xlink:type="simple" xlink:href="{core_xsd}#concept-primary-key"/>\n',
        f'    <link:arcroleRef arcroleURI="http://www.xbrl.jp/core-japan/arcrole/concept-reference-itermtifier" xlink:type="simple" xlink:href="{core_xsd}#concept-reference-itermtifier"/>\n',
    ]
    lines += html

    for core_id,role in roleMap.items():
        if 'J'==core_id[:1]:
            defineHypercube(core_id, role, 2)

    lines.append('</link:linkbase>\n')

    core_japan_definitionl_file = file_path(f'{xbrl_base}/{core_definition}.xml')
    with open(core_japan_definitionl_file, 'w', encoding='utf_8', newline='') as f:
        f.writelines(lines)
    if VERBOSE:
        print(f'-- {core_japan_definitionl_file}')

    print('** END **')