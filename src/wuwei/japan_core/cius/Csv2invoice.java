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
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Collectors;

import javax.xml.transform.TransformerException;

import org.w3c.dom.Element;
import org.w3c.dom.Node;

import wuwei.japan_core.utils.CSV;
import wuwei.japan_core.utils.CustomComparator;
import wuwei.japan_core.utils.WriteXmlDom;
import wuwei.japan_core.utils.XPathHandler;

/**
 * Tidy dataを格納しているCSVファイルを読み取りセマンティックモデル定義と構文バインディング定義からXMLインスタンス文書を出力する.
 */
public class Csv2invoice {
	static boolean TRACE         = false;	
	static boolean DEBUG         = false;	
	static String PROCESSING     = null;
	static String SYNTAX_BINDING = null;
	static String XML_SKELTON    = null;
	static String CHARSET        = "UTF-8";
	
	static String IN_CSV         = null;
	static String OUT_XML        = null;
	
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
//	static TreeMap<String, TreeMap<Integer, String>> rowMapList = new TreeMap<>();
    static TreeMap<String, TreeMap<Integer, String>> rowMapList = new TreeMap<>(new CustomComparator());

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
	static class DataValue {
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
 				HashMap<String,String> attributes) {
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
	static class PathValue {
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
 	 * CSVをデジタルインボイス(XML)に変換する。
 	 * The application's entry point
	 * @param args an array of command-line arguments for the application
	 * last updated 2023-10-09
	 */
	public static void main(String[] args) {
	    parseAndSetArguments(args);
	    processCSV(IN_CSV, OUT_XML);
	    System.out.println("** END ** Csv2Invoice " + PROCESSING + " " + IN_CSV + " " + OUT_XML);
	}
	
	private static void parseAndSetArguments(String[] args) {
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
	    TRACE = false;
	    DEBUG = false;

	    if (args.length <= 1) {
	        TRACE = true;
	        if (1 == args.length) {
	            PROCESSING = args[0] + " SYNTAX";
	        } else {
	            PROCESSING = "JP-PINT SYNTAX";
	        }
	        setFilesPathBasedOnProcessing();

	    } else if (args.length >= 3) {
	        PROCESSING = args[0] + " SYNTAX";
	        IN_CSV = args[1];
	        OUT_XML = args[2];
	        if (args.length >= 4) {
	            if (args[3].indexOf("T") >= 0)
	                TRACE = true;
	            if (args[3].indexOf("D") >= 0)
	                DEBUG = true;
	        }
	    }
	    
	    if (args.length >= 5) {
	        SYNTAX_BINDING = args[3];
	        XML_SKELTON = args[4];
	        FileHandler.SYNTAX_BINDING = SYNTAX_BINDING;
	        FileHandler.XML_SKELTON = XML_SKELTON;
	        if (6 == args.length) {
	            if (args[5].indexOf("T") >= 0)
	                TRACE = true;
	            if (args[5].indexOf("D") >= 0)
	                DEBUG = true;
	        }
	    } else {
	        setDefaultSyntaxBindingAndSkeleton();
	    }

	    FileHandler.PROCESSING = PROCESSING;
	    FileHandler.TRACE = TRACE;
	    FileHandler.DEBUG = DEBUG;
	    XPathHandler.TRACE = TRACE;
	    XPathHandler.DEBUG = DEBUG;
	    CSV.TRACE = TRACE;
	    CSV.DEBUG = DEBUG;
	}

	private static void setFilesPathBasedOnProcessing() {
	    if (0 == PROCESSING.indexOf("JP-PINT")) {
	        IN_CSV = "data/csv/Example1_PINT.csv";
	        OUT_XML = "data/xml/Example1_PINT.xml";
	    } else if (0 == PROCESSING.indexOf("SME-COMMON")) {
	        IN_CSV = "data/csv/Example1_SME.csv";
	        OUT_XML = "data/xml/Example1_SME.xml";
	    } else {
	        // Handling for unsupported PROCESSING type
	        throw new IllegalArgumentException("Unsupported PROCESSING type");
	    }
	}

	private static void setDefaultSyntaxBindingAndSkeleton() {
	    if (0 == PROCESSING.indexOf("JP-PINT")) {
	        FileHandler.SYNTAX_BINDING = FileHandler.JP_PINT_CSV;
	        FileHandler.XML_SKELTON = FileHandler.JP_PINT_XML_SKELTON;
	    } else if (0 == PROCESSING.indexOf("SME-COMMON")) {
	        FileHandler.SYNTAX_BINDING = FileHandler.SME_CSV;
	        FileHandler.XML_SKELTON = FileHandler.SME_XML_SKELTON;
	    } else {
	        // Handling for unsupported PROCESSING type
	        throw new IllegalArgumentException("Unsupported PROCESSING type");
	    }
	}

	/**
	 * Tidy dataのCSVファイルをデジタルインボイスのXMLインスタンス文書に変換する.
	 * 
	 * @param in_csv 入力するTidy dataのCSVファイル.
	 * @param out_xml 出力するデジタルインボイスのXMLインスタンス文書.
	 */
	public static void processCSV(String in_csv, String out_xml) {
		Binding binding        = null;
		Binding defaultBinding = null;
		Integer boughSort      = null;
		Integer boughSeq       = null;
		Integer semSort        = null;
		Integer synSort        = null;
		String id              = null;
		String xPath           = null;
		String value           = "";
		String rowKey          = null;		
		HashMap<String,String>                    attributes = new HashMap<>();
		TreeMap<Integer/*synSort*/, String/*id*/> idMap      = new TreeMap<>();
		TreeMap<String/*rowKey:id*/, Binding>     defaultMap = new TreeMap<>();
		
		FileHandler.parseBinding();		
		FileHandler.parseSkeleton();
			
		try {
			if (0==PROCESSING.indexOf("SME-COMMON"))
				terminalElements = new ArrayList<String>(Arrays.asList(
						"@unitCode","DateTimeString","Indicator",
						"IssueDateTime","AccountName","ActualAmount","AdditionalReferencedCIReferencedDocument","AllowanceTotalAmount",
						"AttachmentBinaryObject","BasisAmount","BasisQuantity","BilledQuantity","BuyerAssignedID",
						"BuyerOrderReferencedCIReferencedDocument","CalculatedAmount","CalculatedRate","CalculationMethodCode",
						"CalculationPercent","CardholderName","CategoryCode","CategoryName","ChannelCode","ChargeAmount","ChargeIndicator",
						"ChargeTotalAmount","CompleteNumber","Content","ConversionRate","CountryID","CurrencyCode","DepartmentName",
						"Description","DirectionCode","DuePayableAmount","FileName","GlobalID","GrandTotalAmount","GrossLineTotalAmount",
						"ID","IncludingTaxesLineTotalAmount","Information","InstructedAmount","InvoiceCurrencyCode","InvoiceCurrencyCode",
						"IssuerAssignedID","IssuingCompanyName","JapanFinancialInstitutionCommonID","LineID","LineOne","LineThree",
						"LineTwo","LocalTaxSystemID","ManufacturerAssignedID","MIMECode","Name","NetIncludingTaxesLineTotalAmount",
						"NetLineTotalAmount","PackageQuantity","PaidAmount","PaymentCurrencyCode","PerPackageUnitQuantity","PersonID",
						"PersonName","PostcodeCode","PreviousRevisionID","ProductGroupID","ProductUnitQuantity","ProprietaryID",
						"PurposeCode","RateApplicablePercent","Reason","ReasonCode","ReferenceTypeCode","RegisteredID","RevisionID",
						"SellerAssignedID","SourceCurrencyCode","SpecifiedTransactionID","Subject","SubordinateLineID","SubtypeCode",
						"TargetCurrencyCode","TaxBasisTotalAmount","TaxCurrencyCode","TaxCurrencyCode","TaxTotalAmount","TotalPrepaidAmount",
						"TypeCode","URIID","Value"));
			FileHandler.csvFileRead(in_csv, CHARSET);
		} catch (FileNotFoundException e) {
			System.out.println("File not found "+in_csv);
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		// 通貨コード取得
		for (int i=0; i<FileHandler.header.size(); i++) {
			id = FileHandler.header.get(i);
			if (id.equals(DOCUMENT_CURRENCY_ID))
				DOCUMENT_CURRENCY = FileHandler.tidyData.get(0).get(i);
			else if (id.equals(TAX_CURRENCY_ID))
				TAX_CURRENCY = FileHandler.tidyData.get(0).get(i);
		}
		if (null==DOCUMENT_CURRENCY)
			DOCUMENT_CURRENCY = "JPY";
		else if (null!=TAX_CURRENCY && !TAX_CURRENCY.equals("JPY"))
			TAX_CURRENCY = "JPY";
		
		if (TRACE) System.out.println("- processCSV FileHandler.tidyData record");
		
		rowMapList = new TreeMap<>(new CustomComparator());
		
		for (ArrayList<String> record: FileHandler.tidyData) {			
			if (TRACE) System.out.println(record.toString());			
			rowMap = new TreeMap<>();
			String key = "";
			for (int i = 0; i < record.size(); i++) {
				String field = record.get(i);
				if (field != null && field.length() > 0) {
					id      = FileHandler.header.get(i);
					binding = FileHandler.bindingDict.get(id);
					if (null==binding && id.startsWith("d_")) {
						binding = FileHandler.bindingDict.get(id.substring(2));
					}
					if (null==binding) {
						if (DEBUG) System.out.println(id+" is NOT DEFINED in bindingDict");
						String[] ids = FileHandler.header.get(0).split(",");
						if (i<ids.length) {
							id      = ids[i];
							binding = FileHandler.bindingDict.get(id);
						}
					}
					if (null==binding)
						continue;
					semSort = binding.getSemSort();
					synSort = binding.getSynSort();
					if (id.toUpperCase().matches("^D_[A-Z0-9]+(_([A-Z0-9]_)?[A-Z0-9]+)?$")) {
						key += synSort+"="+field+" ";
						if (0 == PROCESSING.indexOf("SME-COMMON") && 0 == semSort - MIN_TAX_BREAKDOWN)
							COUNT_TAX_BREAKDOWN = 1 + Integer.parseInt(field);
					} else {
						rowMap.put(synSort, field);
					}
					xPath = binding.getXPath();
					if (DOCUMENT_CURRENCY_ID.equals(id)) {
						documentCurrencyCode.xPath = xPath;
						documentCurrencyCode.value = field;
					} else if (TAX_CURRENCY_ID.equals(id)) {
						taxCurrencyCode.xPath = xPath;
						taxCurrencyCode.value = field;
					}
				}
			}
			key = key.trim();
			rowMapList.put(key, rowMap);
		}
					
		int n = 0;
		if (TRACE) {
			System.out.println("* HEADER");
			System.out.println(FileHandler.header);
		}
		// Syntax Sort順にheaderをソート
		for (Map.Entry<String, TreeMap<Integer, String>> rowMap : rowMapList.entrySet()) {
			rowKey                       = rowMap.getKey();
			TreeMap<Integer, String> row = rowMapList.get(rowKey);
			for (Integer _synSort : row.keySet()) {
				binding = FileHandler.synBindingMap.get(_synSort);
				if (null!=binding) {
					id = binding.getID();			
					idMap.put(_synSort, id);
					String prefix = removeSuffix(id);
			        List<String> keys = FileHandler.defaultMap.keySet().stream()
			                .filter(k -> removeSuffix(k).equals(prefix))
			                .collect(Collectors.toList());
			        for (String key: keys) {
			        	defaultBinding         = FileHandler.defaultMap.get(key);
			        	Integer defaultSynSort = defaultBinding.getSynSort();
			            defaultMap.put(rowKey+":"+defaultSynSort, defaultBinding);
			        	idMap.put(defaultSynSort, key);
			            if (DEBUG) {
				        	String defaultValue = defaultBinding.getDefaultValue();
			            	System.out.println("Default value: "+defaultBinding.getLevel()+" "+id+" "+key+" = "+defaultValue);
			            }
			        }
				}
			}
			n++;
		}
		
		int row_size = n;
		int col_size = idMap.size();
		DataValue[][] dataRedords = new DataValue[row_size][col_size];	
		
//		if (DEBUG) {
//			System.out.println("** idMap");
//			for (Integer _synSort : idMap.keySet()) {
//				Binding b = FileHandler.synBindingMap.get(_synSort);
//				String xpath = b.getXPath();
//				if (xpath.contains("Tax"))
//					System.out.println(_synSort+" "+b.getLevel()+" "+b.getID()+" "+xpath+" "+b.getDefaultValue());
//			}
//		}
		
		int i = 0;
		for (Map.Entry<String, TreeMap<Integer, String>> rowMap : rowMapList.entrySet()) {
			rowKey          = rowMap.getKey();
			String[] boughs = rowKey.split(",");
			String   bough  = boughs[boughs.length-1];
			String[] data   = bough.split(" ");
			String   ds     = data[data.length-1];
			String[] d      = ds.split("=");
			if (d.length < 2) {
				System.out.println(d);
				continue;
			}
			boughSort       = Integer.parseInt(d[0]);
			boughSeq        = Integer.parseInt(d[1]);
			TreeMap<Integer, String> row = rowMapList.get(rowKey);
			for (Integer _synSort : idMap.keySet()) {
				if (_synSort < 1) {
					System.out.println(_synSort);
					continue;
				}
				value = row.get(_synSort);
				if (null==value || value.length()==0) {
					defaultBinding = defaultMap.get(rowKey+":"+_synSort);
					if (null!=defaultBinding)
						value = defaultBinding.getDefaultValue();
				}
				if (null==value || value.length()==0)
					continue;
				binding = FileHandler.synBindingMap.get(_synSort);
				id      = binding.getID();
				xPath   = binding.getXPath();
				// XMLパーサーが[??=true()]や[??=false()]のBool値を判定できないため、文字列として判定する形にXPathを書き換える。
				if (xPath.indexOf("true")>0) {
					xPath = xPath.replaceAll("\\[([:a-zA-Z]*)=true\\(\\)\\]","[normalize-space($1/text())='true']");
				} else if (xPath.indexOf("false")>0) {
					xPath = xPath.replaceAll("\\[([:a-zA-Z]*)=false\\(\\)\\]","[normalize-space($1/text())='false']");
				// XMLパーサーが[cbc:TaxAmount/@currencyID=./cbc:DocumentCurrencyCode]を正しく判定できないので、固定値との比較に書き換える。
				} else if  (0==PROCESSING.indexOf("JP-PINT")) {
					if (xPath.indexOf("cbc:DocumentCurrencyCode]")>0) {
						xPath = xPath.replaceAll("(/Invoice|/\\*|\\.)/cbc:DocumentCurrencyCode","'"+DOCUMENT_CURRENCY+"'");
					} else if (xPath.indexOf("cbc:TaxCurrencyCode]")>0) {
						xPath = xPath.replaceAll("(/Invoice|/\\*|\\.)/cbc:TaxCurrencyCode","'"+TAX_CURRENCY+"'");
					}
				} else if  (0==PROCESSING.indexOf("SME-COMMON")) {
					if (xPath.indexOf("InvoiceCurrencyCode]")>0) {
						xPath = xPath.replaceAll(
								"//CIIHSupplyChainTradeTransaction/ApplicableCIIHSupplyChainTradeSettlement/InvoiceCurrencyCode",
								"'"+DOCUMENT_CURRENCY+"'");
					} else if (xPath.indexOf("TaxCurrencyCode]")>0) {
						xPath = xPath.replaceAll(
								"//CIIHSupplyChainTradeTransaction/ApplicableCIIHSupplyChainTradeSettlement/TaxCurrencyCode",
								"'"+TAX_CURRENCY+"'");
					}
				}
				String datatype = binding.getDatatype();
				attributes      = new HashMap<>();
				if (0==PROCESSING.indexOf("JP-PINT")) {
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
				Set<Integer> keySet = idMap.keySet();
				
				// Converting entrySet to ArrayList
				List<Integer> entryList = new ArrayList<>(keySet);
				
				int j = entryList.indexOf(_synSort);
				if (TRACE) System.out.println("dataRedords["+i+"]["+j+"] = DataValue("+boughSort+" "+boughSeq+"  "+id+" "+FileHandler.getShortPath(xPath)+" "+value+" "+attributes);
				
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
					if (null!=xPath && xPath.length() > 0) {
						if (0==PROCESSING.indexOf("JP-PINT") && id.equals("JC69_e_JC13_01")) { 
							// JC69_e_JC13_01(IBT-184 Despatch advice reference cac:DespatchLineReference/cac:DocumentReference/cbc:ID )
							// では、UBL構文が必須としている cac:DespatchLineReference/cbc:LineID　に　NA を定義する。
							// Syntax required item. Value shall be NA. 構文必須要素。値として 'NA'を使用する。							
							if (DEBUG)
								System.out.println("call appendElementNS /Invoice/cac:InvoiceLine/cac:DespatchLineReference/cbc:LineID = NA");
							appendElementNS(boughSort, boughSeq, "", "/Invoice/cac:InvoiceLine/cac:DespatchLineReference/cbc:LineID", "NA", attributes);
						} else if (0==PROCESSING.indexOf("SME-COMMON")) {
							// 外貨でての税額があるときには、文書合計金額の税額に外貨建ての金額もあるのでSelkectorを修正する。
							binding         = FileHandler.bindingDict.get(id);
							semSort = binding.getSemSort();
							if (MIN_DOCUMENT_TOTAL <= semSort && semSort <= MAX_DOCUMENT_TOTAL)
								xPath = FileHandler.stripSelector(xPath);
							if (id.equals(TOTAL_TAX_ID)) {
								attributes.put("currencyID", DOCUMENT_CURRENCY);
								xPath += "[position()=1]";
							} else if (id.equals(TOTAL_TAX_CURRENCY_TAX_ID)) {
								attributes.put("currencyID", TAX_CURRENCY);
								xPath += "[position()=2]";
							}
							/**
							 * SME-COMMONのときの外貨建ての税区分ごとの税額の判定が不正。暫定的に外貨建てを対象外とする。
							 * TODO: 外貨建ての税区分ごとの税額サポート
							 */
							if (xPath.indexOf("[CurrencyCode=/SMEInvoice/CIIHSupplyChainTradeTransaction/ApplicableCIIHSupplyChainTradeSettlement/InvoiceCurrencyCode]") > 0) {
								xPath = FileHandler.stripSelector(xPath);
							}
							else if (xPath.indexOf("[CurrencyCode=/SMEInvoice/CIIHSupplyChainTradeTransaction/ApplicableCIIHSupplyChainTradeSettlement/TaxCurrencyCode]") > 0) {
								if (DEBUG) System.out.println("TODO: support "+xPath);
							}
//							/**
//							 * SME-COMMONのときのSelector条件では、子要素のほとんどで新しくApplicableCITradeTaxを定義してしまう。
//							 * ApplicableCITradeTaxをまとめて定義しなくても済ませるために、ApplicableCITradeTaxの定義順をpositionで指定する。
//							 * ApplicableCITradeTax[CurrencyCode='JPY']
//							 * ApplicableCITradeTax[CurrencyCode=//CIIHSupplyChainTradeTransaction/ApplicableCIIHSupplyChainTradeSettlement/InvoiceCurrencyCode]
//							 */
//							if (MIN_TAX_BREAKDOWN <= semSort && semSort <= MAX_TAX_BREAKDOWN) {
//								if (COUNT_TAX_BREAKDOWN > 0) {
//									xPath = xPath.replace("[CurrencyCode='"+DOCUMENT_CURRENCY+"']","[position()="+(1+boughSeq)+"]");;
//								} else {
//									xPath = FileHandler.stripSelector(xPath);
//								}
//							} else if (MIN_TAX_CURRENCY_BREAKDOWN <= semSort && semSort <= MAX_TAX_CURRENCY_BREAKDOWN) {
//								if (COUNT_TAX_BREAKDOWN > 0) {
//									xPath = xPath.replace("[CurrencyCode='"+TAX_CURRENCY+"']","[position()="+(1+boughSeq+COUNT_TAX_BREAKDOWN)+"]");;
//								} else {
//									xPath = xPath.replace("[CurrencyCode='"+TAX_CURRENCY+"']","[position()=2]");
//								}
//							}
						}
						if (DEBUG) 
							System.out.println("call appendElementNS "+id+" "+FileHandler.getShortPath(xPath)+" = "+value);
						
						appendElementNS(boughSort, boughSeq, id, xPath, value, attributes);
						
					}
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
		
		if (DEBUG) System.out.println("-- END -- "+out_xml);		
	}

    private static String removeSuffix(String str) {
        Pattern pattern = Pattern.compile("^(.*?)(_\\d+)?$");
        Matcher matcher = pattern.matcher(str);
        if (matcher.find()) {
            return matcher.group(1);
        } else {
            return str;  // これは起こり得ないが、マッチしなかった場合のフォールバックとして残しています
        }
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
			HashMap<String,String> attributes) {
		value               = value.trim();
		Binding binding     = FileHandler.bindingDict.get(id);
		Integer synSort     = binding.getSynSort();
		String defaultValue = binding.getDefaultValue();
		if (defaultValue.length() > 0 && ! value.equals(defaultValue))
			value = defaultValue;

		if (DEBUG) {
			if (value.length() > 0) {
				System.out.println("* appendElementNS "+boughSort+"="+boughSeq+" "+id+"("+synSort+")\n"+FileHandler.getShortPath(xPath) +" = "+value);
			} else {
				System.out.println("* appendElementNS "+boughSort+"="+boughSeq+"\n"+FileHandler.getShortPath(xPath));
			}
		}
		ArrayList<String> paths = splitPath(xPath);
		int depth               = paths.size();	
	    Element currentElement  = FileHandler.root;	    
	    for (int i = 1; i < depth; i++) {
			if (depth == i+1) {
				currentElement = fillLevelElement(i, currentElement, xPath, boughSort, boughSeq, value, attributes );
				return currentElement;
			} else {
				currentElement = fillLevelElement(i, currentElement, xPath, boughSort, boughSeq, null, new HashMap<>() );
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
			Element parent, 
			String  xPath, 
			Integer boughSort, 
			Integer boughSeq,
			String  value,
			HashMap<String,String> attributes ) {
		ArrayList<String> paths = splitPath(xPath);
		int depth               = paths.size();	
		String path             = paths.get(n);
//		String childPath        = null;
//		if (n + 1 <= depth - 1)
//			childPath = paths.get(n+1);
		if (null==parent) {
			if (DEBUG) System.out.println("- fillLevelElement parent is NULL use root");
			parent = FileHandler.root;
		}
		if (0==path.indexOf("@currencyID")) {
			if (DEBUG) System.out.println("- fillLevelElement setting @currencyID return Amount element");
			return parent;
		}			
//		if ("cbc:TaxAmount".equals(parent.getNodeName()))
//			System.out.println(parent.getNodeName());
		String strippedPath  = FileHandler.stripSelector(path);
		Binding boughBinding = FileHandler.synBindingMap.get(boughSort);
		String boughXPath    = boughBinding.getXPath();
		boughXPath           = FileHandler.stripSelector(boughXPath);
		ArrayList<String> 
			boughPaths       = splitPath(boughXPath);
		int boughLevel       = boughPaths.size()-1;
//		String selector      = FileHandler.extractSelector(path);
		
		List<Node> elements  = FileHandler.getXPath(parent, strippedPath);// path);		
		Element element      = null;
		try {
			if (DEBUG) {
				System.out.print("- fillLevelElement getXPath returns "+elements.size()+" elements boughSeq = "+boughSeq+" "+path);
				if (elements.size()==0 && n+1==depth &&
					((0==PROCESSING.indexOf("JP-PINT") && ! path.matches("^cac:[a-zA-Z]+$")) || 
						(0==PROCESSING.indexOf("SME-COMMON") && terminalElements.indexOf(strippedPath) >= 0))) {
					System.out.println(" = "+value);
				} else {
					System.out.println("");
				}
			}
			
			if (0 == elements.size()) {
				if (DEBUG) System.out.println("+createElement"+parent.getChildNodes().toString()+" "+path+" value="+value);
				
				element = createElement(parent, strippedPath, value, attributes, n, depth);
				
//				if (selector.length() > 0 && selector.indexOf(childPath) < 0) {
//					if (DEBUG) System.out.println("    selector="+selector);
//					
//					defineSelector(element, selector, boughSort, boughSeq, n, depth);
//					
//				}
			} else {
				if (n == boughLevel) {
					if (path.indexOf("position") > 0) { // 課税分類ごとの金額に外貨建てがあることを考慮したことでSelector条件をposition=nに変更していることにより、boughSeqで区別せずに済むため。
						 element = (Element) elements.get(0);
					} else if (boughSeq <= elements.size()) { // 返金や追加請求など同じSelector条件で複数ある場合は、boughSeqで区別する。 boughSeq=1, 2, 3, ...
						 if (boughSeq > 0) // 2023-10-04
							 boughSeq -= 1;
						 element = (Element) elements.get(boughSeq); 
					} else {
						if (DEBUG) System.out.println("+createElement"+parent.getChildNodes().toString()+" "+path+" value="+value);
						
						element = createElement(parent, strippedPath, value, attributes, n, depth);
						
//						if (selector.length() > 0 && selector.indexOf("position") < 0) {
//							if (DEBUG) System.out.println("    selector="+selector);
//							
//							defineSelector(element, selector, boughSort, boughSeq, n, depth);
//							
//						}
					}
				} else {
					element = (Element) elements.get(0);
				}				
			}			
		} catch (Exception e) {
			System.out.println("xx ERROR fillLevelElement "+parent.getNodeName()+" XPath="+path);
			System.out.println(e.toString());
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
//	private static void defineSelector(
//			Element element, 
//			String  selector, 
//			Integer boughSort, 
//			Integer boughSeq, 
//			int     n, 
//			int     depth ) {
//		if (selector==null || 0==selector.length() || 0==selector.indexOf("not(") || selector.indexOf("position") >= 0) {
//			return;
//		}
//		selector = selector.substring(1,selector.length()-1);
//		if (selector.startsWith("not("))
//			return;
//		String[] params      = selector.split("=");
//		String selectorXPath = params[0];		
//        // 正規表現パターンを用意します。こちらは "normalize-space(" の後の任意の文字列をキャプチャするものです。
//        Pattern pattern = Pattern.compile("normalize-space\\(([^/]+)/text\\(\\)\\)");
//        Matcher matcher = pattern.matcher(selectorXPath);
//        // マッチするものが見つかった場合、キャプチャした部分（つまり、要素名）を返します。
//        if (matcher.find()) {
//        	selectorXPath = matcher.group(1);  // グループ 1 がキャプチャした部分です。
//        }		
//		String selectorValue         = params[1].replace("'","");
//		String[] paths               = selectorXPath.split("/");
//		HashMap<String,String> attrs = new HashMap<>();
//		Element el = element;
//		for (String sPath : paths) {
//			if (sPath.matches("^cac:.*$")) {
//				if (DEBUG) System.out.println("- defineSelector => createElement "+sPath);
//				
//				el = createElement(el, sPath, "", attrs, n, depth);
//				
//			} else {
//				if (DEBUG) System.out.println("- defineSelector => createElement "+sPath+" value="+selectorValue);
//				
//				el = createElement(el, sPath, selectorValue, attrs, n, depth);
//				
//			}
//		}
//	}

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
	 * @param value 定義するXML要素の値.
	 * @param attributes 定義するXML要素の属性.
	 * @param level
	 * @param depth XML要素のXPathを / で分割したときにいくつに分割されたかを示す分割された要素数.
	 * 
	 * @return element 定義したXML要素.
	 */
	private static Element createElement(
			Element parent, 
			String path,
			String value, 
			HashMap<String,String> attributes, 
			int level,
			int depth ) {
		Element element = null;
		String cacValue = "";
		HashMap<String,String> cacAttributes = null;
				
		String path1 = FileHandler.stripSelector(path);
		String ns = null, nsURI = null, qname = null;
		if ("@".equals(path1.substring(0,1))) {
			qname = path1;
		} else {
			if (path1.contains(":")) {
				String[] ename = path1.split(":");
				ns             = ename[0];
				nsURI          = FileHandler.nsURIMap.get(ns);
				qname          = ename[1];
			} else {
				ns    = "";
				qname = path1;
			}
		}
		
		if (0==PROCESSING.indexOf("JP-PINT") && "cac".equals(ns)) {
			value      = cacValue;
			attributes = cacAttributes;
		}
		
		element = FileHandler.appendElementNS(parent, nsURI, ns, qname, value, attributes);
		
		return element;
	}

	/**
	 * 選択条件を指定する [条件式] を含んだXPathを / で分割し、その階層ごとの文字列のリストを返す.
	 * 
	 * @param xPath [条件式] を含んだXPath文字列.
	 * 
	 * @return paths 分割された階層ごとの文字列のリスト. ArrayList&lt;String&gt;.
	 */
	private static ArrayList<String> splitPath (String xPath ) {
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
