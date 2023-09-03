#!/usr/bin/env python3
# coding: utf-8
#
# generate CSV fron UN/CEFACT ABIE schema file
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
import json
import argparse
import os
from lxml import etree

UNIDs = sorted(
    [
        'UN01005479',
        'UN01005861',
        'UN01005936',
        'UN01005471',
        'UN01005557',
        'UN01005579',
        'UN01006014',
        'UN01005878',
        'UN01005909',
        'UN01005988',
        'UN01005475',
        'UN01005756',
        'UN01000371',
        'UN01005738',
        'UN01005670',
        'UN01005832',
        'UN01005608',
        'UN01005779',
        'UN01005941',
        'UN01005487',
        'UN01015590',
        'UN01005953',
        'UN01005958',
        'UN01005968',
        'UN01005994',
        'UN01009647',
        'UN01005718',
        'UN01005687',
        'UN01005857',
        'UN01005398',
        'UN01005402',
        'UN01004493',
        'UN01005626',
        'UN01005706',
        'UN01006006',
        'UN01005680',
        'UN01009653',
        'UN01009659',
        'UN01009664',
        'UN01005809',
        'UN01003138',
        'UN01005790',
        'UN01005573',
        'UN01005567',
        'UN01005735'
    ]
)
DEBUG = False
VERBOSE = True
SEP = os.sep

xsd_file = "data/SME_Common/15JUL23XMLSchemas-D23A/uncefact/data/standard/ReusableAggregateBusinessInformationEntity_33p0.xsd"
json_path = 'data/BIE/ABIE.json'

def file_path(pathname):
    if SEP == pathname[0:1]:
        return pathname
    else:
        dir = os.path.dirname(__file__)
        new_path = os.path.join(dir, pathname)
        return new_path


def extract_complex_type_data(xsd_content):
    # tree = etree.fromstring(xsd_content)
    tree = etree.parse(xsd_path)

    namespace = {
        'xsd': 'http://www.w3.org/2001/XMLSchema',
        'ccts': 'urn:un:unece:uncefact:documentation:standard:CoreComponentsTechnicalSpecification:2'  # この名前空間URIを正確なものに置き換えてください
    }

    complex_types = tree.xpath('//xsd:complexType', namespaces=namespace)
    result = {}

    for ctype in complex_types:
        name = ctype.get("name")
        annotation = ctype.find('xsd:annotation/xsd:documentation', namespaces=namespace)

        # ComplexTypeの主要な情報を取得
        den      = annotation.find('ccts:DictionaryEntryName', namespaces=namespace).text
        unid     = annotation.find('ccts:UniqueID', namespaces=namespace).text
        key_name = f"{unid} {den} {name}"
        if unid not in UNIDs:
            continue

        result[key_name] = []
        elements = ctype.xpath('.//xsd:element', namespaces=namespace)

        # 各子要素の情報を取得
        for elem in elements:
            elem_annotation = elem.find('xsd:annotation/xsd:documentation', namespaces=namespace)
            kind = elem_annotation.find('ccts:Acronym', namespaces=namespace).text
            unid = elem_annotation.find('ccts:UniqueID', namespaces=namespace).text
            den  = elem_annotation.find('ccts:DictionaryEntryName', namespaces=namespace).text
            name = elem.get("name")
            type = elem.get("type")
            minOccurs = elem.get("minOccurs")
            maxOccurs = elem.get("maxOccurs")
            card = elem_annotation.find('ccts:Cardinality', namespaces=namespace).text
            elem_info = {
                "kind": kind,
                "UNID": unid,
                "DEN": den,
                "card": card,
                "name": name,
                "type": type,
                "minOccurs": minOccurs,
                "maxOccurs": maxOccurs
            }
            result[key_name].append(elem_info)

    return result

# JSON ファイルとして書き出し
def write_to_json(data, file_path):
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

# if __name__ == "__main__":
    xsd_path = xsd_file
    complex_types_data = extract_complex_type_data(xsd_path)
    write_to_json(complex_types_data, json_path)
    csv_path = "output.csv"

    print('-- END --')
