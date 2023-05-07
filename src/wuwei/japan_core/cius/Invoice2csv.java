package wuwei.japan_core.cius;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
//import java.util.Collections;
//import java.util.Comparator;
//import java.util.HashMap;
//import java.util.HashSet;
import java.util.List;
import java.util.Map;
//import java.util.Set;
import java.util.TreeMap;

import org.w3c.dom.NamedNodeMap;
import org.w3c.dom.Node;
//import org.w3c.dom.NodeList;

//import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ArrayNode;
import com.fasterxml.jackson.databind.node.ObjectNode;

//import wuwei.japan_core.utils.JSONHandler0;

/**
 * デジタルインボイスのXMLインスタンス文書を読み取り、Tidy dataを格納しているCSVファイルを出力する.
 */
public class Invoice2csv 
{
	static boolean TRACE         = false;	
	static boolean DEBUG         = false;	
	static String PROCESSING     = null;
	static String SYNTAX_BINDING = null;
	static String XML_SKELTON    = null;
	static String OUT_CSV        = null;
	static String IN_XML         = null;
	static String CHARSET        = "UTF-8";

	static String ROOT_ID;
	static Integer ROOT_SEMSORT;	
	static String DOCUMENT_CURRENCY_ID;      /*文書通貨コードのID*/
	static String TAX_CURRENCY_ID;           /*税通貨コードのID*/
	static String INVOICE_ID;                /*インボイス番号のID*/
	static int MIN_DOCUMENT_TOTAL;           /*semSort 文書ヘッダ合計金額*/
	static int MAX_DOCUMENT_TOTAL;           /*semSort*/
	static String TOTAL_TAX_ID;              /*文書ヘッダ合計税額のID*/
	static int TOTAL_TAX;                    /*semSort*/
	static String TOTAL_TAX_CURRENCY_TAX_ID; /*外貨建て請求書文書ヘッダ合計税額のID*/
	static int TOTAL_TAX_CURRENCY_TAX;       /*semSort*/
	static int MIN_TAX_BREAKDOWN;            /*semSort 文書ヘッダ課税分類*/
	static int MAX_TAX_BREAKDOWN;            /*semSort*/
	static int MIN_TAX_CURRENCY_BREAKDOWN;   /*semSort 文書ヘッダ外貨建て課税分類*/
	static int MAX_TAX_CURRENCY_BREAKDOWN;   /*semSort*/	
	static String DOCUMENT_CURRENCY = null;  /*文書通貨コード*/
	static String TAX_CURRENCY      = null;  /*税通貨コード*/
	static String INVOICE_NUMBER    = null;  /*インボイス番号*/
	static int COUNT_TAX_BREAKDOWN  = 0;
	
	/**
	 * 複数回繰り返され定義されているJBGグループ
	 */
	public static TreeMap<Integer/*semSort*/, String/*id*/> multipleMap = new TreeMap<>();

	/**
	 * Tidy dataテーブルの行を指定する索引データ
	 */
	static TreeMap<Integer/*sort*/,Integer/*seq*/> boughMap = new TreeMap<>();
	
	/**
	 * Tidy dataテーブル全体についてのTidy dataテーブルの行を指定する索引データのリスト
	 */
	static ArrayList<TreeMap<Integer, Integer>> boughMapList = new ArrayList<>();
	
	/**
	 * Tidy dataテーブル作成用の2次元リストの行
	 */
	static TreeMap<Integer, String> rowMap = new TreeMap<>();
	
	/**
	 * Tidy dataテーブル作成用の2次元リスト　Tidy dataテーブルは、FileHandler/tidyData
	 */
	static TreeMap<String, TreeMap<Integer, String>> rowMapList = new TreeMap<>();

	/**
	 * デジタルインボイス(XML)をCSVに変換する。
 	 * The application's entry point
	 * @param args an array of command-line arguments for the application
	 * last updated 2023-03-11
	 */
	public static void main(String[] args)
	{
		ROOT_ID                    = FileHandler.ROOT_ID;
		ROOT_SEMSORT               = FileHandler.ROOT_SEMSORT;	
		DOCUMENT_CURRENCY_ID       = FileHandler.DOCUMENT_CURRENCY_ID;       /*文書通貨コードのID*/
		TAX_CURRENCY_ID            = FileHandler.TAX_CURRENCY_ID;            /*税通貨コードのID*/
		INVOICE_ID                 = FileHandler.INVOICE_ID;                 /*インボイス番号のID*/	
		MIN_DOCUMENT_TOTAL         = FileHandler.MIN_DOCUMENT_TOTAL;         /*semSort 文書ヘッダ合計金額*/
		MAX_DOCUMENT_TOTAL         = FileHandler.MAX_DOCUMENT_TOTAL;         /*semSort*/
		TOTAL_TAX_ID               = FileHandler.TOTAL_TAX_ID;               /*文書ヘッダ合計税額のID*/
		TOTAL_TAX                  = FileHandler.TOTAL_TAX;                  /*semSort*/
		TOTAL_TAX_CURRENCY_TAX_ID  = FileHandler.TOTAL_TAX_CURRENCY_TAX_ID;  /*外貨建て請求書文書ヘッダ合計税額のID*/
		TOTAL_TAX_CURRENCY_TAX     = FileHandler.TOTAL_TAX_CURRENCY_TAX;     /*semSort*/
		MIN_TAX_BREAKDOWN          = FileHandler.MIN_TAX_BREAKDOWN;          /*semSort 文書ヘッダ課税分類*/
		MAX_TAX_BREAKDOWN          = FileHandler.MAX_TAX_BREAKDOWN;          /*semSort*/
		MIN_TAX_CURRENCY_BREAKDOWN = FileHandler.MIN_TAX_CURRENCY_BREAKDOWN; /*semSort 文書ヘッダ外貨建て課税分類*/
		MAX_TAX_CURRENCY_BREAKDOWN = FileHandler.MAX_TAX_CURRENCY_BREAKDOWN; /*semSort*/
		TRACE = false;
		DEBUG = false;
		if (0 == args.length) 
		{
			PROCESSING = "JP-PINT SEMANTICS";
		} else 
		{
			PROCESSING = args[0]+" SEMANTICS";
		}
		if (args.length <= 1) 
		{
			TRACE = true;
			DEBUG = true;
			if (0==PROCESSING.indexOf("JP-PINT")) {	
				IN_XML  = "data/xml/JP-PINT/Example.xml";
				OUT_CSV = "data/csv/JP-PINT/Example.csv";
			} else if (0==PROCESSING.indexOf("SME-COMMON")) {
				IN_XML  = "data/xml/SME-COMMON/Example.xml";				
				OUT_CSV = "data/csv/SME-COMMON/Example.csv";
			} else if (0==PROCESSING.indexOf("XBRL-GL")) {
				IN_XML  = "data/xml/XBRL-GL/0001-20090401-18-1-1-463.xml";				
				OUT_CSV = "data/csv/XBRL-GL/0001-20090401-18-1-1-463.csv";
			} else {
				return;
			}
		} else if (args.length >= 3) 
		{
			IN_XML     = args[1];	
			OUT_CSV    = args[2];
			if (4==args.length) {
				if (args[3].indexOf("T")>=0)
					TRACE = true;
				if (args[3].indexOf("D")>=0)
					DEBUG = true;
			}	
		}
		if (args.length>=5) 
		{
			SYNTAX_BINDING = args[3];
			XML_SKELTON    = args[4];
			FileHandler.SYNTAX_BINDING = SYNTAX_BINDING;
			FileHandler.XML_SKELTON    = XML_SKELTON;
			if (4==args.length) {
				if (args[5].indexOf("T")>=0)
					TRACE = true;
				if (args[5].indexOf("D")>=0)
					DEBUG = true;
			}	
		} else 
		{
			if (0==PROCESSING.indexOf("JP-PINT")) 
			{		
				FileHandler.SYNTAX_BINDING = FileHandler.JP_PINT_CSV;
				FileHandler.XML_SKELTON    = FileHandler.JP_PINT_XML_SKELTON;			
			} else if (0==PROCESSING.indexOf("SME-COMMON")) 
			{
				FileHandler.SYNTAX_BINDING = FileHandler.SME_CSV;
				FileHandler.XML_SKELTON    = FileHandler.SME_XML_SKELTON;
			} else 
			{
				return;
			}
		}
		FileHandler.PROCESSING = PROCESSING;
		FileHandler.TRACE      = TRACE;	
		FileHandler.DEBUG      = DEBUG;	
	
		processInvoice(IN_XML, OUT_CSV);
		
		System.out.println("** END ** Invoice2csv "+PROCESSING+" "+IN_XML+" "+OUT_CSV);
	}
	
	/**
	 * インボイスXMLファイルを読み込んで Tidy dataテーブルに展開し、CSVファイルに出力する.
	 * 
	 * @param in_xml デジタルインボイス（XMLインスタンス文書）.
	 * @param out_csv Tidy dataのCSV(RFC4180形式)ファイル.
	 */
	private static void processInvoice(String in_xml, String out_csv) 
	{
		if (TRACE) System.out.println("\n** processInvoice("+in_xml+", "+out_csv+")");
		
		boughMap     = new TreeMap<Integer/*sort*/,Integer/*seq*/>();
		boughMapList = new ArrayList<TreeMap<Integer, Integer>>();
		rowMap       = new TreeMap<Integer, String>();
		rowMapList   = new TreeMap<String, TreeMap<Integer, String>>();
	
		FileHandler.parseBinding();
		
		try 
		{
			FileHandler.parseInvoice(in_xml);
		} catch (Exception e) 
		{
			e.printStackTrace();
			return;
		}
		
		// 通貨コードをチェック
		for (Map.Entry<String, Binding> entry : FileHandler.bindingDict.entrySet()) 
		{
			Binding binding = entry.getValue();
			String id       = binding.getID();
			String xPath    = binding.getXPath();
			if (id.equals(DOCUMENT_CURRENCY_ID)) 
			{
				List<Node> nodes = FileHandler.getXPathNodes(FileHandler.root, xPath);
				if (nodes.size() > 0) 
				{
					DOCUMENT_CURRENCY = nodes.get(0).getTextContent();
					FileHandler.DOCUMENT_CURRENCY = DOCUMENT_CURRENCY;
				}
			} else if (id.equals(TAX_CURRENCY_ID)) 
			{
				List<Node> nodes = FileHandler.getXPathNodes(FileHandler.root, xPath);
				if (nodes.size() > 0) 
				{
					TAX_CURRENCY = nodes.get(0).getTextContent();
					FileHandler.TAX_CURRENCY = TAX_CURRENCY;
				}
			}
		}
		
		FileHandler.nodeMap = FileHandler.parseDoc();
		
		// 複数繰返しをチェック
		multipleMap = new TreeMap<>();
		for (Map.Entry<String, Binding> entry : FileHandler.bindingDict.entrySet()) 
		{
			Binding binding = entry.getValue();
			Integer sort    = binding.getSemSort();
			String id       = binding.getID();
			String card     = binding.getCard();
			if (id.toUpperCase().matches("^NC[0-9]+-NC[0-9]+$") &&
					card.matches("^.*n$") && //!occur.matches("^.*0$") &&
					isMultiple(sort)) 
			{
				multipleMap.put(sort, id);
			}
		}
		
		Binding binding = FileHandler.bindingDict.get(FileHandler.ROOT_ID);
		if (null==binding)
			System.out.println("FileHandler.ROOT_ID "+FileHandler.ROOT_ID+" is null.");
		Integer sort = binding.getSemSort();
		boughMap.put(sort, 0);
		boughMapList.add(boughMap);
		
		fillGroup(FileHandler.root, sort, boughMap);
		
		fillTable();

		try {
			FileHandler.csvFileWrite(FileHandler.tidyData, out_csv, CHARSET, ",", false);
		} catch (FileNotFoundException fnf) {
			System.out.println("* File Not Found Exception "+out_csv);
		} catch (IOException e) {
			e.printStackTrace();
		}
		
        String out_json = out_csv.substring(0, out_csv.lastIndexOf('.')) + ".json";
		try {
			fillJsonMeta(out_csv, out_json);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

		if (TRACE) System.out.println("-- END -- IN_XML "+in_xml);
	}
	
	/**
	 * This function creates a JSON object to store document, table template and table data.
	 * The resulting JSON object is written to a file in a human-readable format.
	 * 
	 * @param out_json the path and filename for the output JSON file
	 * @throws IOException if an I/O error occurs
	 */
	private static void fillJsonMeta(String out_csv, String out_json) throws IOException {
	    ArrayList<String> columns = FileHandler.header;

	    // Create ObjectMapper instance
	    ObjectMapper mapper = new ObjectMapper();

	    // Create documentInfo object
	    ObjectNode documentInfoObj = mapper.createObjectNode();
	    documentInfoObj.put("documentType", "https://xbrl.org/2021/xbrl-csv");

	    // Create namespaces object
	    ObjectNode namespacesObj = mapper.createObjectNode();
	    namespacesObj.put("core", "http://www.xbrl.jp/core-japan");
	    namespacesObj.put("ns0", "http://www.example.com");
	    namespacesObj.put("link", "http://www.xbrl.org/2003/linkbase");
	    namespacesObj.put("iso4217", "http://www.xbrl.org/2003/iso4217");
	    namespacesObj.put("xsi", "http://www.w3.org/2001/XMLSchema-instance");
	    namespacesObj.put("xbrli", "http://www.xbrl.org/2003/instance");
	    namespacesObj.put("xbrldi", "http://xbrl.org/2006/xbrldi");
	    namespacesObj.put("xlink", "http://www.w3.org/1999/xlink");
	    documentInfoObj.set("namespaces", namespacesObj);

	    // Create taxonomy array
	    ArrayNode taxonomyArr = mapper.createArrayNode();
	    taxonomyArr.add("../../xbrl/core.xsd");
	    documentInfoObj.set("taxonomy", taxonomyArr);

	    // Add documentInfo object to json object
	    ObjectNode json = mapper.createObjectNode();
	    json.set("documentInfo", documentInfoObj);

	    // Add tableTemplates object
	    ObjectNode tableTemplatesObj = mapper.createObjectNode();
	    ObjectNode coreObj = mapper.createObjectNode();
	    ObjectNode columnsObj = mapper.createObjectNode();
	    ArrayList<String> dimensions = new ArrayList<>();

	    TreeMap<String, ObjectNode> sortedColumns = new TreeMap<>();

	    for (String column : columns) {
	        String id = column;

	        if (id.startsWith("d_"))
	            id = id.substring(2);

	        Binding binding = FileHandler.bindingDict.get(id);
	        String datatype = binding.getDatatype();

	        ObjectNode columnObj = mapper.createObjectNode();

	        if (column.startsWith("d_")) {
	            columnsObj.set(column, mapper.createObjectNode());
	            dimensions.add(column);
	            sortedColumns.put(column, (ObjectNode) columnsObj.get(column));
	        } else {
	            String conceptName = column;
	            ObjectNode dimensionsObj = mapper.createObjectNode();
	            dimensionsObj.put("concept", "core:" + conceptName);

	            if (datatype.equals("Amount") || datatype.equals("Unit Price Amount")) {
	                dimensionsObj.put("unit", "iso4217:JPY");
	            }

	            columnObj.set("dimensions", dimensionsObj);
	            columnsObj.set(column, columnObj);
	            sortedColumns.put(column, columnObj);
	        }
	    }

	    // Create a new ObjectNode from the sorted TreeMap
	    ObjectNode sortedColumnsObj = mapper.createObjectNode();
	    sortedColumns.forEach(sortedColumnsObj::set);
	    coreObj.set("columns", sortedColumnsObj);

	    // Add sorted columns object to coreObj
	    coreObj.set("columns", mapper.readTree(columnsObj.toString()));

	    ObjectNode dimensionsObj = mapper.createObjectNode();

	    for (String dimension : dimensions) {
	        dimensionsObj.put("core:" + dimension, "$" + dimension);
	    }

	    dimensionsObj.put("period", "2023-11-01T00:00:00");
	    dimensionsObj.put("entity", "ns0:Example co.");
	    coreObj.set("dimensions", dimensionsObj);
	    tableTemplatesObj.set("core_japan_template", coreObj);
	    json.set("tableTemplates", tableTemplatesObj);
	    
	    // Add tables object
	    ObjectNode tablesObj = mapper.createObjectNode();
	    ObjectNode coreTablesObj = mapper.createObjectNode();
	    coreTablesObj.put("template", "core_japan_template");
	    Path csvPath = Paths.get(out_csv);
        Path jsonPath = Paths.get(out_json);        
        Path relativePath = jsonPath.relativize(csvPath);
        String relative_path = relativePath.toString().substring(3);
	    coreTablesObj.put("url", relative_path);
	    tablesObj.set("core_japan_table", coreTablesObj);
	    
	    json.set("tables", tablesObj);

	    // convert the JSON object to a string and print it
	    String jsonString = mapper.writerWithDefaultPrettyPrinter().writeValueAsString(json);
	    if (TRACE) System.out.println(jsonString);

	    // write the JSON object to a file
	    try {
	        mapper.writerWithDefaultPrettyPrinter().writeValue(new File(out_json), json);
	        if (TRACE) System.out.println("JSON object written to " + out_json);
	    } catch (IOException e) {
	        e.printStackTrace();
	    }
	}
	
	/**
	 * Tidy dataテーブル作成用の2次元リストrowMapListをTidy dataテーブル(FileHandler/tidyData)に変換する.
	 */
	private static void fillTable() 
	{
		FileHandler.tidyData = new ArrayList<ArrayList<String>>();		
		FileHandler.header.add(FileHandler.ROOT_ID);	
		// bough
		for (Map.Entry<Integer,String> multipleEntry : multipleMap.entrySet()) 
		{
			String multipleID       = multipleEntry.getValue();
			Binding multipleBinding = FileHandler.bindingDict.get(multipleID);
			if (multipleID.toUpperCase().matches("^NC[0-9]+-NC[0-9]+$") && multipleBinding.isUsed()) 
			{
				FileHandler.header.add(multipleID);
			}
		}
		// data
		for (Map.Entry<Integer,Binding> dataEntry : FileHandler.semBindingMap.entrySet()) 
		{
			Integer dataSort    = dataEntry.getKey();
			Binding dataBinding = dataEntry.getValue();
			String dataID       = dataBinding.getID();
			if (1!=dataSort &&
					dataID.toUpperCase().matches("^NC[0-9]+-[0-9]+$") &&
					dataBinding.isUsed() &&
					! FileHandler.header.contains(dataID)) 
			{
				FileHandler.header.add(dataID);
			}
		}		
		FileHandler.tidyData.add(FileHandler.header);
		for (Map.Entry<String, TreeMap<Integer, String>> entryRow : rowMapList.entrySet()) 
		{
			ArrayList<String> record = new ArrayList<>();
			for (int i = 0; i < FileHandler.header.size(); i++) 
			{
				record.add("");
			}
			// bough
			String rowMapKey = entryRow.getKey();
			String[] boughs = rowMapKey.split(" ");
			for (String bough : boughs) 
			{
				String[] index       = bough.split("=");
				Integer boughSort    = Integer.parseInt(index[0]);
				Binding boughBinding = FileHandler.semBindingMap.get(boughSort);
				if (null!=boughBinding) 
				{
					String boughID  = boughBinding.getID();
					String boughSeq = index[1];
					int boughIndex  = FileHandler.header.indexOf(boughID);
					if (boughIndex!=-1) 
					{
						record.set(boughIndex, boughSeq);
					} else 
					{
						if (TRACE) System.out.println("xx "+boughID+" NOT FOUND in the header");
					}
				}
			}
			// data
			TreeMap<Integer, String> rowMap = entryRow.getValue();
			for (Map.Entry<Integer, String> entry : rowMap.entrySet()) 
			{
				Integer sort    = entry.getKey();
				String value    = entry.getValue();
				Binding binding = FileHandler.semBindingMap.get(sort);
				String id       = binding.getID();
				int dataIndex   = FileHandler.header.indexOf(id);
				if (dataIndex >= 0) 
				{
					record.set(dataIndex, value);
				} else 
				{
					if (TRACE) System.out.println(id+" NOT FOUND in the header");
				}
			}
			FileHandler.tidyData.add(record);
		}
		
		int row_size = FileHandler.tidyData.size();
		int col_size = FileHandler.tidyData.get(0).size();
		ArrayList<Boolean> usedList = new ArrayList<>();        
        for (int i = 0; i < col_size; i++) {
            usedList.add(false);
        }
		for (int y = 1; y < row_size; y++) 
		{
			for (int x = 0; x < col_size; x++) 
			{
				String data = FileHandler.tidyData.get(y).get(x);
				if (null!=data && data.length() > 0)
					usedList.set(x, true);
			}
		}
		int countUsed = 0;
        for (Boolean b : usedList) {
            if (b) {
            	countUsed++;
            }
        }
    	ArrayList<ArrayList<String>> revisedData = new ArrayList<>(row_size);
		for (int y = 0; y < row_size; y++) 
		{
			ArrayList<String> row = new ArrayList<>(countUsed);
			for (int x = 0; x < col_size; x++) 
			{
				String data = FileHandler.tidyData.get(y).get(x);
				if (usedList.get(x))
				{
					if (0==y && data.toUpperCase().matches("^(NC00|NC[0-9]+-NC[0-9]+)$"))
						data = "d_"+data;
					row.add(data);
				}
			}
			revisedData.add(row);
		}
		
		FileHandler.tidyData = revisedData;
		FileHandler.header   = revisedData.get(0);

		if (TRACE) System.out.println("* FileHandler.tidyData");
		for (int y = 0; y < row_size; y++) 
		{
			ArrayList<String> row = new ArrayList<>();
			row = FileHandler.tidyData.get(y);
			if (TRACE) System.out.println(row.toString());
		}
		
		if (TRACE) System.out.println("-- End -- fillTable()");
	}

	/**
	 * 見つかった要素を Tidy dataテーブル作成用の2次元リストrowMapListに登録する.
	 * 
	 * @param semSort セマンティックモデルのセマンティックソート番号
	 * @param value 要素の値
	 * @param boughMap Tidy dataテーブルの行を指定する索引データ
	 */
	private static void fillData (
			Integer semSort, 
			String value, 
			TreeMap<Integer, Integer> boughMap ) 
	{
		Binding binding     = (Binding) FileHandler.semBindingMap.get(semSort);
		String id           = binding.getID();
		String businessTerm = binding.getBT();
		binding.setUsed(true);
		value = value.trim();
		if (TRACE) 
			System.out.println("  fillData boughMap="+boughMap.toString()+" "+id+"("+semSort+") "+businessTerm+" = "+value);
		String rowMapKey = "";
		for (Map.Entry<Integer, Integer> entry : boughMap.entrySet()) 
		{
			Integer boughSort = entry.getKey();
			Integer seq       = entry.getValue();
			rowMapKey += (boughSort+"="+seq+" ");
		}
		rowMap = new TreeMap<>();
		rowMapKey = rowMapKey.trim();
		if (rowMapList.containsKey(rowMapKey)) 
		{
			rowMap = rowMapList.get(rowMapKey);
		}
		rowMap.put(semSort, value);
		rowMapList.put(rowMapKey, rowMap);
		if (INVOICE_ID.equals(id))
			INVOICE_NUMBER = value;
		else if (DOCUMENT_CURRENCY_ID.equals(id))
			DOCUMENT_CURRENCY = value;
		else if (TAX_CURRENCY_ID.equals(id))
			TAX_CURRENCY = value;
	}
	
	/**
	 * デジタルインボイスのXMLインスタンス文書を読み込み、セマンティックモデルの階層定義に従って親要素から子要素のXPathを使用して探し出し、
	 * その値をTidy data定義用の2次元リストに設定する。
	 * 
	 * @param parent 親のXML要素
	 * @param sort モデル定義における親要素のソート番号
	 * @param boughMap　Tidy dataテーブルの行を指定する索引データ
	 */
	private static void fillGroup (
			Node parent, 
			Integer sort, 
			TreeMap<Integer, Integer> boughMap ) 
	{
		Binding binding     = FileHandler.semBindingMap.get(sort);
		String id           = binding.getID();
		String businessTerm = binding.getBT();
		rowMap = new TreeMap<Integer, String>();		

		if (TRACE)
			System.out.println("FileHandler.getChildren "+id);	

		TreeMap<Integer, List<Node>> childList = FileHandler.getChildren(parent, id);
		
		if (TRACE) 
		{
			System.out.print("- 0 fillGroup boughMap="+boughMap.toString()+" "+id+"("+sort+") "+businessTerm);
			if (0==childList.size()) 
			{
				System.out.println(" is Empty");
				return;
			} else 
			{
				System.out.println("");
			}
		}
   	
		for (Integer childSort : childList.keySet()) 
		{ // childList includes both #text and @attribute
			Binding childBinding     = (Binding) FileHandler.semBindingMap.get(childSort);
			String childID           = childBinding.getID();
			String childBusinessTerm = childBinding.getBT();
			String childXPath        = childBinding.getXPath();
			int childLevel           = childBinding.getLevel();

			if (TRACE) System.out.println("- fillGroup "+childID+"("+childSort+") "+childBusinessTerm+" XPath = "+FileHandler.getShortPath(childXPath));

			List<Node> children = childList.get(childSort);
			
			int countChildren = children.size();
			if (countChildren > 0) 
			{
				if (countChildren > 1 && children.get(0).getNodeName().equals(children.get(1).getNodeName()))
				{
					if (childID.toUpperCase().matches("^NC[0-9]+-[0-9]+$"))
					{
						for (int i = 0; i < countChildren; i++) 
						{
							fillMultipleBusinessTerm(boughMap, sort, childSort, children, i);
						}
					} else if (childID.toUpperCase().matches("^NC[0-9]+-NC[0-9]+$"))
					{
						for (int i = 0; i < countChildren; i++) 
						{
							fillMultipleBusinessTermGroup(boughMap, sort, childSort, children, i);
						}
					}						
				}
				for (int i = 0; i < countChildren; i++) 
				{
					Node child           = children.get(i);
					String childNodeName = child.getNodeName();
					String value         = "";
					if (0==PROCESSING.indexOf("JP-PINT") && childNodeName.indexOf("cac:")>=0)
						System.out.println(childNodeName);
					else
						value = child.getTextContent().trim();					
					if (! "Invoice".equals(childNodeName) && childNodeName.indexOf(":")<0)
					{
						fillData(childSort, value, boughMap); // @attribute
						
					} else if (null!=child && null != value && value.length() > 0 && childID.toUpperCase().matches("^NC[0-9]+-[0-9]+$")) 
					{
						if (TRACE) 
							System.out.println("* 1 fillGroup - fillData child["+i+"]"+childID+"("+childSort+") "+childNodeName+" = "+value);

						fillData(childSort, value, boughMap); // #text	
						
						if (FileHandler.semChildMap.containsKey(childSort)) 
						{
							ArrayList<Integer> grandchildren = FileHandler.semChildMap.get(childSort);
							NamedNodeMap attributes = child.getAttributes();
							for (Integer grandchildSort : grandchildren) 
							{
								fillGrandChildren(boughMap, childSort, i, childNodeName, attributes, grandchildSort);
							}
						}						
					} else 
					{
						boolean is_multiple = isMultiple(childSort);
						if (is_multiple && countChildren > 1) 
						{
							fillNewGroup(boughMap, sort, childSort, /*childID, childBusinessTerm, childLevel,*/	countChildren, i, child);
						} else
						{
							if (TRACE) 
								System.out.println("* fillGroup "+ businessTerm+" -> level="+childLevel+" "+childID+"("+childSort+") "+childBusinessTerm+
									"\n    boughMapList="+boughMapList.toString()+"\n    boughMap"+boughMap.toString());
							fillGroup(child, childSort, boughMap);
						}
					}
				}
			}
		}
	}

	/**
	 * Tidy dataテーブルに新たな行を追加する
	 * 
	 * @param boughMap Tidy dataテーブルの行を指定する索引データ
	 * @param sort モデル定義における親要素のソート番号 
	 * @param childSort モデル定義における子要素のソート番号
	 * @param countChildren 親要素が含む子要素の数 
	 * @param i 処理中の子要素の順序番号
	 * @param child 子要素
	 */
	private static void fillNewGroup(
			TreeMap<Integer, Integer> boughMap, 
			Integer sort,
			Integer childSort,
			Integer countChildren, 
			int i, 
			Node child) 
	{
		Integer lastkey          = boughMap.lastKey();
		Integer lastvalue        = boughMap.get(lastkey);
		Binding binding          = FileHandler.semBindingMap.get(sort);
		String businessTerm      = binding.getBT();
		Binding childBinding     = (Binding) FileHandler.semBindingMap.get(childSort);
		String childID           = childBinding.getID();
		String childBusinessTerm = childBinding.getBT();
		int childLevel           = childBinding.getLevel();
		
		@SuppressWarnings("unchecked")
		TreeMap<Integer,Integer> boughMap1 = (TreeMap<Integer, Integer>) boughMap.clone();
		if (TRACE) 
			System.out.print("    boughMap lastKey="+lastkey+" child is multiple level="+childLevel);
		if (childSort != lastkey) 
		{
			if (boughMap1.size() < childLevel) 
			{
				boughMap1.put(childSort, i);
			} else 
			{
				boughMap1.pollLastEntry();
				boughMap1.put(childSort, i);
				boughMapList.remove(boughMapList.size() - 1);
			}
		} else if (countChildren > 1) 
		{
			Integer lastvalue1 = lastvalue + 1;
			boughMap1.put(lastkey, lastvalue1);
		}
		if (boughMapList.size() >= childLevel)
			boughMapList.remove(boughMapList.size() - 1);
		boughMapList.add(boughMap1);
		if (TRACE) 
			System.out.println("\n    UPDATED boughMapList="+boughMapList.toString()+"\n    boughMap1="+boughMap1.toString());
		if (TRACE) 
			System.out.println("* fillGroup "+ businessTerm+" -> level="+childLevel+" "+childID+"("+childSort+") "+childBusinessTerm+
				"\n    boughMapList="+boughMapList.toString()+"\n    boughMap"+boughMap1.toString());
		fillGroup(child, childSort, boughMap1);
	}

	/**
	 * 子要素が含む孫要素を Tidy data テーブルに追加する。
	 * 
	 * @param boughMap Tidy dataテーブルの行を指定する索引データ
	 * @param sort モデル定義における親要素のソート番号
	 * @param childSort モデル定義における子要素のソート番号
	 * @param i
	 * @param childNodeName
	 * @param attributes
	 * @param grandchildSort
	 */
	private static void fillGrandChildren(
			TreeMap<Integer, Integer> boughMap, 
			Integer      childSort,
			int          i, 
			String       childNodeName,
			NamedNodeMap attributes, 
			Integer      grandchildSort) 
	{
		Integer lastKey           = boughMap.lastKey();
		Integer lastID            = boughMap.get(lastKey);
		Binding childBinding      = (Binding) FileHandler.semBindingMap.get(childSort);
		String childID            = childBinding.getID();
		String childBusinessTerm  = childBinding.getBT();
		int childLevel            = childBinding.getLevel();
		Binding grandchildBinding = (Binding) FileHandler.semBindingMap.get(grandchildSort);
		String grandchildID       = grandchildBinding.getID();
		String grandchildBT       = grandchildBinding.getBT();
		String grandchildXPath    = grandchildBinding.getXPath();
		String attrName           = grandchildXPath.substring(2+grandchildXPath.lastIndexOf("/@"));
		if (attributes.getLength() > 0) 
		{
			Node attribute = attributes.getNamedItem(attrName);
			if (null!=attribute) 
			{
				String grandchildValue = attribute.getNodeValue();
				if (TRACE) 
					System.out.print(
							"* 2 fillGroup - fillData boughMap"+boughMap.toString()+"child "+childNodeName+" "+childID+
							" grandchild("+grandchildSort+") "+grandchildID+" level="+childLevel+" "+ childBusinessTerm+"->"+grandchildBT+
							"\n    @"+attrName+"("+grandchildSort+") = "+grandchildValue);
				fillData(grandchildSort, grandchildValue, boughMap);
			}
		} else 
		{									
			ParsedNode parsedNode      = FileHandler.nodeMap.get(grandchildSort);
			List<Node> grandchildNodes = parsedNode.nodes;
			for (int j = 0; j < grandchildNodes.size(); j++) 
			{
				if (0==i-lastID) 
				{
					Node grandchild           = grandchildNodes.get(lastID);
					String grandchildNodeName = grandchild.getNodeName();
					String grandchildValue    = grandchild.getTextContent().trim();
					if (TRACE) 
						System.out.println(
								"* 2 fillGroup - fillData boughMap"+boughMap.toString()+"child "+childNodeName+" "+childID+
								" grandchild("+grandchildSort+") "+grandchildID+" level="+childLevel+" "+ childBusinessTerm+"->"+grandchildBT+
								"\n    grand child["+lastKey+"] "+grandchildNodeName+"="+grandchildValue);		
					fillData(grandchildSort, grandchildValue, boughMap);
				}
			}
		}
	}

	/**
	 * Tidy data テーブルに親要素が含むXPathで見つかった複数の子要素を追加する。
	 * 
	 * @param boughMap Tidy dataテーブルの行を指定する索引データ
	 * @param sort モデル定義における親要素のソート番号
	 * @param childSort モデル定義における子要素のソート番号
	 * @param children
	 * @param i
	 */
	private static void fillMultipleBusinessTermGroup(
			TreeMap<Integer, Integer> boughMap, 
			Integer sort, 
			Integer childSort,
			List<Node> children, 
			int i) 
	{
		Binding binding          = FileHandler.semBindingMap.get(sort);
		String businessTerm      = binding.getBT();
		Binding childBinding     = (Binding) FileHandler.semBindingMap.get(childSort);
		String childID           = childBinding.getID();
		String childBusinessTerm = childBinding.getBT();
		int childLevel           = childBinding.getLevel();
		int countChildren        = children.size();
		Node child               = children.get(i);
		@SuppressWarnings("unchecked")
		TreeMap<Integer,Integer> boughMap1 = (TreeMap<Integer, Integer>) boughMap.clone();
		Integer lastkey          = boughMap1.lastKey();
		Integer lastvalue        = boughMap1.get(lastkey);
		if (TRACE) 
			System.out.print("    boughMap lastKey="+lastkey+" child is multiple level="+childLevel);
		if (childSort != lastkey) 
		{
			if (boughMap1.size() < childLevel) 
			{
				boughMap1.put(childSort, i);
			} else 
			{
				boughMap1.pollLastEntry();
				boughMap1.put(childSort, i);
				boughMapList.remove(boughMapList.size() - 1);
			}
		} else if (countChildren > 1) 
		{
			Integer lastvalue1 = lastvalue + 1;
			boughMap1.put(lastkey, lastvalue1);
		}
		if (boughMapList.size() >= childLevel)
			boughMapList.remove(boughMapList.size() - 1);
		boughMapList.add(boughMap1);							
		if (TRACE) 
			System.out.println("\n    UPDATED boughMapList="+boughMapList.toString()+" boughMap="+boughMap1.toString()+
					"\n* fillGroup "+ businessTerm+" -> level="+childLevel+" "+childID+"("+childSort+") "+childBusinessTerm);
		fillGroup(child, childSort, boughMap1);
	}

	/**
	 * Tidy data テーブルに親要素が含むXPathで見つかった複数の子要素を追加する。
	 * 
	 * @param boughMap Tidy dataテーブルの行を指定する索引データ
	 * @param sort モデル定義における親要素のソート番号
	 * @param childSort モデル定義における子要素のソート番号
	 * @param children
	 * @param i
	 */
	private static void fillMultipleBusinessTerm(
			TreeMap<Integer, Integer> boughMap, 
			Integer    sort, 
			Integer    childSort, 
			List<Node> children, 
			int        i) 
	{
		Integer lastKey          = boughMap.lastKey();
		Binding binding          = FileHandler.semBindingMap.get(sort);
		String businessTerm      = binding.getBT();
		Binding childBinding     = (Binding) FileHandler.semBindingMap.get(childSort);
		String childID           = childBinding.getID();
		String childBusinessTerm = childBinding.getBT();
		int childLevel           = childBinding.getLevel();
		Node child               = children.get(i);
		String value             = child.getTextContent().trim();	
		@SuppressWarnings("unchecked")
		TreeMap<Integer,Integer> boughMap1 = (TreeMap<Integer, Integer>) boughMap.clone();
		Integer lastkey          = boughMap1.lastKey();
		Integer lastvalue        = boughMap1.get(lastkey);
		if (TRACE) 
			System.out.print("    boughMap lastKey="+lastkey+" child is multiple level="+childLevel);
		if (i != lastvalue)
		{
			boughMap1.pollLastEntry();
			boughMap1.put(lastKey, i);
			boughMapList.remove(boughMapList.size() - 1);
			boughMapList.add(boughMap1);
		}
		if (TRACE) 
			System.out.println("\n    UPDATED boughMapList="+boughMapList.toString()+
				"\n* fillGroup "+ businessTerm+" -> level="+childLevel+" "+childID+"("+childSort+") "+childBusinessTerm);
		fillData(childSort, value, boughMap1);
	}

	/**
	 * セマンティックソート番号 semSortで指定された要素がXML DOM Documentに複数あるか判定する.<br>
	 * なお、FileHandler.MULTIPLE_IDで指定された要素も、複数と判定する.
	 * 
	 * @param semSort セマンティックソート番号.
	 * 
	 * @return multiple 複数であればtrue.　存在しないか1件しかなければfalse.
	 */
	@SuppressWarnings("unlikely-arg-type")
	private static boolean isMultiple(Integer semSort) 
	{
		boolean multiple  = false;
		Binding binding   = FileHandler.semBindingMap.get(semSort);
		String id         = binding.getID();
		String xPath      = binding.getXPath();
		List<Node> founds = FileHandler.getXPath(FileHandler.root, xPath);
		if (null!=founds) 
		{
			if (xPath.indexOf("true") > 0 || xPath.indexOf("false") > 0 || founds.size() > 1) 
			{
				multiple = true;
			}
		} else if (Arrays.asList(FileHandler.MULTIPLE_ID).contains(id.toLowerCase())) 
		{
			multiple = true;
		}
		return multiple;
	}

}