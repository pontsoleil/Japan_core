import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import argparse
from collections import defaultdict,OrderedDict
import re
import json
import os

namespace_mappings = {
    'xbrli': 'http://www.xbrl.org/2001/instance',
    'link': 'http://www.xbrl.org/2001/XLink/xbrllinkbase',
    'ISO4217': 'http://www.xbrl.org/2003/iso4217',
    'gl-bus': 'http://www.xbrl.org/int/gl/bus/2006-10-25',
    'gl-cor': 'http://www.xbrl.org/int/gl/cor/2006-10-25',
    'gl-muc': 'http://www.xbrl.org/int/gl/muc/2006-10-25',
    'gl-usk': 'http://www.xbrl.org/taxonomy/int/gl/usk/2003-08-29/',
    'gl-plt': 'http://www.xbrl.org/int/gl/plt/2006-10-25',
    'tdb': 'www.tdb.co.jp',
    'xhtml': 'http://www.w3.org/1999/xhtml',
    'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
}

namespace1_mappings = {
    'xbrli': 'http://www.xbrl.org/2001/instance',
    'xbrll': 'http://www.xbrl.org/2003/linkbase',
    'link': 'http://www.xbrl.org/2001/XLink/xbrllinkbase',
    'xlink': 'http://www.w3.org/1999/xlink',
    'iso4217': 'http://www.xbrl.org/2003/iso4217',
    'iso639': 'http://www.xbrl.org/2005/iso639',
    'gl-gen': 'http://www.xbrl.org/taxonomy/int/gl/gen/2003-08-29/',
    'gl-cor': 'http://www.xbrl.org/taxonomy/int/gl/cor/2003-08-29/',
    'gl-bus': 'http://www.xbrl.org/taxonomy/int/gl/bus/2003-08-29/',
    'gl-muc': 'http://www.xbrl.org/taxonomy/int/gl/muc/2003-08-29/',
    'gl-usk': 'http://www.xbrl.org/taxonomy/int/gl/usk/2003-08-29/',
    'gl-taf': 'http://www.xbrl.org/taxonomy/int/gl/taf/2003-08-29/',
    'gl-plt': 'http://www.xbrl.org/taxonomy/int/gl/plt/2003-08-29/',
    'xhtml': 'http://www.w3.org/1999/xhtml',
    'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
}

namespace2_mappings = {
    'xbrli': 'http://www.xbrl.org/2003/instance',
    'xbrll': 'http://www.xbrl.org/2003/linkbase',
    'link': 'http://www.xbrl.org/2001/XLink/xbrllinkbase',
    'xlink': 'http://www.w3.org/1999/xlink',
    'iso4217': 'http://www.xbrl.org/2003/iso4217',
    'iso639': 'http://www.xbrl.org/2005/iso639',
    'gl-gen': 'http://www.xbrl.org/int/gl/gen/2015-03-25',
    'gl-cor': 'http://www.xbrl.org/int/gl/cor/2015-03-25',
    'gl-bus': 'http://www.xbrl.org/int/gl/bus/2015-03-25',
    'gl-muc': 'http://www.xbrl.org/int/gl/muc/2015-03-25',
    'gl-usk': 'http://www.xbrl.org/int/gl/usk/2015-03-25',
    'gl-taf': 'http://www.xbrl.org/int/gl/taf/2015-03-25',
    'gl-srcd': 'http://www.xbrl.org/int/gl/srcd/2015-03-25',
    'gl-ehm': 'http://www.xbrl.org/int/gl/ehm/2015-03-25',
    'gl-plt': 'http://www.xbrl.org/int/gl/plt/2015-03-25',
    'xhtml': 'http://www.w3.org/1999/xhtml',
    'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
}

# namespace3_mappings = {
#     'xbrli': 'http://www.xbrl.org/2001/instance',
#     'xbrll': 'http://www.xbrl.org/2003/linkbase',
#     'link': 'http://www.xbrl.org/2001/XLink/xbrllinkbase',
#     'xlink': 'http://www.w3.org/1999/xlink',
#     'iso4217': 'http://www.xbrl.org/2003/iso4217',
#     'iso639': 'http://www.xbrl.org/2005/iso639',
#     'gl-gen': 'http://www.xbrl.org/int/gl/gen/2016-12-01',
#     'gl-cor': 'http://www.xbrl.org/int/gl/cor/2016-12-01',
#     'gl-bus': 'http://www.xbrl.org/int/gl/bus/2016-12-01',
#     'gl-muc': 'http://www.xbrl.org/int/gl/muc/2016-12-01',
#     'gl-usk': 'http://www.xbrl.org/int/gl/usk/2016-12-01',
#     'gl-taf': 'http://www.xbrl.org/int/gl/taf/2016-12-01',
#     'gl-srcd': 'http://www.xbrl.org/int/gl/srcd/2016-12-01',
#     'gl-ehm': 'http://www.xbrl.org/int/gl/ehm/2016-12-01',
#     'gl-plt': 'http://www.xbrl.org/int/gl/plt/2016-12-01',
#     'xhtml': 'http://www.w3.org/1999/xhtml',
#     'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
# }

def prettify(elem, level=0):
    indent = "    "  # Four spaces for each level of indentation
    newline = "\n"

    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = newline + indent * (level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = newline + indent * level
        for i, subelem in enumerate(elem):
            prettify(subelem, level + 1)
            if i == len(elem) - 1:
                subelem.tail = newline + indent * level
            else:
                subelem.tail = newline + indent * (level + 1)
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = newline + indent * level

def modify_dict_element_order0(dictionary, target_key, new_index):
    if target_key not in dictionary:
        return dictionary
    keys = list(dictionary.keys())
    values = list(dictionary.values())
    target_index = keys.index(target_key)
    if target_index == new_index:
        return dictionary
    keys.insert(new_index, keys.pop(target_index))
    values.insert(new_index, values.pop(target_index))
    return OrderedDict(zip(keys, values))

def insert_dict_element(dictionary, target_key, target_value, index):
    keys = list(dictionary.keys())
    values = list(dictionary.values())
    keys.insert(index, target_key)
    values.insert(index, target_value)
    return OrderedDict(zip(keys, values))

def modify_dict_element_order(dictionary, target_key, new_index):
    if target_key not in dictionary:
        return dictionary
    keys = list(dictionary.keys())
    values = list(dictionary.values())
    target_index = keys.index(target_key)
    if target_index == new_index:
        return dictionary
    keys.insert(new_index, keys.pop(target_index))
    values.insert(new_index, values.pop(target_index))
    return OrderedDict(zip(keys, values))

def modify_xml_files_in_directory(in_directory, out_directory):
    # Get a list of XML files in the directory
    xml_files = [file for file in os.listdir(in_directory) if file.endswith('.xml')]

    # Process each XML file
    for xml_file in xml_files:
        # Construct the input and output file paths
        input_file = os.path.join(in_directory, xml_file)
        output_file = os.path.join(out_directory, xml_file)

        # Modify XML namespaces
        modify_xml_namespaces(input_file, output_file)

def modify_xml_namespaces(xml_file, output_file):
    # parse XML document
    tree = ET.parse(xml_file)
    root = tree.getroot()
    # Modify the xsi:schemaLocation attribute value
    root.set("{http://www.w3.org/2001/XMLSchema-instance}schemaLocation", "http://www.xbrl.org/int/gl/plt/2015-03-25 ../plt/case-c-b-m-u-t-s/gl-plt-all-2015-03-25.xsd")

    # Convert XML to dictionary
    xml_dict = etree_to_dict(root)

    # Modify namespace definitions and element names
    xml_dict['{'+namespace_mappings['xbrli']+'}xbrl'] = xml_dict.pop('{'+namespace_mappings['xbrli']+'}group')
    xml_dict['{'+namespace_mappings['xbrli']+'}xbrl']['@xmlns:xbrli']   = namespace2_mappings['xbrli']
    xml_dict['{'+namespace_mappings['xbrli']+'}xbrl']['@xmlns:xbrll']   = namespace2_mappings['xbrll']
    xml_dict['{'+namespace_mappings['xbrli']+'}xbrl']['@xmlns:xlink']   = namespace2_mappings['xlink']
    xml_dict['{'+namespace_mappings['xbrli']+'}xbrl']['@xmlns:iso4217'] = namespace2_mappings['iso4217']
    xml_dict['{'+namespace_mappings['xbrli']+'}xbrl']['@xmlns:iso639']  = namespace2_mappings['iso639']
    xml_dict['{'+namespace_mappings['xbrli']+'}xbrl']['@xmlns:gl-cor']  = namespace2_mappings['gl-cor']
    xml_dict['{'+namespace_mappings['xbrli']+'}xbrl']['@xmlns:gl-muc']  = namespace2_mappings['gl-muc']
    xml_dict['{'+namespace_mappings['xbrli']+'}xbrl']['@xmlns:gl-bus']  = namespace2_mappings['gl-bus']
    xml_dict['{'+namespace_mappings['xbrli']+'}xbrl']['@xmlns:gl-usk']  = namespace2_mappings['gl-usk']
    xml_dict['{'+namespace_mappings['xbrli']+'}xbrl']['@xmlns:gl-taf']  = namespace2_mappings['gl-taf']
    xml_dict['{'+namespace_mappings['xbrli']+'}xbrl']['@xmlns:gl-srcd'] = namespace2_mappings['gl-srcd']
    xml_dict['{'+namespace_mappings['xbrli']+'}xbrl']['@xmlns:gl-plt']  = namespace2_mappings['gl-plt']

    txtJson = json.dumps(xml_dict)

    txtJson = re.sub('{'+namespace1_mappings['xbrli']+'}',  'xbrli:',  txtJson)
    txtJson = re.sub('{'+namespace1_mappings['gl-cor']+'}', 'gl-cor:', txtJson)
    txtJson = re.sub('{'+namespace1_mappings['gl-muc']+'}', 'gl-muc:', txtJson)
    txtJson = re.sub('{'+namespace1_mappings['gl-bus']+'}', 'gl-bus:', txtJson)
    txtJson = re.sub('{'+namespace1_mappings['gl-usk']+'}', 'gl-usk:', txtJson)
    txtJson = re.sub('{'+namespace1_mappings['gl-taf']+'}', 'gl-taf:', txtJson)
    txtJson = re.sub('{'+namespace1_mappings['gl-gen']+'}', 'gl-gen:', txtJson)
    txtJson = re.sub('{'+namespace1_mappings['gl-plt']+'}', 'gl-plt:', txtJson)
    txtJson = re.sub('xbrli:nonNumericContext','xbrli:context',txtJson)
    txtJson = re.sub('xbrli:numericContext','xbrli:context',txtJson)
    txtJson = re.sub('cwa="false" precision="11"','',txtJson)
    txtJson = re.sub('nonNumericContext','contextRef',txtJson)
    txtJson = re.sub('numericContext','contextRef',txtJson)
    txtJson = re.sub('ISO693','iso639',txtJson)
    txtJson = re.sub('ISO4217','iso4217',txtJson)
    txtJson = re.sub('"@contextRef": "c1",','"@contextRef": "s1", "@unitRef": "JPY", "@decimals": "0",',txtJson)

    txtJson = re.sub('gl-cor:xbrlElement', 'gl-cor:summaryReportingElement', txtJson)
    txtJson = re.sub('gl-cor:xbrlTaxonomy', 'gl-srcd:summaryReportingTaxonomyIDRef', txtJson)

    # Convert the modified JSON back to XML
    xml_dict2 = json.loads(txtJson)

    del xml_dict2['xbrli:xbrl']['xbrli:context']

    # xbrll:schemaRefを先頭に追加
	# <xbrll:schemaRef xlink:type="simple" xlink:arcrole="http://www.w3.org/1999/xlink/properties/linkbase" xlink:href="../plt/case-c-b-m-u-t/gl-plt-all-2015-03-25.xsd"/>
    xml_dict2['xbrli:xbrl'] = insert_dict_element(
        xml_dict2['xbrli:xbrl'],
        'xbrll:schemaRef',
        {
            '@xlink:type':'simple',
            '@xlink:arcrole':'http://www.w3.org/1999/xlink/properties/linkbase',
            '@xlink:href':'../plt/case-c-b-m-u-t-s/gl-plt-all-2015-03-25.xsd'
        },
        0  # 0は先頭を指定
    )

    # xbrli:contextを２番目の要素に追加
	# <!-- Contexts, mandatory according to the XBRL 2.1, Specification, are not meant to describe the information in XBRL GL and appear only by convention. All facts are instant and developers are encouraged to duplicate/provide the date the XBRL GL information is created as the period's date. -->
	# <xbrli:context id="now">
	# 	<xbrli:entity>
	# 		<xbrli:identifier scheme="http://www.xbrl.org/xbrlgl/sample">SAMPLE</xbrli:identifier>
	# 	</xbrli:entity>
	# 	<!-- The XBRL GL WG recommends using the file creation data as the period. -->
	# 	<xbrli:period>
	# 		<xbrli:instant>2004-10-03</xbrli:instant>
	# 	</xbrli:period>
	# </xbrli:context>
    xml_dict2['xbrli:xbrl'] = insert_dict_element(
        xml_dict2['xbrli:xbrl'],
        'xbrli:context',
        {
            '@id':'s1',
            'xbrli:entity': {
                'xbrli:identifier': {
                    '@scheme':'http://www.xbrl.org/xbrlgl/sample',
                    '#text':'SAMPLE'
                }
            },
            'xbrli:period': {
                'xbrli:instant':{'#text':'2004-10-03'}
            }
        },
        1  # 1は２番目を指定
    )

    # xbrli:unit　JPYを３番目の要素に追加
	# <!-- Units of measure in XBRL GL are handled within the measurable or multicurrency elements. Units are provided by convention and should not be relied upon in interpreting XBRL GL data. -->
	# <xbrli:unit id="JPY">
	# 	<xbrli:measure>iso4217:JPY</xbrli:measure>
	# </xbrli:unit>
	# <xbrli:unit id="NotUsed">
	# 	<xbrli:measure>pure</xbrli:measure>
	# </xbrli:unit>
    xml_dict2['xbrli:xbrl'] = insert_dict_element(
        xml_dict2['xbrli:xbrl'],
        'xbrli:unit',
        [
            {
                'xbrli:measure': {'#text':'iso4217:JPY'},
                '@id':'JPY'
            },
            {
                'xbrli:measure': {'#text':'pure'},                        
                '@id':'NotUsed'
            }
        ],
        2  # 2は３番目を指定
    )

    # 'gl-bus:sourceApplication'を後ろに移動
    last = len(xml_dict2['xbrli:xbrl']['gl-cor:accountingEntries']['gl-cor:documentInfo'])
    xml_dict2['xbrli:xbrl']['gl-cor:accountingEntries']['gl-cor:documentInfo'] = modify_dict_element_order(
        xml_dict2['xbrli:xbrl']['gl-cor:accountingEntries']['gl-cor:documentInfo'],
        'gl-bus:sourceApplication',
        last  # lastは最後の要素の後ろを指定
    )
    # 'gl-bus:organizationIdentifiers'を前に移動
    xml_dict2['xbrli:xbrl']['gl-cor:accountingEntries']['gl-cor:entityInformation'] = modify_dict_element_order(
        xml_dict2['xbrli:xbrl']['gl-cor:accountingEntries']['gl-cor:entityInformation'],
        'gl-bus:organizationIdentifiers',
        -1  # -1は最後の要素の前を指定
    )

    keys = list(xml_dict2['xbrli:xbrl']['gl-cor:accountingEntries']['gl-cor:entryHeader'].keys())
    index0 = keys.index('gl-cor:entryType')
    index1 = keys.index('gl-cor:entryNumber')
    if index0 > index1:
        index = index1
    else:
        index = index1 - 1
    xml_dict2['xbrli:xbrl']['gl-cor:accountingEntries']['gl-cor:entryHeader'] = modify_dict_element_order(
        xml_dict2['xbrli:xbrl']['gl-cor:accountingEntries']['gl-cor:entryHeader'],
        'gl-cor:entryType',
        index  # indexはgl-bus:entryOriginの前を指定
    )    
    keys = list(xml_dict2['xbrli:xbrl']['gl-cor:accountingEntries']['gl-cor:entryHeader'].keys())
    index0 = keys.index('gl-bus:entryOrigin')
    index1 = keys.index('gl-cor:entryNumber')
    if index0 > index1:
        index = index1
    else:
        index = index1 - 1
    xml_dict2['xbrli:xbrl']['gl-cor:accountingEntries']['gl-cor:entryHeader'] = modify_dict_element_order(
        xml_dict2['xbrli:xbrl']['gl-cor:accountingEntries']['gl-cor:entryHeader'],
        'gl-bus:entryOrigin',
        index  # indexはgl-cor:entryNumberの前を指定
    )

    detail_count = len(xml_dict2['xbrli:xbrl']['gl-cor:accountingEntries']['gl-cor:entryHeader']['gl-cor:entryDetail'])
    for i in range(detail_count):
        keys = list(xml_dict2['xbrli:xbrl']['gl-cor:accountingEntries']['gl-cor:entryHeader']['gl-cor:entryDetail'][i].keys())
        index = 1+keys.index('gl-cor:account')
        # 'gl-cor:amount'を'gl-cor:account'の次に入れ替え
        xml_dict2['xbrli:xbrl']['gl-cor:accountingEntries']['gl-cor:entryHeader']['gl-cor:entryDetail'][i] = modify_dict_element_order(
            xml_dict2['xbrli:xbrl']['gl-cor:accountingEntries']['gl-cor:entryHeader']['gl-cor:entryDetail'][i],
            'gl-cor:debitCreditCode',
            index  # indexはgl-cor:accountの次を指定
        )
        keys = list(xml_dict2['xbrli:xbrl']['gl-cor:accountingEntries']['gl-cor:entryHeader']['gl-cor:entryDetail'][i].keys())
        index = 1+keys.index('gl-cor:account')
        xml_dict2['xbrli:xbrl']['gl-cor:accountingEntries']['gl-cor:entryHeader']['gl-cor:entryDetail'][i] = modify_dict_element_order(
            xml_dict2['xbrli:xbrl']['gl-cor:accountingEntries']['gl-cor:entryHeader']['gl-cor:entryDetail'][i],
            'gl-cor:amount',
            index  # indexはgl-cor:accountの次を指定
        )

        xml_dict2['xbrli:xbrl']['gl-cor:accountingEntries']['gl-cor:entryHeader']['gl-cor:entryDetail'][i]['gl-cor:xbrlInfo'] = modify_dict_element_order(
            xml_dict2['xbrli:xbrl']['gl-cor:accountingEntries']['gl-cor:entryHeader']['gl-cor:entryDetail'][i]['gl-cor:xbrlInfo'],
            'gl-cor:summaryReportingElement',
            0  # 0は先頭を指定
        )

        del xml_dict2['xbrli:xbrl']['gl-cor:accountingEntries']['gl-cor:entryHeader']['gl-cor:entryDetail'][i]['gl-muc:amountCurrency']

    modified_xml = dict_to_etree(xml_dict2)

    # Write the modified XML to the output file
    modified_xml.write(output_file, encoding='utf-8', xml_declaration=True)

    # XMLファイルを読み込む
    tree = ET.parse(output_file)
    # XMLを文字列に変換
    xml_str = ET.tostring(tree.getroot(), encoding='utf-8')
    # 文字列からDOMオブジェクトを作成
    dom = minidom.parseString(xml_str)
    # 整形して文字列化
    pretty_xml_str = dom.toprettyxml(indent='  ')
    # 整形済みのXML文字列をファイルに書き込む
    with open(f'{output_file[:-3]}xbrl', 'w', encoding='utf-8') as file:
        file.write(pretty_xml_str)

def etree_to_dict(t):
    d = {t.tag: {} if t.attrib else None}
    children = list(t)
    if children:
        dd = defaultdict(list)
        for dc in map(etree_to_dict, children):
            for k, v in dc.items():
                dd[k].append(v)
        d = {t.tag: {k: v[0] if len(v) == 1 else v
                     for k, v in dd.items()}}
    if t.attrib:
        d[t.tag].update(('@' + k, v)
                        for k, v in t.attrib.items())
    if t.text:
        text = t.text.strip()
        if children or t.attrib:
            if text:
                d[t.tag]['#text'] = text
        else:
            d[t.tag] = text
    return d

def dict_to_etree(d):
    def _to_etree(d, root):
        if not d:
            pass
        elif isinstance(d, str):
            root.text = d
        elif isinstance(d, dict):
            for k,v in d.items():
                assert isinstance(k, str)
                if k.startswith('#'):
                    assert k == '#text' and isinstance(v, str)
                    root.text = v
                elif k.startswith('@'):
                    assert isinstance(v, str)
                    root.set(k[1:], v)
                elif isinstance(v, list):
                    for e in v:
                        _to_etree(e, ET.SubElement(root, k))
                else:
                    _to_etree(v, ET.SubElement(root, k))
        else:
            raise TypeError('invalid type: ' + str(type(d)))
    assert isinstance(d, dict) and len(d) == 1
    tag, body = next(iter(d.items()))
    node = ET.Element(tag)
    _to_etree(body, node)
    return ET.ElementTree(node)

def main():
    parser = argparse.ArgumentParser(description='Version up XBRL-GL from XBRL Spec 2.0a to 2.1')
    parser.add_argument('-i', dest='input_file', help='Input XML file')
    parser.add_argument('-o', dest='output_file', help='Output XML file')
    parser.add_argument('-d', dest='input_directory', help='Input directory containing XML files')
    parser.add_argument('-x', dest='output_directory', help='Output directory containing XML files')

    args = parser.parse_args()

    in_file = args.input_file
    out_file = args.output_file
    if in_file and out_file:
        in_file = in_file.strip()
        out_file = out_file.strip()
        modify_xml_namespaces(in_file, out_file)
        print(f"Modified XML file has been generated. {in_file} -> {out_file}")
    else:
        in_directory = args.input_directory
        out_directory = args.output_directory
        if not in_directory or not out_directory:
            parser.print_help()
            return
        in_directory = in_directory.strip()
        out_directory = out_directory.strip()
        modify_xml_files_in_directory(in_directory, out_directory)
        print(f"Modified XML file in '{in_directory}' has been generated in '{out_directory}'.")

if __name__ == '__main__':
    main()
