package wuwei.japan_core.cius;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.lang.reflect.Method;
import java.util.AbstractList;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;
import java.util.Map.Entry;
import java.util.RandomAccess;
import java.util.Set;
import java.util.List;
import java.util.TreeMap;

import javax.script.ScriptEngine;
import javax.script.ScriptEngineManager;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.transform.OutputKeys;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerException;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.TransformerFactoryConfigurationError;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;
import javax.xml.xpath.XPath;
import javax.xml.xpath.XPathConstants;
import javax.xml.xpath.XPathExpression;
import javax.xml.xpath.XPathExpressionException;
import javax.xml.xpath.XPathFactory;

import org.w3c.dom.Attr;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.NamedNodeMap;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;

import wuwei.japan_core.utils.CSV;
import wuwei.japan_core.utils.NamespaceResolver;

/**
 * 物理ファイルとの入出力とその為のデータ変換を制御するクラス
 */
public class FileHandler 
{
	static String SYNTAX_BINDING             = null;
	static String XML_SKELTON                = null;
	static String JP_PINT_CSV                = "data/base/jp_pint_binding.csv";
	static String JP_PINT_XML_SKELTON        = "data/base/jp_pint_skeleton.xml";
	static String SME_CSV                    = "data/base/sme_binding.csv";
	static String SME_XML_SKELTON            = "data/base/sme_skeleton.xml";
	
	static String XBRL_GL_CSV                = "data/base/xBRL_GL_binding.csv";
	static String IN_DIR                     = "XBRL_GLinstances"; //"data/xml/XBRL-GL";
	static String OUT_CSV                    = "data/csv/XBRL-GL/instances.csv";
	
	public static Document doc               = null;
	public static XPath xpath                = null;
	public static Element root               = null;

	public static String ROOT_ID                   = "NC00";
	public static String ROOT_GL_ID                = "GL02"; // "NC00";
	
	public static Integer ROOT_SEMSORT             = 1000;	
	public static String DOCUMENT_CURRENCY_ID      = "NC00-01"; /*文書通貨コードのID*/
	public static String TAX_CURRENCY_ID           = "NC00-02"; /*税通貨コードのID*/
	public static String INVOICE_ID                = "NC00-19"; /*インボイス番号のID*/	
	public static int MIN_DOCUMENT_TOTAL           = 5190;      /*NC39-NC55 semSort 文書ヘッダ合計金額*/
	public static int MAX_DOCUMENT_TOTAL           = 5260;      /*NC55-07   semSort*/
	public static String TOTAL_TAX_ID              = "NC55-03"; /*文書ヘッダ合計税額のID*/
	public static int TOTAL_TAX                    = 5220;      /*NC55-03 semSort*/
	public static String TOTAL_TAX_CURRENCY_TAX_ID = "NC56-01"; /*外貨建て請求書文書ヘッダ合計税額のID*/
	public static int TOTAL_TAX_CURRENCY_TAX       = 5280;      /*NC56-01 semSort*/
	public static int MIN_TAX_BREAKDOWN            = 5290;      /*NC39-NC57 semSort 文書ヘッダ課税分類*/
	public static int MAX_TAX_BREAKDOWN            = 5390;      /*NC57-10   semSort*/
	public static int MIN_TAX_CURRENCY_BREAKDOWN   = 5400;      /*NC39-NC58 semSort 文書ヘッダ外貨建て課税分類*/
	public static int MAX_TAX_CURRENCY_BREAKDOWN   = 5460;      /*NC58-06   semSort*/
	public static String INVOICE_NUMBER            = null;      /*インボイス番号*/
	public static String DOCUMENT_CURRENCY         = null;      /*文書通貨コード*/
	public static String TAX_CURRENCY              = null;      /*税通貨コード*/
			
	public static boolean TRACE     = false;
	public static boolean DEBUG     = false;
	public static String PROCESSING = null;
	
	public static String SME_ROOT   = "/rsm:SMEinvoice";
	
	public static ArrayList<String> MULTIPLE_ID = new ArrayList<>();
	public static HashMap<String, String> nsURIMap = null;
	
	/**
	 * 終端XML要素
	 */
	public static ArrayList<String> terminalElements = new ArrayList<>();
	
	/**
	 * Tidy dataテーブルの見出し行
	 */
	public static ArrayList<String> header = new ArrayList<>();
	
	/**
	 * Tidy dataテーブル
	 */
	public static ArrayList<ArrayList<String>> tidyData = new ArrayList<>();
	
	public static Map<String/*id*/,	Binding>           bindingDict   = new HashMap<>();
	public static TreeMap<Integer/*semSort*/, Binding> semBindingMap = new TreeMap<>();
	public static TreeMap<Integer/*synSort*/, Binding> synBindingMap = new TreeMap<>();
	
	public static TreeMap<Integer/*parent semSort*/, ArrayList<Integer/*child semSort*/>> semChildMap = new TreeMap<>();
	public static TreeMap<Integer/*parent synSort*/, ArrayList<Integer/*child synSort*/>> synChildMap = new TreeMap<>();
	public static TreeMap<Integer/*child semSort*/, Integer/*parent semSort*/> semParentMap = new TreeMap<>();
	public static TreeMap<Integer/*child synSort*/, Integer/*parent synSort*/> synParentMap = new TreeMap<>();
	
//	public static TreeMap<Integer/*semSort*/, String/*id*/> multipleMap                     = new TreeMap<>();
	
	public static TreeMap<Integer/*semSort*/, ParsedNode> nodeMap                           = new TreeMap<>();

	/**
 	 * The application's entry point
	 * @param args an array of command-line arguments for the application
	 * last updated 2023-02-24
	 */
	public static void main(String[] args) { }
	
	/**
	 * セマンティックモデル定義及びシンタクスバインディング定義シートを読み込み定義情報を次の広域変数に設定する。<br>
	 * Map&lt;String(id),Binding> bindingDict<br>
	 * TreeMap&lt;Integer(semSort), Binding> semBindingMap<br>
	 * TreeMap&lt;Integer(synSort), Binding> synBindingMap
	 */
	public static void parseBinding() 
	{
		if (DEBUG) System.out.println(" (FileHandler) parseBinding");

		Integer[] parents       = new Integer[10];
		Binding[] bindingParent = new Binding[10];
		ArrayList<ArrayList<String>> binding_data = new ArrayList<>();
		Binding binding = null;
		Binding parentBinding;
		Integer semSort, synSort, level, parent_level;
		String  id, xPath, strippedXPath, additionalXPath;
		String  parentID, parentXPath, strippedParentXPath;
		int     idx;
		try 
		{
			FileInputStream fileInputStream = new FileInputStream(SYNTAX_BINDING);
			binding_data = CSV.readFile(fileInputStream, "UTF-8");
			ArrayList<String> headers = binding_data.get(0);
			for (int n=1; n < binding_data.size(); n++) 
			{
				ArrayList<String> cells = binding_data.get(n);
				// semSort,id,card,level,businessTerm,desc,defaultValue,dataType,syntaxID,businessTerm_en,businessTerm_ja,desc_ja,synSort,xPath,occur			
				// 0       1  2    3     4            5    6            7        8        9               10              11      12      13    14
				binding = new Binding(0, "", 0, "", "", "", "", 0, "", "");
				for (int i = 0; i < cells.size(); i++) 
				{
					String key = headers.get(i);
					if (0==i) 
					{
						key	= key.replace("\uFEFF", "");
					}
					String value = cells.get(i);
					semSort = synSort = -1;
					level = 0;
					switch (key) 
					{
						case "semSort":
							if (value.matches("^[0-9]+$"))
							{
								semSort = Integer.parseInt(value);
								binding.setSemSort(semSort);
							}
							break;
						case "id":
							binding.setID(value);
							if (value.length() > 0 && value.toUpperCase().matches("^NC[0-9]+-NC[0-9]+$"))
								MULTIPLE_ID.add(value);
							break;
						case "defaultValue":
							if (value.length() > 0 &&!"?".equals(value))
								binding.setDefaultValue(value);
							break;
						case "card":
							binding.setCard(value);
							break;
						case "level":
							if (value.matches("^[0-9]+$"))
							{
								level = Integer.parseInt(value);
								binding.setLevel(level);
							}
							break;
						case "businessTerm":
							binding.setBT(value);
							break;
						case "dataType":
							binding.setDatatype(value);
							break;
						case "synSort":
							if (value.matches("^[0-9]+$"))
							{
								synSort = Integer.parseInt(value);
								binding.setSynSort(synSort);
							}
							break;
						case "xPath":
							binding.setXPath(value);
							if (PROCESSING.indexOf("SYNTAX")>0) 
							{
								xPath = stripSelector(value);
								level = countChar('/', xPath) - 1;
								binding.setLevel(level);
							}
							break;
						case "occur":
							binding.setOccur(value);
					}
				}
				id      = binding.getID();
				semSort = binding.getSemSort();
				synSort = binding.getSynSort();
				bindingDict.put(id, binding);
				if (semSort > 0)
					semBindingMap.put(semSort, binding);
				if (synSort > 0)
					synBindingMap.put(synSort, binding);
				if (DEBUG) System.out.println(" (FileHandler) parseBinding "+id+" semSort:"+semSort+" synSort:"+synSort+" "+binding.getXPath());
			}
			
			if (PROCESSING.indexOf("SEMANTICS")>0) 
			{
				for (Entry<Integer, Binding> entry : semBindingMap.entrySet()) 
				{
					semSort        = entry.getKey();
					binding        = entry.getValue();
					level          = binding.getLevel();
					id             = binding.getID();
					if (null==id || "".equals(id))
						continue;
//					if (null==semSort)
//						if (DEBUG) System.out.println(id+"("+semSort+")");
					parents[level] = semSort;
					parent_level   = 0;
					ArrayList<Integer> children = null;
					if (0==Integer.compare(ROOT_SEMSORT,semSort))
						continue;
					try 
					{
						if (java.util.Objects.equals(0,level)) 
						{
							if (semChildMap.containsKey(ROOT_SEMSORT)) 
							{
								children = semChildMap.get(ROOT_SEMSORT);
							} else 
							{
								children = new ArrayList<Integer>();
							}
							if (ROOT_SEMSORT!=semSort) 
							{
								children.add(semSort);
								semChildMap.put(ROOT_SEMSORT, children);
								semParentMap.put(semSort, ROOT_SEMSORT);
							}
						} else if (level > 0) 
						{
							parent_level          = level - 1;
							Integer parentSemSort = parents[parent_level];				
							if (null==parentSemSort)
								if (DEBUG) System.out.println(semSort);
							if (semChildMap.containsKey(parentSemSort)) 
							{
								children = semChildMap.get(parentSemSort);
							} else 
							{
								children = new ArrayList<Integer>();
							}
							if (parentSemSort!=semSort) 
							{
								children.add(semSort);
								semChildMap.put(parentSemSort, children);
								semParentMap.put(semSort, parentSemSort);
							}
						}
					} catch (Exception e) 
					{
						// TODO Auto-generated catch block
						e.printStackTrace();
					}				
				}
			  
				for (Entry<Integer, Binding> entry : semBindingMap.entrySet()) 
				{
					binding       = entry.getValue();
					id            = binding.getID();
					semSort       = binding.getSemSort();
					xPath         = binding.getXPath();
					strippedXPath = stripSelector(xPath);
					idx = strippedXPath.lastIndexOf("/");
					additionalXPath = "";
					if (idx >= 0) 
					{
						additionalXPath = strippedXPath.substring(0, idx);
					}
					level                = binding.getLevel();
					bindingParent[level] = binding;
					if (level > 0) 
					{
						parent_level  = level - 1;
						parentBinding = bindingParent[parent_level];
						parentID      = parentBinding.getID();
						parentXPath   = parentBinding.getXPath();
						strippedParentXPath = stripSelector(parentXPath);
						if (DEBUG) System.out.println(" (FileHandler) parseBinding check additional XPath " + parentID + "->" + id);
						if (additionalXPath.length() > 0 && additionalXPath.lastIndexOf("/") > 0 &&
								strippedParentXPath.indexOf(additionalXPath) >= 0 &&
								additionalXPath.indexOf(strippedParentXPath) < 0) 
						{
							additionalXPath = resumeSelector(additionalXPath, xPath);
							if (DEBUG) System.out.println(id+" "+xPath+" "+parentID+" "+parentXPath+"\n    ADDED parent XPath: "+parentXPath+" additional Xpath: "+additionalXPath);
							parentBinding.addAdditionalXPath(additionalXPath);
						} else if (idx > 0 && xPath.length() > 0 && xPath.lastIndexOf("/") > 0 &&
								strippedParentXPath.indexOf(xPath) >= 0 &&
								xPath.indexOf(strippedParentXPath) < 0) 
						{
							additionalXPath = xPath;
							if (DEBUG) System.out.println(id+" "+xPath+" "+parentID+" "+parentXPath+"\n    ADDED parent XPath: "+parentXPath+" additional Xpath: "+additionalXPath);
							parentBinding.addAdditionalXPath(additionalXPath);
						}
					}
				}
			} else if (PROCESSING.indexOf("SYNTAX")>0) 
			{
				for (Entry<Integer, Binding> entry : synBindingMap.entrySet()) 
				{
					synSort       = entry.getKey();
					binding       = entry.getValue();
					xPath         = binding.getXPath();
					strippedXPath = stripSelector(xPath);
					level         = binding.getLevel();
					if (0==PROCESSING.indexOf("SME-COMMON") && (
							strippedXPath.indexOf("udt:") > 0 ||
							strippedXPath.indexOf("ram:TelephoneCIUniversalCommunication") > 0 ||
							strippedXPath.indexOf("ram:FaxCIUniversalCommunication") > 0 ||
							strippedXPath.indexOf("ram:EmailURICIUniversalCommunication") > 0 ))
					{
						level -= 1;
					}
					parents[level] = synSort;
					if (level > 0) 
					{
						parent_level                = level - 1;
						Integer parentSynSort       = parents[parent_level];
						ArrayList<Integer> children = null;
						if (synChildMap.containsKey(parentSynSort)) 
						{
							children = synChildMap.get(parentSynSort);
						} else 
						{
							children = new ArrayList<Integer>();
						}
						children.add(synSort);
						synChildMap.put(parentSynSort, children);
						for (Integer childSynSort: children) 
						{
							synParentMap.put(childSynSort, parentSynSort);
						}
					}
				}
			}
		}
		catch (IOException e) 
		{
		  e.printStackTrace();
		}
	}
	
	private static int countChar(char ch, String str) {
		int count = 0;
		for (int i = 0; i < str.length(); i++) 
		{
			if (str.charAt(i) == ch) 
			{
				count++;
			}
		}
		return count;
	}
	
	/**
	 * 変換元のデジタルインボイスを読み込み、XML DOM及び名前空間を指定したXPathが使用できるように<br>
	 * XML DOM Document: doc, ルート要素(Element: root)及びxpath(XPath: xpath)を広域変数に設定する。
	 * 
	 * @param xmlfile 変換元のデジタルインボイス
	 */
	public static void parseInvoice(String xmlfile) 
	{
		try 
		{
			//Build DOM
			DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
			factory.setNamespaceAware(true); // never forget this!
			DocumentBuilder builder        = factory.newDocumentBuilder();
			doc                            = builder.parse(new FileInputStream(new File(xmlfile)));
			//Create XPath
			XPathFactory xpathfactory      = XPathFactory.newInstance();
			xpath                          = xpathfactory.newXPath();
			xpath.setNamespaceContext(new NamespaceResolver(doc));
			// root
			root = (Element) doc.getChildNodes().item(0);
		 	nsURIMap = new HashMap<String,String>();
		 	NamedNodeMap attributes = root.getAttributes();
		 	for (int i = 0; i < attributes.getLength(); i++) 
		 	{
		 		Node attribute = attributes.item(i);
				String name = attribute.getNodeName();
				if ("xmlns".equals(name)) 
				{
					name = "";
				} else 
				{
					name = name.replace("xmlns:","");
				}
				String value = attribute.getNodeValue();
				nsURIMap.put(name, value);
			}
		} catch (Exception e) 
		{
			e.printStackTrace();
		}
	}
	
	/**
	 * semSortをキーにバインディング定義のXPathを検索し、それ使用してdocに定義されている要素を取り出して作成したTreeMapであるnodeMapを作成する。
	 * 
	 * @return nodeMap semSortをキーとするTreeMap&lt;Integer(semSort) ParsedNod&gt;
	 * 
	 */
	public static TreeMap<Integer, ParsedNode> parseDoc() 
	{
		TreeMap<Integer/*semSort*/, ParsedNode> nodeMap = new TreeMap<>();
		for (Integer semSort: semBindingMap.keySet()) 
		{
			Binding binding = semBindingMap.get(semSort);
			String xPath = binding.getXPath();
			List<Node> nodes = getXPath(root, xPath);
			if (null!=nodes) 
			{
				if (nodes.size() > 0) 
				{
					binding.setUsed(true);
				}
				ParsedNode parsedNode = new ParsedNode(binding, nodes);
				nodeMap.put(semSort, parsedNode);
			}
		}
		return nodeMap;
	}
	
	/**
	 * デジタルインボイスのルート要素のみが定義されたスキーマファイルXML_SKELTONを読み込んで名前空間を定義する。
	 */
	public static void parseSkeleton() 
	{
		String skeleton = XML_SKELTON;
		try 
		{
			//Build DOM
			DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
			factory.setNamespaceAware(true); // never forget this!
			DocumentBuilder builder = factory.newDocumentBuilder();
			//Parse XML file
			FileInputStream fis = new FileInputStream(new File(skeleton));
			doc = builder.parse(fis);
			//Create XPath
			XPathFactory xpathfactory = XPathFactory.newInstance();
			xpath = xpathfactory.newXPath();
			xpath.setNamespaceContext(new NamespaceResolver(doc));
			// root
		 	root                    = (Element) doc.getChildNodes().item(0);
		 	nsURIMap                = new HashMap<String,String>();
		 	NamedNodeMap attributes = root.getAttributes();
		 	for (int i = 0; i < attributes.getLength(); i++) 
		 	{
		 		Node attribute = attributes.item(i);
				String name    = attribute.getNodeName();
				if ("xmlns".equals(name)) 
				{
					name = "";
				} else 
				{
					name = name.replace("xmlns:","");
				}
				String value = attribute.getNodeValue();
				nsURIMap.put(name, value);
			}
		} catch (Exception e) 
		{
			e.printStackTrace();
		}
	}
	
	/**
	 * セマンティックモデルのidから、バインディング情報のsemSortを検索し、その値を用いてnodeMapから該当するNodeの値を取り出してnodeValueMapを作成する。
	 * 
	 * @param id セマンティックモデルのid
	 * @return nodeValueMap TreeMap&lt;Integer(順序番号), String(Nodeの値)&gt;
	 */
	public static TreeMap<Integer, String> getNodeValues(String id) 
	{
		TreeMap<Integer, String> nodeValueMap = new TreeMap<>();
		Binding binding = bindingDict.get(id);
		Integer sort = binding.getSemSort();
		
		ParsedNode parsedNode = nodeMap.get(sort);
		
		List<Node> nodes = parsedNode.nodes;
		for (int i = 0; i < nodes.size(); i++) 
		{
			Node node = nodes.get(i);
			String value = node.getTextContent().trim();
			nodeValueMap.put(i, value);
		}
		return nodeValueMap;
	}
	
//	/**
//	 * 子要素のidからバインディング定義のXPathを取り出してそれを使用して親要素の下位にある子要素を探し出し、その結果をリストとして返す。
//	 * 
//	 * @param parent　親要素
//	 * @param id　子要素のid
//	 * @return nodes XPathに該当する要素のリスト List&lt;Node&gt; nodes
//	 */
//	public static List<Node> getElements(Element parent, String id) 
//	{
//		Binding binding = (Binding) bindingDict.get(id);
//		String xpath = binding.getXPath();
//		xpath = xpath.replaceAll("/Invoice", "/*");
//		xpath = xpath.replaceAll("/ubl:Invoice", "/*");
//		if (null==parent) {
//			if (DEBUG) System.out.println("- FileHaldler.getElements parent null");
//			return null;
//		}
//		if (id.toLowerCase().matches("^ibt-.+$")) {
//			xpath += "/text()";
//		}
//		List<Node> nodes = getXPathNodes(parent, xpath);
//		return nodes;
//	}
	
	/**
	 * 親要素から指定されたXPathに該当する要素を探す。
	 * 
	 * @param parent 親要素
	 * @param xpath 親要素からのXPath
	 * @return
	 */
	public static List<Node> getXPath(Element parent, String xpath) 
	{
		xpath = xpath.replaceAll("/(Invoice|ubl:Invoice)/", "/*/");
		if (null==parent) 
		{
			if (DEBUG) System.out.println("- FileHaldler.getXPath parent null");
			return null;
		}
		List<Node> nodes = getXPathNodes(parent, xpath);
		return nodes;
	}

	/**
	 * セマンティックモデルに基づいて親要素のidから次の方法で子要素を探す。
	 * <ul>
	 * <li>親要素から子要素のXPathに基づいて指定されたXML要素を探す.</li>
	 * <li>及び構文バインディングでは定義されていないが子要素のXPathから、その親要素のXPathのXML要素を追加定義する.</li>
	 * </ul>
	 * 
	 * @param parent 親要素
	 * @param parent_id 親要素のid
	 * @return 親要素のsemSortをキーとし、子要素(Node)のリストを値とするTreeMap
	 */
	public static TreeMap<Integer, List<Node>> getChildren(Node parent, String parent_id) 
	{
		TreeMap<Integer, List<Node>> childList = new TreeMap<>();	
		Binding binding = (Binding) bindingDict.get(parent_id);
		Integer parentSemSort = binding.getSemSort();
		String parentXPath = binding.getXPath();
		if (DEBUG) System.out.println(" (FileHandler) getChildren "+parent_id+"("+parentSemSort+") "+parentXPath);

		ArrayList<Integer> children = semChildMap.get(parentSemSort);
		
		if (null!=children) 
		{
			for (Integer sort: children) 
			{
				Binding child_binding       = (Binding) semBindingMap.get(sort);
				String child_xpath          = child_binding.getXPath();
				String defaultValue         = child_binding.getDefaultValue();
				Set<String> additionalXPath = child_binding.getAdditionalXPath();
				List<Node> nodes            = null;
				if (null==parentXPath) {
					System.out.println("null parentXPath");
				}
				if (child_xpath.substring(1).indexOf("/") > 0 && 0==child_xpath.indexOf(parentXPath)) 
				{
					child_xpath = child_xpath.replace(parentXPath, ".");				
					nodes = getXPathNodes(parent, child_xpath);
				} else {
					nodes = getXPathNodes(root, child_xpath);
				}
				
				if (null!=nodes && nodes.size() > 0) 
				{
					childList.put(sort, nodes);
				} else if (PROCESSING.indexOf("SYNTAX") > 0 && defaultValue.length() > 0) 
				{
					// 未定義だが固定値が定義されている要素についてその値が定義されたNodeを返す。
					String element_name = child_xpath.substring(1+child_xpath.lastIndexOf('/'));
					String ns           = element_name.substring(0,element_name.indexOf(':'));
					String nsURI        = nsURIMap.get(ns);
					String qname        = element_name.substring(1+element_name.indexOf(':'));		
					Node child_node     = appendElementNS((Element) parent, nsURI, ns, qname, defaultValue, null);
					nodes = new ArrayList<>();
					nodes.add(child_node);
					childList.put(sort, nodes);
				} else if (null!=additionalXPath) 
				{
					for (Iterator<String> iterator = additionalXPath.iterator(); iterator.hasNext();) 
					{
						String additional_xpath     = iterator.next();
						List<Node> additional_nodes = getXPathNodes(parent, additional_xpath);
						if (additional_nodes.size() > 0) 
						{
							nodes = getXPathNodes(additional_nodes.get(0), child_xpath);
							if (nodes.size() > 0)
								childList.put(sort, nodes);
						}
					}
				} 
			}
		}
		return childList;
	}

	/**
	 * 親のXML要素から指定されたXPathにあるXML要素を探し見つかった要素を返す.
	 * 
	 * @param parent 親のXML要素
	 * @param xPath 親のXML要素からのXPath
	 * @return XPathで指定された位置にある子のXML要素のリスト
	 */
	public static List<Node> getXPathNodes(
			Node parent, 
			String xPath ) 
	{
		if (null==xPath || 0==xPath.length())
			return null;
		XPathExpression expr = null;
		List<Node> nodeList  = new ArrayList<>();
		List<Node> nodes     = new ArrayList<>();
		NodeList result;
		try 
		{
			if (0==PROCESSING.indexOf("JP-PINT")) 
			{
				xPath = xPath.replace("/Invoice", "/*");
			} else if (0==PROCESSING.indexOf("SME-COMMON") && xPath.indexOf("ram:TaxCurrencyCode]")>0) 
			{
				if (DEBUG) System.out.println(" (FileHandler) getXPathNodes "+xPath);
			}
			// XMLパーサーが[??=true()]や[??=false()]のBool値を判定できないため、文字列として判定する形にXPathを書き換える。
			if (xPath.indexOf("true")>0 || xPath.indexOf("false")>0) 
//			{
//				xPath = xPath.replaceAll("\\[([:a-zA-Z]*)=true\\(\\)\\]","[normalize-space($1/text())='true']");
//			} else if (xPath.indexOf("false")>0) 
			{
				xPath = xPath.replace("[", "[normalize-space(");
				xPath = xPath.replace("=", "/text())='");
				xPath = xPath.replace("()]", "']");				
//				xPath = xPath.replaceAll("\\[([:a-zA-Z]*)=false\\(\\)\\]","[normalize-space($1/text())='false']");
			// XMLパーサーが[cbc:TaxAmount/@currencyID=./cbc:DocumentCurrencyCode]を正しく判定できないので、固定値との比較に書き換える。
			} else if (0==PROCESSING.indexOf("JP-PINT")) 
			{
				if (xPath.indexOf("cbc:DocumentCurrencyCode]")>0) 
				{
					xPath = xPath.replaceAll("(/Invoice|/\\*|\\.)/cbc:DocumentCurrencyCode","'"+DOCUMENT_CURRENCY+"'");
				} else if (null!=TAX_CURRENCY && xPath.indexOf("cbc:TaxCurrencyCode]")>0) 
				{
					xPath = xPath.replaceAll("(/Invoice|/\\*|\\.)/cbc:TaxCurrencyCode","'"+TAX_CURRENCY+"'");
				}
			} else if (0==PROCESSING.indexOf("SME-COMMON")) 
			{
				if (xPath.indexOf("ram:InvoiceCurrencyCode]")>0) 
				{
					xPath = xPath.replaceAll(
							"//rsm:CIIHSupplyChainTradeTransaction/ram:ApplicableCIIHSupplyChainTradeSettlement/ram:InvoiceCurrencyCode",
							"'"+DOCUMENT_CURRENCY+"'");
				} else if (null!=TAX_CURRENCY && xPath.indexOf("ram:TaxCurrencyCode]")>0) 
				{
					xPath = xPath.replaceAll(
							"//rsm:CIIHSupplyChainTradeTransaction/ram:ApplicableCIIHSupplyChainTradeSettlement/ram:TaxCurrencyCode",
							"'"+TAX_CURRENCY+"'");
				}
			}
			expr     = xpath.compile(xPath);
			result   = (NodeList) expr.evaluate(parent, XPathConstants.NODESET);
			nodeList = asList(result); // https://stackoverflow.com/questions/50509663/convert-nodelist-to-list-in-java
			int len  = nodeList.size();
			for (int i = 0; i < len; i++) 
			{
			  final Node node = nodeList.get(i);
			  if (node.getNodeType() == Node.ELEMENT_NODE ||
					  node.getNodeType() == Node.TEXT_NODE ||
					  node.getNodeType() == Node.ATTRIBUTE_NODE) 
			  { // この他は無視する。
				  nodes.add((Node) node);
			  }
			}
			return nodes;	
		} catch (XPathExpressionException e) 
		{
			e.printStackTrace();
			return null;
		}
	}
	
	// https://stackoverflow.com/questions/19589231/can-i-iterate-through-a-nodelist-using-for-each-in-java
	/**
	 * XML要素のNodeListをXML要素のリストList&lt;Node&gt;に変換する.
	 * @param nodes XML要素のNodeList
	 * @return 変換されたXML要素のリスト List&lt;Node&gt;
	 */
	public static List<Node> asList(NodeList nodes) 
	{
		return nodes.getLength()==0
				? Collections.<Node>emptyList()
				: new NodeListWrapper(nodes);
	}
	/**
	 * XML要素のNodeListをXML要素のリストList&lt;Node&gt;に変換するためのリストのラッパークラス.<br>
	 * asList()関数で使用する.
	 */
	static final class NodeListWrapper extends AbstractList<Node>	  
	implements RandomAccess 
	{
		private final NodeList list;
		NodeListWrapper(NodeList l) 
		{
		  list=l;
		}
		public Node get(int index) 
		{
		  return list.item(index);
		}
		public int size() 
		{
		  return list.getLength();
		}
	}
	
	/**
	 * XPathの文字列中に選択条件を指定するSelectorの文字列が含まれていればそのSelector文字列を返す.
	 * @param xPath XPathの文字列.
	 * @return 選択条件を指定するSelectorの文字列 [条件式]
	 */
	public static String extractSelector(String xPath) 
	{
		int start = xPath.indexOf("[");
		int last = xPath.lastIndexOf("]");
		String selector = "";
		if (start >= 0) 
		{
			selector = xPath.substring(start, last+1);
		}
		return selector;
	}
	
	/**
	 * XPathの文字列中に選択条件を指定するSelectorの文字列が含まれていればそのSelector文字列を削除したXPath文字列を返す.
	 * @param xPath XPathの文字列.
	 * @return 選択条件を指定するSelectorの文字列 [条件式] を削除したXPath文字列.
	 */
	public static String stripSelector(String path) 
	{
		int start = path.indexOf("[");
		int last = path.lastIndexOf("]");
		if (start >= 0) 
		{
			path = path.substring(0, start) + path.substring(last+1,path.length());	
		}
		return path;
	}
	
	/**
	 * 選択条件を指定するSelector文字列を削除したXPath文字列に、Selectorの文字列を含むXPathの文字列からSelectorを取り出し、そのSelectorをSelector文字列を削除したXPath文字列に戻してその文字列を返す.
	 * 
	 * @param strippedPath Selector文字列を削除したXPath文字列.
	 * @param path Selectorの文字列を含むXPathの文字列.
	 * @return resumedPath Selector文字列を削除したXPath文字列にSelectorを戻した文字列.
	 */
	public static String resumeSelector(String strippedPath, String path) 
	{
		String resumedPath = strippedPath;
		if (strippedPath.indexOf("cac:AllowanceCharge") >= 0) 
		{
			int start = path.indexOf("[");
			int last = path.lastIndexOf("]");
			if (start >= 0) 
			{
				String selector = path.substring(start, last+1);
				String hdr = strippedPath.substring(0, start);
				if (start+1 > strippedPath.length()) 
				{
					resumedPath = hdr + selector;
				} else 
				{
					String trailer = strippedPath.substring(start+1, strippedPath.length());
					resumedPath = hdr + selector + "/" + trailer;
				}
			}
		}
		return resumedPath;	
	}

	/**
	 * XML DOM DocumentにXML要素を追加定義し、そのXML要素を親のXML要素の子要素として追加する.
	 * 
	 * @param parent 親のXML要素.
	 * @param nsURI XML要素の名前空間URI.
	 * @param prefix XML要素の名前空間を指定する接頭辞.
	 * @param qname XML要素の名前.
	 * @param value XML要素の値.
	 * @param attrMap　XML要素の属性.
	 * 
	 * @return element 
	 */
	public static Element appendElementNS (
			Element parent,
			String nsURI, 
			String prefix, 
			String qname, 
			String value, 
			HashMap<String, String> attrMap ) 
	{
		if (null==parent) {
			if (DEBUG) System.out.println("- FileHaldler.appendElementNS parent "+prefix+":"+qname+" is NULL. return null.");
			return null;
		}
		try 
		{
			if ("@".equals(qname.substring(0,1))) 
			{
				String attrName = qname.substring(1, qname.length());
				
				Attr attribute = doc.createAttribute(attrName);
				
				attribute.setValue(value);
				parent.setAttributeNode(attribute);
				return parent;
			} else 
			{				
				Element element = doc.createElementNS(nsURI, qname);
				
				element.setPrefix(prefix); // Set the desired namespace and prefix
				if (value!="") 
				{
					element.setTextContent(value);					
				}
				if (null!=attrMap && attrMap.size() > 0) 
				{
					for (Map.Entry<String, String> entry : attrMap.entrySet()) 
					{
					   String name = entry.getKey();
					   String attr = entry.getValue();
					   Attr attribute = doc.createAttribute(name);
					   attribute.setValue(attr);
					   element.setAttributeNode(attribute);
					}
				}
				parent.appendChild(element);				
				return element;
			}
		} catch (Exception e) 
		{
			e.printStackTrace();
			return null;
		}
	}
	
	/**
	 * XML DOOM DocumentをXMLインスタンス文書ファイルに出力する.
	 * 
	 * @param doc XML DOOM Document
	 * @param filename XMLインスタンス文書ファイル名
	 * 
	 * @throws FileNotFoundException
	 * @throws TransformerException
	 * @throws TransformerFactoryConfigurationError
	 * @throws IOException
	 */
	public static void writeXML(
			Document doc, 
			String filename )
		throws
			FileNotFoundException,
			TransformerException,
			TransformerFactoryConfigurationError,
			IOException 
	{
		TransformerFactory transformerFactory = TransformerFactory.newInstance();
		Transformer transformer = transformerFactory.newTransformer();
		DOMSource source = new DOMSource(doc);
		FileOutputStream output = new FileOutputStream(filename);
		StreamResult result = new StreamResult(output);
		// pretty print XML
		transformer.setOutputProperty(OutputKeys.INDENT, "yes");
		transformer.transform(source, result);
	}

	/**
	 * Tidy dataテーブルをCSVファイルに出力する.
	 * 
	 * @param filename CSVファイル名.
	 * @param charset 文字コード.
	 * @param delimiter 区切り記号.
	 * 
	 * @throws FileNotFoundException
	 * @throws IOException
	 */
	public static void csvFileWrite(
			ArrayList<ArrayList<String>> data,
			String filename, 
			String charset,
			String delimiter,
			boolean append)
		throws
			FileNotFoundException,
			IOException 
	{
		if (DEBUG) System.out.println(" (FileHandler) csvFileWrite " + filename + " " + charset+" delimiter="+delimiter);
		CSV.csvFileWrite(data, filename, charset, delimiter, append);
	}

	/**
	 * CSVファイルから読み込んでTidy dataテーブルに展開する.
	 * 
	 * @param filename CSVファイル名.
	 * @param charset 文字コード.
	 * 
	 * @throws FileNotFoundException
	 * @throws IOException
	 */
	public static void csvFileRead(
			String filename, 
			String charset )
		throws
			FileNotFoundException,
			IOException 
	{
		if (DEBUG) System.out.println(" (FileHandler) csvFileRead " + filename + " " + charset);
		FileInputStream fileInputStream = new FileInputStream(filename);		
		ArrayList<ArrayList<String>> data = CSV.readFile(fileInputStream, charset);		
		// header
		header = new ArrayList<String>();
		ArrayList<String> fields = data.get(0);
		int headerCount = fields.size();
		TreeMap<Integer,Integer> headerMap = new TreeMap<>();
		int offset = 0;
		for (int i = 0; i < headerCount; i++) 
		{
			String id = fields.get(i);
			if (0==id.indexOf("d_"))
				id = id.substring(2);
			if (id.toUpperCase().matches("^NC00$") || id.toUpperCase().matches("^NC[0-9]+-NC[0-9]+$"))
				offset += 1;
			else
				break;				
		}
		String id = "";
		Integer synSort = 0;
		for (int i = 0; i < headerCount; i++) 
		{
			if (i < offset)
				continue;
			id = fields.get(i);			
			Binding binding = bindingDict.get(id);
			if (null==binding)
				System.out.println(id + " is not defined in bindingMap.");
			else
			{
				synSort = binding.getSynSort();
				if (synSort >= 1000)
					headerMap.put(synSort, i);
				else
					System.out.println(id + " is defined in bindingMap with NO synSort.");
			}
		}
		// header
		for (int i = 0; i < offset; i++) 
		{
			String field = fields.get(i);
			if (0==field.indexOf("d_"))
				field = field.substring(2);
			header.add(field);
		}
		for (Map.Entry<Integer,Integer> entry : headerMap.entrySet()) 
		{
			Integer i = entry.getValue();
			String field = "";
			if (i < fields.size())
				field = fields.get(i);
			header.add(field);
		}
		// data
		tidyData = new ArrayList<ArrayList<String>>();
		for (int n = 1; n < data.size(); n++) 
		{
			fields = data.get(n);
			ArrayList<String> record = new ArrayList<String>();
			for (int i = 0; i < offset; i++) 
			{
				String field = fields.get(i);
				record.add(field);
			}			
			for (Map.Entry<Integer,Integer> entry : headerMap.entrySet()) 
			{
				int i = entry.getValue();
				String field = "";
				if (i < fields.size())
					field = fields.get(i);
				record.add(field);
			}			
			tidyData.add(record);
		}
		fileInputStream.close();
	}
	
	/**
	 * デバッグ時のログ出力のためにXPathの文字列を短縮する。
	 * 
	 * @param path XPath文字列
	 * @return　短縮された path
	 */
	public static String getShortPath(String path) 
	{
		if (0==PROCESSING.indexOf("SME-COMMON"))
		{
			String _path = path;
			_path = _path.replace("[ram:TaxTotalAmount/@currencyID=/rsm:SMEinvoice/rsm:CIIHSupplyChainTradeTransaction/ram:ApplicableCIIHSupplyChainTradeSettlement","[ram:TaxTotalAmount/@currencyID=...");
			_path = _path.replace("[ram:CurrencyCode=/rsm:SMEinvoice/rsm:CIIHSupplyChainTradeTransaction/ram:ApplicableCIIHSupplyChainTradeSettlement","[ram:CurrencyCode=...");
			_path = _path.replace("/rsm:SMEinvoice/rsm:CIIHSupplyChainTradeTransaction/ram:ApplicableCIIHSupplyChainTradeAgreement/","...Agreement/");
			_path = _path.replace("/rsm:SMEinvoice/rsm:CIIHSupplyChainTradeTransaction/ram:IncludedCIILSupplyChainTradeLineItem/","...LineItem/");
			_path = _path.replace("/rsm:SMEinvoice/rsm:CIIHSupplyChainTradeTransaction/ram:ApplicableCIIHSupplyChainTradeSettlement/","...Settlement/");
			return _path;
		} else
		{
			return path;
		}
	}

}