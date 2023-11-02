# print(',Load pint_ja/generate_ubl/dic2etree/__init__.py',)
from .dic2etree import dict_to_etree
from .dic2etree import etree_to_dict

ns = {
  'gl-bus': 'http://www.xbrl.org/taxonomy/int/gl/bus/2003-08-29/',
  'gl-cor': 'http://www.xbrl.org/taxonomy/int/gl/cor/2003-08-29/',
  'gl-muc': 'http://www.xbrl.org/taxonomy/int/gl/muc/2003-08-29/',
  'gl-plt': 'http://www.xbrgl.com/gl-plt/',
  'gl-usk': 'http://www.xbrl.org/taxonomy/int/gl/usk/2003-08-29/',
  'link': 'http://www.xbrl.org/2001/XLink/xbrllinkbase',
  'tdb': 'www.tdb.co.jp',
  'xbrli': 'http://www.xbrl.org/2001/instance',
  'xhtml': 'http://www.w3.org/1999/xhtml',
  'xsi': 'http://www.w3.org/2001/XMLSchema-instance'#,
  # 'jp-bs': 'http://www.xbrl-jp.org/taxonomy/jp/fr/common/bs/2003-08-31',
  # 'jp-gcd': 'http://www.xbrl-jp.org/taxonomy/jp/gcd/2003-08-31',
  # 'jp-pl': 'http://www.xbrl-jp.org/taxonomy/jp/fr/common/pl/2003-08-31',
  # 'jp-sc': 'http://www.xbrl-jp.org/taxonomy/jp/fr/common/sc/2003-08-31',
  # 'jp-sr': 'http://www.xbrl-jp.org/taxonomy/jp/fr/common/sr/2003-08-31',
  # 'jp-ta-bs': 'http://www.xbrl-jp.org/taxonomy/jp/fr/ta/bs/2003-08-31',
  # 'jp-ta-pl': 'http://www.xbrl-jp.org/taxonomy/jp/fr/ta/pl/2003-08-31',
  # 'jp-ta-sc': 'http://www.xbrl-jp.org/taxonomy/jp/fr/ta/sc/2003-08-31',
  # 'jp-ta-sr': 'http://www.xbrl-jp.org/taxonomy/jp/fr/ta/sr/2003-08-31',
  # 'pca-bs': 'http://www.pca.co.jp/taxonomy/jp/fr/bs/2003-08-31',
  # 'pca-pl': 'http://www.pca.co.jp/taxonomy/jp/fr/pl/2003-08-31',
}

__all__ = ['dict_to_etree', 'etree_to_dict', 'ns']