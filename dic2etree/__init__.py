# print("Load pint_ja/generate_ubl/dic2etree/__init__.py")
from .dic2etree import dict_to_etree
from .dic2etree import etree_to_dict

ns = {
  '': 'urn:oasis:names:specification:ubl:schema:xsd:Invoice-2',
  'xsd': 'http://www.w3.org/2001/XMLSchema',
  'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
  'ext': 'urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2',
  'cac': 'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2',
  'cbc': 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2',
  'qdt': 'urn:oasis:names:specification:ubl:schema:xsd:QualifiedDataTypes-2',
  'udt': 'urn:oasis:names:specification:ubl:schema:xsd:UnqualifiedDataTypes-2',
  'ccts': 'urn:un:unece:uncefact:documentation:2',
  'cn': 'urn:oasis:names:specification:ubl:schema:xsd:CreditNote-2',
  'ubl': 'urn:oasis:names:specification:ubl:schema:xsd:Invoice-2',
  # 
  'qdt':"urn:un:unece:uncefact:data:standard:QualifiedDataType:100",
  'udt':"urn:un:unece:uncefact:data:standard:UnqualifiedDataType:100",
  'rsm':"urn:un:unece:uncefact:data:standard:CrossIndustryInvoice:100",
  'ram':"urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
  # CEN/TS 16931-3-3
  # 'rsm': 'urn:un:unece:uncefact:data:standard:CrossIndustryInvoice:23',
  # 'ccts': 'urn:un:unece:uncefact:documentation:standard:CoreComponentsTechnicalSpecification:2',
  # 'udt': 'urn:un:unece:uncefact:data:standard:UnqualifiedDataType:31',
  # 'qdt': 'urn:un:unece:uncefact:data:standard:QualifiedDataType:31',
  # 'ram': 'urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:31',
  'sch': 'http://purl.oclc.org/dsdl/schematron'
}

xbrl = {
  'xbrll': 'http://www.xbrl.org/2003/linkbase',
	'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
	'xlink': 'http://www.w3.org/1999/xlink',
	'iso639': 'http://www.xbrl.org/2005/iso639',
	'iso4217': 'http://www.xbrl.org/2003/iso4217',
	'xbrli': 'http://www.xbrl.org/2003/instance',
	'xbrldi': 'http://xbrl.org/2006/xbrldi',
	'pint': 'http://www.xbrl.org/int/pint/2022-12-31'
}

__all__ = ['dict_to_etree', 'etree_to_dict', 'ns', 'xbrl']