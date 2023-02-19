package wuwei.japan_core.cius;

import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.TreeMap;

import javax.xml.transform.TransformerException;

import org.w3c.dom.Element;
import org.w3c.dom.Node;

import wuwei.japan_core.utils.WriteXmlDom;

/**
 * Tidy dataを格納しているCSVファイルを読み取りセマンティックモデル定義と構文バインディング定義からXMLインスタンス文書を出力する.
 */
public class Csv2invoice {
    static boolean TRACE = true;
    
    static String PROCESSING        = null;

    static String TERMINAL_ELEMENTS = null;
	static String OUT_XML           = null;
	static String IN_CSV            = null;
	static String CHARSET           = "UTF-8";
	
	static String DOCUMENT_CURRENCY_CODE_ID = "JBT-091"; /*文書通貨コードのID*/
	static String TAX_CURRENCY_CODE_ID      = "JBT-090"; /*税通貨コードnoID*/
	static String DOCUMENT_CURRENCY         = null; /*文書通貨コード*/
	static String TAX_CURRENCY              = null; /*税通貨コード*/
	
	/**
	 * 終端XML要素
	 */
	public static ArrayList<String> terminalElements = new ArrayList<>();
	
    // CSV records
	/**
	 * Tidy dataの行データ.
	 */
    static TreeMap<Integer, String> rowMap = new TreeMap<>();
    
    /**
     * Tidy dataのテーブルデータ
     */
    static TreeMap<String, TreeMap<Integer, String>> rowMapList = new TreeMap<>();
 	
    /**
     * tidy data (Node定義)テーブルrowMapListをXMLスキーマで定義されたsyntax sort順にXML要素定義するために、縦横変換する。<br>
     * その際に要素の定義データを一時保存するために使用するクラス。
     * 
     * @param seq 要素が定義されたTidy dataの行に対応する索引(bough)の順序番号.
     * @param sort 要素が定義されたTidy dataの行に対応する索引(bough)に対応するグループ要素のセマンティックソート番号.
     * @param id この要素のid.
     * @param xPath この要素のXPath.
     * @param value この要素の値.
     * @param attributes この要素の属性.
     */
    static class DataValue 
    {
    	public Integer seq;
 		public Integer sort;
 		public String  id;
 		public String  xPath;
 		public String  value;
 		public HashMap<String,String> attributes;
 		// constructor
 		DataValue(
 				Integer seq, 
 				Integer sort, 
 				String id,
 				String xPath, 
 				String value, 
 				HashMap<String,String> attributes) 
 		{
 			this.seq = seq;
 			this.sort = sort;
 			this.id = id;
 			this.xPath = xPath;
 			this.value = value;
 			this.attributes = attributes;
 		}
    }
    
 	/**
 	 * インボイス通貨及び税会計通貨を保持するクラス.
 	 * 
 	 * @param xPath XML要素のXPath
 	 * @param value XML要素の値
 	 *
 	 */
    static class PathValue 
 	{
 		public String xPath;
 		public String value;

 		PathValue(String a, String b) {
 			xPath = a;
 			value = b;
 		}
 	}
    /**
     * インボイスで使用される通貨コード.
     */
 	static PathValue documentCurrencyCode = new PathValue(null, null);
 	/**
 	 * インボイスに関する税会計で使用される通貨コード.
 	 */
 	static PathValue taxCurrencyCode = new PathValue(null, null);
   
 	/**
 	 * mainでは変換処理を単体でテストする.
 	 * 
 	 * @param args
 	 */
	public static void main(String[] args) 
	{
		PROCESSING              = "SME COMMON";
		FileHandler.PROCESSING  = PROCESSING;
		FileHandler.CORE_CSV    = FileHandler.SME_CSV;
		FileHandler.XML_SKELTON = FileHandler.SME_XML_SKELTON;

//		FileHandler.CORE_CSV = FileHandler.JP_PINT_CSV;
//		FileHandler.XML_SKELTON = FileHandler.JP_PINT_XML_SKELTON;
		
		processCSV("data/csv/Example1.csv", "data/xml/Example1_SME.xml");
//		processCSV("data/csv/Example1.csv", "data/xml/Example1_PINT.xml");
//		processCSV("data/csv/Example2-TaxAcctCur.csv","data/xml/Example2-TaxAcctCur_out.xml");
//		processCSV("data/csv/Example3-0.csv","data/xml/Example3-0_out.xml");
//		processCSV("data/csv/Example3-SumInv1.csv","data/xml/Example3-SumInv1_out.xml");
//		processCSV("data/csv/Example4-SumInv2.xsv","data/xml/Example4-SumInv2_out.xml");
//		processCSV("data/csv/Example5-AllowanceCharge0.csv","data/xml/Example5-AllowanceCharge0_out.xml");
//		processCSV("data/csv/Example5-AllowanceCharge.csv","data/xml/Example5-AllowanceCharge_out.xml");
//		processCSV("data/csv/Example6-CorrInv.csv","data/xml/Example6-CorrInv_out.xml");
//		processCSV("data/csv/Example7-Return.Quan.csv","data/xml/Example7-Return.Quan_out.xml");
//		processCSV("data/csv/Example8-Return.ItPr.csv","data/xml/Example8-Return.ItPr_out.xml");
		if (TRACE) System.out.println("** END Csv2Invoice **");
	}
	
	/**
	 * Tidy dataのCSVファイルをデジタルインボイスのXMLインスタンス文書に変換する.
	 * 
	 * @param in_csv 入力するTidy dataのCSVファイル.
	 * @param out_xml 出力するデジタルインボイスのXMLインスタンス文書.
	 */
	public static void processCSV(String in_csv, String out_xml) 
	{	
		FileHandler.parseBinding();		
			
		try {
			if ("SME COMMON"==PROCESSING)
				terminalElements = new ArrayList<String>(Arrays.asList("@unitCode","udt:DateTimeString","ram:AccountName","ram:ActualAmount","ram:AdditionalReferencedCIReferencedDocument","ram:AllowanceTotalAmount","ram:AttachmentBinaryObject","ram:BasisAmount","ram:BasisQuantity","ram:BilledQuantity","ram:BuyerAssignedID","ram:BuyerOrderReferencedCIReferencedDocument","ram:CalculatedAmount","ram:CalculatedRate","ram:CalculationMethodCode","ram:CalculationPercent","ram:CardholderName","ram:CategoryCode","ram:CategoryName","ram:ChannelCode","ram:ChargeAmount","ram:ChargeIndicator","ram:ChargeTotalAmount","ram:CompleteNumber","ram:Content","ram:ConversionRate","ram:CountryID","ram:CurrencyCode","ram:DepartmentName","ram:Description","ram:DirectionCode","ram:DuePayableAmount","ram:FileName","ram:GlobalID","ram:GrandTotalAmount","ram:GrossLineTotalAmount","ram:ID","ram:IncludingTaxesLineTotalAmount","ram:Information","ram:InstructedAmount","ram:InvoiceCurrencyCode","ram:InvoiceCurrencyCode","ram:IssuerAssignedID","ram:IssuingCompanyName","ram:JapanFinancialInstitutionCommonID","ram:LineID","ram:LineOne","ram:LineThree","ram:LineTwo","ram:LocalTaxSystemID","ram:ManufacturerAssignedID","ram:MIMECode","ram:Name","ram:NetIncludingTaxesLineTotalAmount","ram:NetLineTotalAmount","ram:PackageQuantity","ram:PaidAmount","ram:PaymentCurrencyCode","ram:PerPackageUnitQuantity","ram:PersonID","ram:PersonName","ram:PostcodeCode","ram:PreviousRevisionID","ram:ProductGroupID","ram:ProductUnitQuantity","ram:ProprietaryID","ram:PurposeCode","ram:RateApplicablePercent","ram:Reason","ram:ReasonCode","ram:ReferenceTypeCode","ram:RegisteredID","ram:RevisionID","ram:SellerAssignedID","ram:SourceCurrencyCode","ram:SpecifiedTransactionID","ram:Subject","ram:SubordinateLineID","ram:SubtypeCode","ram:TargetCurrencyCode","ram:TaxBasisTotalAmount","ram:TaxCurrencyCode","ram:TaxCurrencyCode","ram:TaxTotalAmount","ram:TotalPrepaidAmount","ram:TypeCode","ram:URIID","ram:Value"));
			FileHandler.csvFileRead(in_csv, CHARSET);
		} catch (FileNotFoundException e) {
			System.out.println("File not found "+in_csv);
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		FileHandler.parseSkeleton();
					
		rowMapList = new TreeMap<>();
		
		if (TRACE) System.out.println("- processCSV FileHandler.tidyData record");
		
		for (ArrayList<String> record: FileHandler.tidyData) {
			
			if (TRACE) System.out.println(record.toString());
			
			rowMap = new TreeMap<>();
			String key = "";
			for (int i = 0; i < record.size(); i++) {
				String field = record.get(i);
				if (field != null && field.length() > 0) {
					String id = FileHandler.header.get(i);
					Binding binding = FileHandler.bindingDict.get(id);
					if (null==binding) {
						if (TRACE) System.out.println(id+" is NOT DEFINED in bindingDict");
						String[] ids = FileHandler.header.get(0).split(",");
						if (i<ids.length) {
							id = ids[i];
							binding = FileHandler.bindingDict.get(id);
						} else {
							continue;
						}
					}
					Integer sort = binding.getSynSort();
					if (id.toLowerCase().matches("^jbg-.+$")) {
						key += sort+"="+field+" ";
					} else {
						rowMap.put(sort, field);
					}
					String xPath = binding.getXPath();
					if ("JP PINT"==PROCESSING) {
						if (DOCUMENT_CURRENCY_CODE_ID.equals(id)) {
							documentCurrencyCode.xPath = xPath;
							documentCurrencyCode.value = field;
						} else if (TAX_CURRENCY_CODE_ID.equals(id)) {
							taxCurrencyCode.xPath = xPath;
							taxCurrencyCode.value = field;
						}
					}
				}
			}
			key = key.trim();
			rowMapList.put(key, rowMap);
		}
		
		Integer boughSort = null;
		Integer boughSeq  = null;
		String id         = null;
		String xPath      = null;
		String value      = "";
		HashMap<String,String> attributes               = new HashMap<>();
		TreeMap<Integer/*synSort*/, String/*id*/> idMap = new TreeMap<>();
		
		int n = 0;
		if (TRACE) {
			System.out.println("* HEADER");
			System.out.println(FileHandler.header);
		}
		for (Map.Entry<String, TreeMap<Integer, String>> rowMap : rowMapList.entrySet()) {
			String key                   = rowMap.getKey();
			TreeMap<Integer, String> row = rowMapList.get(key);
			for (Integer synSort : row.keySet()) {
				Binding binding = FileHandler.synBindingMap.get(synSort);
				id              = binding.getID();
				idMap.put(synSort, id);
			}
			n++;
		}
		
		int row_size = n;
		int col_size = idMap.size();
		DataValue[][] dataRedords = new DataValue[row_size][col_size];	
		
		int i = 0;
		for (Map.Entry<String, TreeMap<Integer, String>> rowMap : rowMapList.entrySet()) {
			String key      = rowMap.getKey();
			String[] boughs = key.split(",");
			String bough    = boughs[boughs.length-1];
			String[] data   = bough.split(" ");
			String ds       = data[data.length-1];
			String[] d      = ds.split("=");
			boughSort       = Integer.parseInt(d[0]);
			boughSeq        = Integer.parseInt(d[1]);
			TreeMap<Integer, String> row = rowMapList.get(key);
			for (Integer synSort : row.keySet()) {
				value           = row.get(synSort);
				Binding binding = FileHandler.synBindingMap.get(synSort);
				id              = binding.getID();
				xPath           = binding.getXPath();
				String datatype = binding.getDatatype();
				attributes = new HashMap<>();
				if ("JP PINT"==PROCESSING) {
					if ("Amount".equals(datatype) || "Unit Price Amount".equals(datatype)) {
						if (xPath.length() > 0) {
							if (null!=taxCurrencyCode.xPath && xPath.indexOf(taxCurrencyCode.xPath)>=0) {
								attributes.put("currencyID", taxCurrencyCode.value);
							} else {
								attributes.put("currencyID", documentCurrencyCode.value);
							}
						}
					}
				}
		        // Get key set of the TreeMap using keySet method
		        Set<Integer > keySet = idMap.keySet();
		        // Converting entrySet to ArrayList
		        List<Integer> entryList = new ArrayList<>(keySet);
		        int j = entryList.indexOf(synSort);
				if (TRACE) System.out.println("dataRedords["+i+"]["+j+"] = DataValue("+boughSeq+" /*boughSeq*/, "+boughSort+" /*boughSort*/, "+id+" /*id*/, "+xPath+" /*xPath*/, "+value+" /*value*/, "+attributes+" /*attributes*/)");
				dataRedords[i][j] = new DataValue(boughSeq, boughSort, id, xPath, value, attributes);
			}
			i++;
		}
		
	    for (int y = 0; y < col_size; y++) {
	    	for (int x = 0; x < row_size; x++) {
	        	DataValue dataValue = dataRedords[x][y];
	        	if (null != dataValue) {
		        	boughSeq   = dataValue.seq;
		        	boughSort  = dataValue.sort;
		        	id         = dataValue.id;
		        	xPath      = dataValue.xPath;
		        	value      = dataValue.value;
		        	attributes = dataValue.attributes;
		        	if (TRACE) System.out.println(id+"="+value+xPath);
		        	if (xPath.indexOf("ram:BasisQuantity")>0) {
		        		System.out.println(xPath);
		        	}		        	
					appendElementNS(boughSort, boughSeq, id, xPath, value, attributes);
	        	}
	        }
	    }

		try (FileOutputStream output = new FileOutputStream(out_xml)) {
			WriteXmlDom.writeXml(FileHandler.doc, output);
		} catch (IOException eIO) {
		    eIO.printStackTrace();
		} catch (TransformerException eTE) {
			eTE.printStackTrace();
		}
		
		if (TRACE) System.out.println("-- END -- "+out_xml);
	}

	/**
	 * 指定された要素に対応するXML要素をXMLインスタンス文書に追加する.<br>
	 * 次のステップで追加処理する.
	 * <ul>
	 * <li>a) XPathのそれぞれの階層において、該当する位置に要素があればそれを使用し、なければfillLevelElement()で追加する.</li>
	 * <li>b) XPathの終端の階層では、fillLevelElement()でその値を設定する.</li>
	 * <li>c) b)で追加されたXML要素を返す.</li>
	 * </ul>
	 * 
     * @param boughSort 要素が定義されたTidy dataの行に対応する索引(bough)に対応するグループ要素のセマンティックソート番号.
	 * @param boughSeq 要素が定義されたTidy dataの行に対応する索引(bough)の順序番号.
     * @param id この要素のid.
     * @param xPath この要素のXPath.
     * @param value この要素の値.
     * @param attributes この要素の属性.
     * 
	 * @return Element 追加したXML要素.
	 */
	private static Element appendElementNS (
			Integer boughSort, 
			Integer boughSeq, 
			String id,
			String xPath,
			String value, 
			HashMap<String,String> attributes) 
	{
		if (xPath.indexOf('[') > 0) {
			xPath = FileHandler.stripSelector(xPath);
		}
		value = value.trim();
		Binding binding = FileHandler.bindingDict.get(id);
		Integer semSort = binding.getSemSort();
		if (TRACE) {
			if (value.length() > 0) {
				System.out.println("* appendElementNS "+boughSort+"="+boughSeq+" "+id+"("+semSort+") "+xPath +" = "+value);
			} else {
				System.out.println("* appendElementNS "+boughSort+"="+boughSeq+" "+xPath);
			}
		}
		Element element1, element2, element3, element4, element5, element6, element7, element8, element9;
		ArrayList<String> paths      = splitPath(xPath);
		int depth                    = paths.size();
		Element element0             = FileHandler.root;
//		if (xPath.indexOf("ram:BasisQuantity") >= 0)
//				System.out.println(xPath);
		if (depth > 1) {
			element1 = fillLevelElement(1, depth, element0, paths.get(1), boughSort, boughSeq, value, attributes );
			if (2 == depth) {		
				return element1;
			} else {
				element2 = fillLevelElement(2, depth, element1, paths.get(2), boughSort, boughSeq, value, attributes );
				if (3==depth) {
					return element2;
				} else {
					element3 = fillLevelElement(3, depth, element2, paths.get(3), boughSort, boughSeq, value, attributes );
					if (4==depth) {
						return element3;
					} else {
						element4 = fillLevelElement(4, depth, element3, paths.get(4), boughSort, boughSeq, value, attributes );
						if (5==depth) {
							return element4;
						} else {
							element5 = fillLevelElement(5, depth, element4, paths.get(5), boughSort, boughSeq, value, attributes );
							if (6==depth) {
								return element5;
							} else {
								element6 = fillLevelElement(6, depth, element5, paths.get(6), boughSort, boughSeq, value, attributes );
								if (7==depth) {
									return element6;
								} else {
									element7 = fillLevelElement(7, depth, element6, paths.get(7), boughSort, boughSeq, value, attributes );
									if (8==depth) {
										return element7;
									} else {
										element8 = fillLevelElement(8, depth, element7, paths.get(8), boughSort, boughSeq, value, attributes );
										if (9==depth) {
											return element8;
										} else {
											element9 = fillLevelElement(9, depth, element8, paths.get(9), boughSort, boughSeq, value, attributes );
											if (10==depth) {
												return element9;
											} else {
												if (TRACE) System.out.println("** ERROR appendElementNS appendElementNS XPath dpth is too deep 10.");
												return null;
											}
										}
									}
								}
							}
						}
					}
				}
			}
		}
		return null;
	}
	
	/**
	 * 
	 * 
	 * @param n XML要素のXPathを / で分割したときの何番目の要素か指定する番号.
	 * @param depth XML要素のXPathを / で分割したときにいくつに分割されたかを示す分割された要素数.
	 * @param parent 親のXML要素.
	 * @param path XML要素のXPathを / で分割したときのn番目の要素に対応するXPathの文字列. 親のXML要素からの相対XPath.
     * @param boughSort 要素が定義されたTidy dataの行に対応する索引(bough)に対応するグループ要素のセマンティックソート番号.
	 * @param boughSeq 要素が定義されたTidy dataの行に対応する索引(bough)の順序番号.
     * @param value この要素の値.
     * @param attributes この要素の属性.
	 * 
	 * @return
	 */
	private static Element fillLevelElement (
			int     n, 
			int     depth,
			Element parent, 
			String  path, 
			Integer boughSort, 
			Integer boughSeq,
			String  value,
			HashMap<String,String> attributes ) 
	{
		if (null==parent) {
			if (TRACE) System.out.println("- fillLevelElement parent is NULL use root");
			parent = FileHandler.root;
		}
		String strippedPath          = FileHandler.stripSelector(path);
		Binding boughBinding         = FileHandler.synBindingMap.get(boughSort);
		String boughXPath            = boughBinding.getXPath();
		boughXPath                   = FileHandler.stripSelector(boughXPath);
		ArrayList<String> boughPaths = splitPath(boughXPath);
		int boughLevel               = boughPaths.size()-1;	
		
		String selector = FileHandler.extractSelector(path);
		
		List<Node> elements = FileHandler.getXPath(parent, strippedPath);
		
		Element element = null;
		try {
			if (TRACE) {
				System.out.print("- fillLevelElement getXPath "+strippedPath+" returns "+elements.size()+" elements boughSeq = "+boughSeq+" "+path);
				if (elements.size()==0 && n+1==depth &&
						(("JP PINT" == PROCESSING && ! strippedPath.matches("^cac:.*$")) || 
							terminalElements.indexOf(strippedPath) >= 0 ))  {
					System.out.println(" = "+value);
				} else {
					value = null;
					System.out.println("");
				}
			}
			if (0 == elements.size()) {
				element = createElement(parent, strippedPath, boughSort, 0, value, attributes, n, depth);
				if (selector.length() > 0) {
					if (TRACE) System.out.println("    selector="+selector);
					defineSelector(element, selector, boughSort, boughSeq, n, depth);
				}
			} else {
				if (n == boughLevel) {
					if (boughSeq < elements.size()) {
						element = (Element) elements.get(boughSeq);
					} else {
						element = createElement(parent, strippedPath, boughSort, boughSeq, value, attributes, n, depth);
						if (selector.length() > 0) {
							if (TRACE) System.out.println("    selector="+selector);
							defineSelector(element, selector, boughSort, boughSeq, n, depth);
						}
					}
				} else {
					element = (Element) elements.get(0);
				}
			}			
		} catch (Exception e) {
			System.out.println("xx ERROR fillLevelElement "+parent.getNodeName()+" XPath="+strippedPath+" element = "+element.toString());
			if (TRACE) System.out.println(e.toString());
			e.getStackTrace();
		}
		return element;
	}

	/**
	 * XML要素に対応したSelectorの文字列で指定される要素を定義する.
	 * 
	 * @param element XML要素
	 * @param selector XPathの文字列中のに選択条件を指定する文字列.
     * @param boughSort 要素が定義されたTidy dataの行に対応する索引(bough)に対応するグループ要素のセマンティックソート番号.
	 * @param boughSeq 要素が定義されたTidy dataの行に対応する索引(bough)の順序番号.
	 * @param n XML要素のXPathを / で分割したときの何番目の要素か指定する番号.
	 * @param depth XML要素のXPathを / で分割したときにいくつに分割されたかを示す分割された要素数.
	 */
	private static void defineSelector(
			Element element, 
			String selector, 
			Integer boughSort, 
			Integer boughSeq, 
			int n, 
			int depth ) 
	{
		if (0==selector.length()) {
			return;
		}
		selector = selector.substring(1,selector.length()-1);
		String[] params = selector.split("=");
		String selectorXPath = params[0];
		String selectorValue = params[1];
		if ("true()".equals(selectorValue)) {
			selectorValue = "true";
		} else if ("false()".equals(selectorValue)) {
			selectorValue = "false";
		} else {
			selectorValue = selectorValue.substring(1,selector.length()-1);
		}
		String[] paths = selectorXPath.split("/");
		HashMap<String,String> attrs = new HashMap<>();
		Element el = null;
		for (String sPath : paths) {
			if (sPath.matches("^cac:.*$")) {
				if (TRACE) System.out.println("- defineSelector => createElement "+boughSort+"="+boughSeq+" "+sPath);
				el = createElement(element, sPath, boughSort, boughSeq, "", attrs, n, depth);
			} else {
				if (TRACE) System.out.println("- defineSelector => createElement "+boughSort+"="+boughSeq+" "+sPath+" value="+selectorValue);
				createElement(el, sPath, boughSort, boughSeq, selectorValue, attrs, n, depth);
			}
		}
	}
	
	/**
	 * FileHandler.appendElementNSを使用してXML DOM DocumentにXML要素を追加定義し、そのXML要素を親のXML要素の子要素として追加する.
	 * 指定されたパラメタから定義するXML要素の次の引数を作成し関数を呼び出す。
	 * <ul>
	 * 	<li>prefix XML要素の名前空間を指定する接頭辞.</li>
	 *  <li>nsURI XML要素の名前空間URI.</li>
	 *  <li>prefix XML要素の名前空間を指定する接頭辞.</li>
	 *  <li>attrMap XML要素の属性.</li>
	 * </ul>
	 * 
	 * @param qname 定義するXML要素の名前.
	 * @param parent 親のXML要素.
	 * @param path XML要素のXPathを / で分割したときのn番目の要素に対応するXPathの文字列. 親のXML要素からの相対XPath.
     * @param boughSort 要素が定義されたTidy dataの行に対応する索引(bough)に対応するグループ要素のセマンティックソート番号.
	 * @param boughSeq 要素が定義されたTidy dataの行に対応する索引(bough)の順序番号.
	 * @param value 定義するXML要素の値.
	 * @param attributes 定義するXML要素の属性.
	 * @param level
	 * @param depth XML要素のXPathを / で分割したときにいくつに分割されたかを示す分割された要素数.
	 * 
	 * @return element 定義したXML要素.
	 */
	private static Element createElement (
			Element parent, 
			String path, 
			Integer boughSort, 
			Integer boughSeq,
			String value, 
			HashMap<String,String> attributes, 
			int level,
			int depth ) 
	{
		Element element = null;
		String cacValue = "";
		HashMap<String,String> cacAttributes = null;
				
		String path1 = FileHandler.stripSelector(path);
		String ns = null, nsURI = null, qname = null;
		if ("@".equals(path1.substring(0,1))) {
			qname = path1;
		} else {
			String[] ename = path1.split(":");
			ns = ename[0];
			nsURI = FileHandler.nsURIMap.get(ns);
			qname = ename[1];
		}
		
		if ("JP PINT"==PROCESSING && "cac".equals(ns)) {
			value = cacValue;
			attributes = cacAttributes;
		}
		if ("@".equals(qname.substring(0,1))) {
			FileHandler.appendElementNS(parent, nsURI, ns, qname, value, attributes);
			return null;
		} else {
			element = FileHandler.appendElementNS(parent, nsURI, ns, qname, value, attributes);
			return element;
		}
	}

	/**
	 * 選択条件を指定する [条件式] を含んだXPathを / で分割し、その階層ごとの文字列のリストを返す.
	 * 
	 * @param xPath [条件式] を含んだXPath文字列.
	 * 
	 * @return paths 分割された階層ごとの文字列のリスト. ArrayList&lt;String&gt;.
	 */
	private static ArrayList<String> splitPath (String xPath ) 
	{
		int start = xPath.indexOf("[");
		int last = xPath.lastIndexOf("]");
		String xPath1 = "";
		if (start >= 0) {
			String selector = xPath.substring(start, last+1);
			selector = selector.replaceAll("/","_");
			xPath1 = xPath.substring(0, start)+selector+xPath.substring(last+1,xPath.length());		
		} else {
			xPath1 = xPath;
		}
		ArrayList<String> paths = new ArrayList<>();
		if ("/".equals(xPath1.substring(0,1))) {
			xPath1 = xPath1.substring(1);
		}
		String[] paths0 = xPath1.split("/");
		for (int i = 0; i < paths0.length; i++) {
			String path = paths0[i];
			path = path.replaceAll("_","/");
			paths.add(path);
		}
		return paths;
	}

}
