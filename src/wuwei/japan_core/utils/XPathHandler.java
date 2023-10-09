package wuwei.japan_core.utils;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;

import java.util.AbstractList;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;
// import java.util.Map.Entry;
import java.util.RandomAccess;
import java.util.Set;
import java.util.List;
import java.util.TreeMap;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
// import javax.xml.parsers.ParserConfigurationException;
import javax.xml.transform.OutputKeys;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerException;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.TransformerFactoryConfigurationError;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;
import javax.xml.xpath.XPath;
import javax.xml.xpath.XPathConstants;
//import javax.xml.xpath.XPathEvaluationResult;
// import javax.xml.xpath.XPathException;
import javax.xml.xpath.XPathExpression;
import javax.xml.xpath.XPathExpressionException;
import javax.xml.xpath.XPathFactory;
//import javax.xml.xpath.XPathNodes;

import org.w3c.dom.Attr;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.NamedNodeMap;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
// import org.xml.sax.InputSource;
// import org.xml.sax.SAXException;

import wuwei.japan_core.cius.Binding;
// import wuwei.japan_core.cius.FileHandler;
import wuwei.japan_core.cius.ParsedNode;
// import wuwei.japan_core.utils.CSV;
// import wuwei.japan_core.utils.NamespaceResolver;

/**
 * 物理ファイルとの入出力とその為のデータ変換を制御するクラス
 */
public class XPathHandler {
	static String SYNTAX_BINDING             = null;
	static String XML_SKELTON                = null;
	static String JP_PINT_CSV                = "data/base/jp_pint_binding.csv";
	static String JP_PINT_XML_SKELTON        = "data/base/jp_pint_skeleton.xml";
	static String SME_CSV                    = "data/base/sme_binding.csv";
	static String SME_XML_SKELTON            = "data/base/sme_skeleton.xml";

	public static Document doc               = null;
	public static XPath xpath                = null;
	public static Element root               = null;
	public static String ROOT_ID             = "JBG-00";
	public static Integer ROOT_SEMSORT       = 1000;
	
	public static ArrayList<String> MULTIPLE_ID = new ArrayList<>();
	public static HashMap<String, String> nsURIMap = null;
			
	public static boolean TRACE = false;
	public static boolean DEBUG = false;
	static String PROCESSING    = null;
	static String IN_XML        = null;
	static String OUT_CSV       = null;
	
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
	
	public static Map<String/*id*/,	Binding> bindingDict             = new HashMap<>();
	public static TreeMap<Integer/*semSort*/, Binding> semBindingMap = new TreeMap<>();
	static TreeMap<Integer/*synSort*/, Binding> synBindingMap        = new TreeMap<>();
	
	public static TreeMap<Integer/*parent semSort*/, ArrayList<Integer/*child semSort*/>> semChildMap = new TreeMap<>();
	public static TreeMap<Integer/*parent synSort*/, ArrayList<Integer/*child synSort*/>> synChildMap = new TreeMap<>();
	public static TreeMap<Integer/*child semSort*/, Integer/*parent semSort*/> semParentMap = new TreeMap<>();
	public static TreeMap<Integer/*child synSort*/, Integer/*parent synSort*/> synParentMap = new TreeMap<>();
		
	public static TreeMap<Integer/*semSort*/, ParsedNode> nodeMap                           = new TreeMap<>();

	/**
 	 * The application's entry point
	 * @param args an array of command-line arguments for the application
	 * Debug for XPath
	 */
	public static void main(String[] args) {

	}
	
/**	private static int countChar(char ch, String str) {
		int count = 0;
		for (int i = 0; i < str.length(); i++) {
			if (str.charAt(i) == ch) {
				count++;
			}
		}
		return count;
	}
*/	
	/**
	 * 変換元のデジタルインボイスを読み込み、XML DOM及び名前空間を指定したXPathが使用できるように<br>
	 * XML DOM Document: doc, ルート要素(Element: root)及びxpath(XPath: xpath)を広域変数に設定する。
	 * 
	 * @param xmlfile 変換元のデジタルインボイス
	 */
	public static void parseInvoice(String xmlfile) {
		try {
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
		 	for (int i = 0; i < attributes.getLength(); i++) {
		 		Node attribute = attributes.item(i);
				String name = attribute.getNodeName();
				if ("xmlns".equals(name)) {
					name = "";
				} else {
					name = name.replace("xmlns:","");
				}
				String value = attribute.getNodeValue();
				nsURIMap.put(name, value);
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	/**
	 * semSortをキーにバインディング定義のXPathを検索し、それ使用してdocに定義されている要素を取り出して作成したTreeMapであるnodeMapを作成する。
	 * 
	 * @return nodeMap semSortをキーとするTreeMap&lt;Integer(semSort) ParsedNod&gt;
	 * 
	 */
	public static TreeMap<Integer, ParsedNode> parseDoc() {
		TreeMap<Integer/*semSort*/, ParsedNode> nodeMap = new TreeMap<>();
		for (Integer semSort: semBindingMap.keySet()) {
			Binding binding = semBindingMap.get(semSort);
			String xPath = binding.getXPath();
			List<Node> nodes = getXPath(root, xPath);
			if (null!=nodes) {
				if (nodes.size() > 0) {
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
	public static void parseSkeleton() {
		String skeleton = XML_SKELTON;
		try {
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
		 	root = (Element) doc.getChildNodes().item(0);
		 	nsURIMap = new HashMap<String,String>();
		 	NamedNodeMap attributes = root.getAttributes();
		 	for (int i = 0; i < attributes.getLength(); i++) {
		 		Node attribute = attributes.item(i);
				String name = attribute.getNodeName();
				if ("xmlns".equals(name)) {
					name = "";
				} else {
					name = name.replace("xmlns:","");
				}
				String value = attribute.getNodeValue();
				nsURIMap.put(name, value);
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	/**
	 * セマンティックモデルのidから、バインディング情報のsemSortを検索し、その値を用いてnodeMapから該当するNodeの値を取り出してnodeValueMapを作成する。
	 * 
	 * @param id セマンティックモデルのid
	 * @return nodeValueMap TreeMap&lt;Integer(順序番号), String(Nodeの値)&gt;
	 */
	public static TreeMap<Integer, String> getNodeValues(String id) {
		TreeMap<Integer, String> nodeValueMap = new TreeMap<>();
		Binding binding = bindingDict.get(id);
		Integer sort = binding.getSemSort();
		
		ParsedNode parsedNode = nodeMap.get(sort);
		
		List<Node> nodes = parsedNode.nodes;
		for (int i = 0; i < nodes.size(); i++) {
			Node node = nodes.get(i);
			String value = node.getTextContent().trim();
			nodeValueMap.put(i, value);
//			if (TRACE) System.out.println(i+" "+node.getNodeName()+" "+value);
		}
		return nodeValueMap;
	}
	
	/**
	 * 子要素のidからバインディング定義のXPathを取り出してそれを使用して親要素の下位にある子要素を探し出し、その結果をリストとして返す。
	 * 
	 * @param parent　親要素
	 * @param id　子要素のid
	 * @return nodes XPathに該当する要素のリスト List&lt;Node&gt; nodes
	 */
	public static List<Node> getElements(Element parent, String id) {
		Binding binding = (Binding) bindingDict.get(id);
		String xpath = binding.getXPath();
		xpath = xpath.replaceAll("/Invoice", "/*");
		xpath = xpath.replaceAll("/ubl:Invoice", "/*");
		if (null==parent) {
			if (TRACE) System.out.println(" (XPathHaldler) getElements parent null");
			return null;
		}
		if (id.toLowerCase().matches("^ibt-.+$")) {
			xpath += "/text()";
		}
		List<Node> nodes = getXPathNodes(parent, xpath);
		return nodes;
	}
	
	/**
	 * 親要素から指定されたXPathに該当する要素を探す。
	 * 
	 * @param parent 親要素
	 * @param xpath 親要素からのXPath
	 * @return
	 */
	public static List<Node> getXPath(Element parent, String xpath) {
		xpath = xpath.replaceAll("/(Invoice|ubl:Invoice)/", "/*/");
		if (null==parent) {
			if (TRACE) System.out.println(" (XPathHaldler) getXPath parent null");
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
	public static TreeMap<Integer, List<Node>> getChildren(Node parent, String parent_id) {
		TreeMap<Integer, List<Node>> childList = new TreeMap<>();	
		Binding binding = (Binding) bindingDict.get(parent_id);
		Integer parentSemSort = binding.getSemSort();
		String xpath = binding.getXPath();
		if (TRACE) System.out.println(" (XPathHandler) getChildren "+parent_id+"("+parentSemSort+") "+xpath);
//		if (parentSemSort-4060==0)
//			System.out.println(parentSemSort);

		ArrayList<Integer> children = semChildMap.get(parentSemSort);
		
		if (null!=children) {
			for (Integer sort: children) {
				Binding child_binding       = (Binding) semBindingMap.get(sort);
//				String childID              = child_binding.getID();
//				String child_datatype       = child_binding.getDatatype();
				String child_xpath          = child_binding.getXPath();
				String defaultValue         = child_binding.getDefaultValue();
				Set<String> additionalXPath = child_binding.getAdditionalXPath();
//				if (0==PROCESSING.indexOf("JP-PINT"))
//					child_xpath = checkChildXPath(xpath, childID, child_datatype, child_xpath);
				
				List<Node> nodes = getXPathNodes(parent, child_xpath);
				
				if (null!=nodes && nodes.size() > 0) {
					childList.put(sort, nodes);
				} else if (PROCESSING.indexOf("SYNTAX") > 0 && defaultValue.length() > 0) {
					// 未定義だが固定値が定義されている要素についてその値が定義されたNodeを返す。
					String element_name = child_xpath.substring(1+child_xpath.lastIndexOf('/'));
					String ns           = element_name.substring(0,element_name.indexOf(':'));
					String nsURI        = nsURIMap.get(ns);
					String qname        = element_name.substring(1+element_name.indexOf(':'));		
					Node child_node     = appendElementNS((Element) parent, nsURI, ns, qname, defaultValue, null);
					nodes = new ArrayList<>();
					nodes.add(child_node);
					childList.put(sort, nodes);
				} else if (null!=additionalXPath) {
					for(Iterator<String> iterator = additionalXPath.iterator(); iterator.hasNext();) {
						String additional_xpath     = iterator.next();
						List<Node> additional_nodes = getXPathNodes(parent, additional_xpath);
						if (additional_nodes.size() > 0)
							nodes = getXPathNodes(additional_nodes.get(0), child_xpath);
							if (nodes.size() > 0)
								childList.put(sort, nodes);						
					}
				}
			}
		}
		return childList;
	}

	/**
	 * PROCESSINGがJP-PINTのとき必要に応じて /text() を追加して、ルート要素からの子要素の相対的な XPath を求める。<br>
	 * Append /text() where necessary to find the relative XPath of child elements from the parent element.
	 * 
	 * @param xpath 親要素のXPath / XPath of the parent Node.
	 * @param childID 子要素のid /　id of the child Node.
	 * @param child_datatype 子要素のデータ型 / Data type of the child Node.
	 * @param child_xpath 子要素のXPath / XPath of the child Node.
	 * @return　更新された子要素のXPath / Replaced XPath of the child Node.
	 */
	private static String checkChildXPath(
			String xpath, 
			String childID, 
			String child_datatype, 
			String child_xpath ) {
		if (0==PROCESSING.indexOf("JP-PINT") && child_xpath.length() > 0) {
			if (! xpath.equals("/Invoice") && ! xpath.equals("/ubl:Invoice")) {
				child_xpath = child_xpath.replace(xpath, ".");
			}
			child_xpath = child_xpath.replace("/Invoice/", "/*/");
			child_xpath = child_xpath.replace("/ubl:Invoice/", "/*/");
			if (childID.toLowerCase().matches("^jbt-.*$") &&
					"cbc:".equals(child_xpath.substring(child_xpath.lastIndexOf('/')+1).substring(0,4)) &&
					! "String".equals(child_datatype)) {
				child_xpath += "/text()";
			}
		}
		return child_xpath;
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
			String xPath ) {
		if (null==xPath || 0==xPath.length())
			return null;
		XPathExpression expr = null;
		NodeList result;
		List<Node> nodeList = new ArrayList<>();
		try {		
			expr             = xpath.compile(xPath);
			result           = (NodeList) expr.evaluate(parent, XPathConstants.NODESET);
			nodeList         = asList(result); // https://stackoverflow.com/questions/50509663/convert-nodelist-to-list-in-java
			final int len    = nodeList.size();
			List<Node> nodes = new ArrayList<>();
			for (int i = 0; i < len; i++) {
			  final Node node = nodeList.get(i);
			  if (node.getNodeType() == Node.ELEMENT_NODE ||
					  node.getNodeType() == Node.TEXT_NODE ||
					  node.getNodeType() == Node.ATTRIBUTE_NODE) { // Ignore other node types.
				  nodes.add((Node) node);
			  }
			}
			return nodes;	
		} catch (XPathExpressionException e) {
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
	public static List<Node> asList(NodeList nodes) {
		return nodes.getLength()==0
				? Collections.<Node>emptyList()
				: new NodeListWrapper(nodes);
	}
	/**
	 * XML要素のNodeListをXML要素のリストList&lt;Node&gt;に変換するためのリストのラッパークラス.<br>
	 * asList()関数で使用する.
	 */
	static final class NodeListWrapper extends AbstractList<Node>	  
	implements RandomAccess {
		private final NodeList list;
		NodeListWrapper(NodeList l) {
		  list=l;
		}
		public Node get(int index) {
		  return list.item(index);
		}
		public int size() {
		  return list.getLength();
		}
	}
	
	/**
	 * XPathの文字列中に選択条件を指定するSelectorの文字列が含まれていればそのSelector文字列を返す.
	 * @param xPath XPathの文字列.
	 * @return 選択条件を指定するSelectorの文字列 [条件式]
	 */
	public static String extractSelector(String xPath) {
		int start = xPath.indexOf("[");
		int last = xPath.lastIndexOf("]");
		String selector = "";
		if (start >= 0) {
			selector = xPath.substring(start, last+1);
		}
		return selector;
	}
	
	/**
	 * XPathの文字列中に選択条件を指定するSelectorの文字列が含まれていればそのSelector文字列を削除したXPath文字列を返す.
	 * @param xPath XPathの文字列.
	 * @return 選択条件を指定するSelectorの文字列 [条件式] を削除したXPath文字列.
	 */
	public static String stripSelector(String path) {
		int start = path.indexOf("[");
		int last = path.lastIndexOf("]");
		if (start >= 0) {
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
	public static String resumeSelector(String strippedPath, String path) {
		String resumedPath = strippedPath;
		if (strippedPath.indexOf("cac:AllowanceCharge") >= 0) {
			int start = path.indexOf("[");
			int last = path.lastIndexOf("]");
			if (start >= 0) {
				String selector = path.substring(start, last+1);
				String hdr = strippedPath.substring(0, start);
				if (start+1 > strippedPath.length()) {
					resumedPath = hdr + selector;
				} else {
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
			HashMap<String, String> attrMap ) {
		if (null==parent) {
			if (TRACE) System.out.println(" (XPathHaldler) appendElementNS parent "+prefix+":"+qname+" is NULL return");
			return null;
		}
		try {
			if ("@".equals(qname.substring(0,1))) {
				String attrName = qname.substring(1, qname.length());
				
				Attr attribute = doc.createAttribute(attrName);
				
				attribute.setValue(value);
				parent.setAttributeNode(attribute);
				return parent;
			} else {
				
				Element element = doc.createElementNS(nsURI, qname);
				
				element.setPrefix(prefix); // Set the desired namespace and prefix
				if (value!="") {
					element.setTextContent(value);					
				}
				if (null!=attrMap) {
					for (Map.Entry<String, String> entry : attrMap.entrySet()) {
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
		} catch (Exception e) {
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
			IOException {
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
	 * 
	 * @throws FileNotFoundException
	 * @throws IOException
	 */
	public static void csvFileWrite(
			String filename, 
			String charset )
		throws
			FileNotFoundException,
			IOException {
		if (TRACE) System.out.println(" (XPathHandler) csvFileWrite " + filename + " " + charset);
		ArrayList<ArrayList<String>> data = new ArrayList<>();	
		// header
		data.add(header);
		// data
		for (ArrayList<String> row : tidyData) {
			data.add(row);
		}
		CSV.csvFileWrite(data,filename,charset,",",false);
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
			IOException {
		if (TRACE) System.out.println(" (XPathHandler) csvFileRead " + filename + " " + charset);
		FileInputStream fileInputStream = new FileInputStream(filename);
		
		ArrayList<ArrayList<String>> data = CSV.readFile(fileInputStream, charset);
		
		// header
		header = new ArrayList<String>();
		ArrayList<String> fields = data.get(0);
		int headerCount = fields.size();
		for (String field : fields) {
			header.add(field);
		}
		// data
		tidyData = new ArrayList<ArrayList<String>>();
		for (int i = 1; i < data.size(); i++) {
			fields = data.get(i);
			while (fields.size() < headerCount)
				fields.add(null);
			tidyData.add(fields);
		}
		fileInputStream.close();
	}

}