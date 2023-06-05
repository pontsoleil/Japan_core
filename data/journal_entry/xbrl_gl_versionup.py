# from etree import etree
from lxml import etree

def upgrade_xml(old_xml):
    # XMLパーサを作成
    parser = etree.XMLParser(remove_blank_text=True)
    
    # XMLデータをパース
    tree = etree.parse(old_xml, parser=parser)
    root = tree.getroot()
    
    # XMLの名前空間と要素を更新
    nsmap = {
        'xbrli': "http://www.xbrl.org/2003/instance",
        'xbrll': "http://www.xbrl.org/2003/linkbase",
        'xlink': "http://www.w3.org/1999/xlink",
        'xsi': "http://www.w3.org/2001/XMLSchema-instance",
        'gl-cor': "http://www.xbrl.org/int/gl/cor/2015-03-25",
        'gl-muc': "http://www.xbrl.org/int/gl/muc/2015-03-25",
        'gl-bus': "http://www.xbrl.org/int/gl/bus/2015-03-25",
        'gl-plt': "http://www.xbrl.org/int/gl/plt/2015-03-25",
        'iso4217': "http://www.xbrl.org/2003/iso4217",
        'iso639': "http://www.xbrl.org/2005/iso639"
    }

    # ルート要素を新しいバージョンに変更
    new_root = etree.Element(f"{{{nsmap['xbrli']}}}xbrl", nsmap=nsmap)
    
    # 必要な要素と属性を新しいルート要素に追加
    schemaRef = etree.SubElement(new_root, f"{{{nsmap['xbrll']}}}schemaRef", 
                                 {'{http://www.w3.org/1999/xlink}type': 'simple', 
                                  '{http://www.w3.org/1999/xlink}arcrole': 'http://www.w3.org/1999/xlink/properties/linkbase', 
                                  '{http://www.w3.org/1999/xlink}href': '../plt/case-c-b-m-u-t/gl-plt-all-2015-03-25.xsd'})
    
    context = etree.SubElement(new_root, f"{{{nsmap['xbrli']}}}context", id="now")
    entity = etree.SubElement(context, f"{{{nsmap['xbrli']}}}entity")
    identifier = etree.SubElement(entity, f"{{{nsmap['xbrli']}}}identifier", scheme="http://www.xbrl.org/xbrlgl/sample")
    identifier.text = "SAMPLE"
    period = etree.SubElement(context, f"{{{nsmap['xbrli']}}}period")
    instant = etree.SubElement(period, f"{{{nsmap['xbrli']}}}instant")
    instant.text = "2004-10-03"
    
    unit_usd = etree.SubElement(new_root, f"{{{nsmap['xbrli']}}}unit", id="usd")
    measure_usd = etree.SubElement(unit_usd, f"{{{nsmap['xbrli']}}}measure")
    measure_usd.text = "iso4217:USD"
    
    unit_NotUsed = etree.SubElement(new_root, f"{{{nsmap['xbrli']}}}unit", id="NotUsed")
    measure_NotUsed = etree.SubElement(unit_NotUsed, f"{{{nsmap['xbrli']}}}measure")
    measure_NotUsed.text = "pure"
    
    accountingEntries = etree.SubElement(new_root, f"{{{nsmap['gl-cor']}}}accountingEntries")
    
    # 新しいXMLドキュメントを文字列として返す
    return etree.tostring(new_root, pretty_print=True, xml_declaration=True, encoding="UTF-8").decode('utf-8')

old_xml = "data/journal_entry/XBRL_GLinstances/0001-20090401-18-1-1-463.xml"
new_xml = upgrade_xml(old_xml)
print(new_xml)
