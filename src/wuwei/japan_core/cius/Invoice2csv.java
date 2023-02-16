package wuwei.japan_core.cius;

import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;

import org.w3c.dom.Node;

/**
 * デジタルインボイスのXMLインスタンス文書を読み取り、Tidy dataを格納しているCSVファイルを出力する.
 */
public class Invoice2csv {
	static String IN_XML = "data/xml/Example1.xml";
	static String OUT_CSV = "data/csv/Example1.csv";
	static String CHARSET = "UTF-8";

	/**
	 * Tidy dataテーブルの行を指定する索引データ
	 */
    static TreeMap<Integer/* sort */,Integer/* seq */> boughMap = new TreeMap<>();
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
 	 * mainでは変換処理を単体でテストする.
	 * 
	 * @param args
	 */
    public static void main(String[] args) {
    	FileHandler.CORE_CSV = FileHandler.JP_PINT_CSV;

//		processInvoice("data/xml/Example0.xml", "data/csv/Example0.csv");
		 processInvoice("data/xml/Example1.xml", "data/csv/Example1.csv");
//		 processInvoice("data/xml/Example2-TaxAcctCur.xml", "data/csv/Example2-TaxAcctCur.csv");
//		 processInvoice("data/xml/Example3-0.xml", "data/csv/Example3-0.csv");
//		 processInvoice("data/xml/Example3-SumInv1.xml", "data/csv/Example3-SumInv1.csv");
//		 processInvoice("data/xml/Example4-SumInv2.xml", "data/csv/Example4-SumInv2.xsv");
//		 processInvoice("data/xml/Example5-AllowanceCharge0.xml", "data/csv/Example5-AllowanceCharge0.csv");
//		 processInvoice("data/xml/Example5-AllowanceCharge.xml", "data/csv/Example5-AllowanceCharge.csv");
//		 processInvoice("data/xml/Example6-CorrInv.xml", "data/csv/Example6-CorrInv.csv");
//		 processInvoice("data/xml/Example7-Return.Quan.xml", "data/csv/Example7-Return.Quan.csv");
//		 processInvoice("data/xml/Example8-Return.ItPr.xml", "data/csv/Example8-Return.ItPr.csv");
		 System.out.println("** END Invoice2csv**");
	}
	
	/**
	 * を読み込んで Tidy dataテーブルに展開し、CSVファイルに出力する.
	 * 
	 * @param in_xml デジタルインボイス（XMLインスタンス文書）.
	 * @param out_csv Tidy dataのCSV(RFC4180形式)ファイル.
	 */
	private static void processInvoice(String in_xml, String out_csv) {
		System.out.println("\n** processInvoice("+in_xml+", "+out_csv+")");
		
	    boughMap = new TreeMap<Integer/*sort*/,Integer/*seq*/>();
	    boughMapList = new ArrayList<TreeMap<Integer, Integer>>();
	    rowMap = new TreeMap<Integer, String>();
	    rowMapList = new TreeMap<String, TreeMap<Integer, String>>();
	
	    FileHandler.parseBinding();
	    
		try {
			FileHandler.parseInvoice(in_xml);
		} catch (Exception e) {
			e.printStackTrace();
			return;
		}
		
		FileHandler.nodeMap = FileHandler.parseDoc();
	    
		for (Map.Entry<String, Binding> entry : FileHandler.bindingDict.entrySet()) {
			Binding binding = entry.getValue();
			Integer sort = binding.getSemSort();
			String id = binding.getID();
			String card = binding.getCard();
			if (id.toLowerCase().matches("^jbg-.+$") &&
					card.matches("^.*n$") &&
					isMultiple(sort)) {
				FileHandler.multipleMap.put(sort, id);
			}
		}
	    
		Binding binding = FileHandler.bindingDict.get(FileHandler.ROOT_ID);
		Integer sort = binding.getSemSort();
		boughMap.put(1000,0);
		boughMapList.add(boughMap);
		
	    fillGroup(FileHandler.root, sort, boughMap);
	    
	    fillTable();
	    
        try {
			FileHandler.csvFileWrite(out_csv, CHARSET);
        } catch (FileNotFoundException fnf) {
        	System.out.println("* File Not Found Exception "+out_csv);
		} catch (IOException e) {
			e.printStackTrace();
		}

		System.out.println("-- END -- "+in_xml);
	}
	
	/**
	 * Tidy dataテーブル作成用の2次元リストrowMapListをTidy dataテーブル(FileHandler/tidyData)に変換する.
	 */
	private static void fillTable() {
		FileHandler.tidyData = new ArrayList<ArrayList<String>>();
		System.out.println();

		FileHandler.header.add("jbg-00");
		// bough
		for (Map.Entry<Integer,String> multipleEntry : FileHandler.multipleMap.entrySet()) {
			String multipleID = multipleEntry.getValue();
			Binding multipleBinding = FileHandler.bindingDict.get(multipleID);
			if (multipleID.toLowerCase().matches("^jbg-.+$") &&
					multipleBinding.isUsed()) {
				FileHandler.header.add(multipleID);
			}
		}
		// data
		for (Map.Entry<Integer,Binding> dataEntry : FileHandler.semBindingMap.entrySet()) {
			Integer dataSort = dataEntry.getKey();
			Binding dataBinding = dataEntry.getValue();
			String dataID = dataBinding.getID();
			if (1000!=dataSort &&
					dataID.toLowerCase().matches("^jbt-.+$") &&
					dataBinding.isUsed() &&
					! FileHandler.header.contains(dataID)) {
				FileHandler.header.add(dataID);
			}
		}
		System.out.println("* FileHandler.tidyData\n"+FileHandler.header.toString());
		for (Map.Entry<String, TreeMap<Integer, String>> entryRow : rowMapList.entrySet()) {
			ArrayList<String> record = new ArrayList<>();
			for (int i = 0; i < FileHandler.header.size(); i++) {
				record.add("");
			}
			// bough
			String rowMapKey = entryRow.getKey();
			String[] boughs = rowMapKey.split(" ");
			for (String bough : boughs) {
				String[] index = bough.split("=");
				Integer boughSort = Integer.parseInt(index[0]);
				Binding boughBinding = FileHandler.semBindingMap.get(boughSort);
				if (null!=boughBinding) {
					String boughID = boughBinding.getID();
					String boughSeq = index[1];
					int boughIndex = FileHandler.header.indexOf(boughID);
					if (boughIndex!=-1) {
						record.set(boughIndex, boughSeq);
					} else {
						System.out.println(boughID+" NOT FOUND in the header");
					}
				}
			}
			// data
			TreeMap<Integer, String> rowMap = entryRow.getValue();
			for (Map.Entry<Integer, String> entry : rowMap.entrySet()) {
				Integer sort = entry.getKey();
				String value = entry.getValue();
				Binding binding = FileHandler.semBindingMap.get(sort);
				String id = binding.getID();
				int dataIndex = FileHandler.header.indexOf(id);
				if (dataIndex!=-1) {
					record.set(dataIndex, value);
				} else {
					System.out.println(id+" NOT FOUND in the header");
				}
			}
			FileHandler.tidyData.add(record);
			System.out.println(record.toString());
		}
	}

	/**
	 * 見つかった要素を Tidy dataテーブル作成用の2次元リストrowMapListに登録する.
	 * 
	 * @param semSort セマンティックモデルのセマンティックソート番号
	 * @param value 要素の値
	 * @param boughMap 
	 */
	private static void fillData (
			Integer semSort, 
			String value, 
			TreeMap<Integer, Integer> boughMap ) {
		Binding binding = (Binding) FileHandler.semBindingMap.get(semSort);
        String id = binding.getID();
		String businessTerm = binding.getBT();
		binding.setUsed(true);
		value = value.trim();
		System.out.println("- 0 fill Data boughMap="+boughMap.toString()+id+"("+semSort+")"+businessTerm+"="+value);

		String rowMapKey = "";
		for (Map.Entry<Integer, Integer> entry : boughMap.entrySet()) {
			Integer boughSort = entry.getKey();
			Integer seq = entry.getValue();
			rowMapKey += (boughSort+"="+seq+" ");
		}
		rowMap = new TreeMap<>();
		rowMapKey = rowMapKey.trim();
		if (rowMapList.containsKey(rowMapKey)) {
			rowMap = rowMapList.get(rowMapKey);
		}
		rowMap.put(semSort, value);
		rowMapList.put(rowMapKey, rowMap);
	}
	
	/**
	 * デジタルインボイスのXMLインスタンス文書を読み込み、セマンティックモデルの階層定義に従って親要素から子要素のXPathを使用して探し出し、その値をTidy data定義用の2次元リストに設定する。
	 * 
	 * @param parent 親のXML要素
	 * @param sort セマンティックモデル定義における親要素のセマンティックソート番号
	 * @param boughMap　要素が定義されたTidy dataの行に対応する索引
	 */
	private static void fillGroup (
			Node parent, 
			Integer sort, 
			TreeMap<Integer, Integer> boughMap ) {
		
		rowMap = new TreeMap<Integer, String>();
		
		// get child Nodes
		Binding binding = FileHandler.semBindingMap.get(sort);
		String id = binding.getID();
		String businessTerm = binding.getBT();

		TreeMap<Integer, List<Node>> childList = FileHandler.getChildren(parent, id);
		
		if (0==childList.size()) {
			System.out.println("- 0 fill Group boughMap="+boughMap.toString()+id+"("+sort+")"+businessTerm+" is Empty" );
			return;
		}
   	
		for (Integer childSort : childList.keySet()) {
			// childList includes both #text and @attribute
			Binding childBinding = (Binding) FileHandler.semBindingMap.get(childSort);
            String childID = childBinding.getID();
    		String childBusinessTerm = childBinding.getBT();
    		String childXPath = childBinding.getXPath();
    		int childLevel = Integer.parseInt(childBinding.getLevel());
			System.out.println("- 1 fill Group "+childID+"("+childSort+")"+childBusinessTerm+" "+childXPath);
          
            List<Node> children = childList.get(childSort);
            
            Integer countChildren = children.size();             
            if (countChildren > 0) {
	            for (int i = 0; i < countChildren; i++) {
	            	Node child = children.get(i);
		        	if (childID.toLowerCase().matches("jbt-.+$")) {
	        			String value = null;
	        			value = child.getTextContent().trim();
		            	if (null != value && value.length() > 0) {
//		            		if (! "#text".equals(child.getNodeName()))
//		            			continue; // @attribute has already registered as a grand child in the procedure below if clause.
	            			System.out.println("* 1 fill Data child["+i+"]"+childID+"("+childSort+")"+child.getNodeName()+"="+value);
		            		
			            	fillData(childSort, value, boughMap);
			            	
			        		if (FileHandler.childMap.containsKey(childSort)) {
			        			ArrayList<Integer> grandchildren = FileHandler.childMap.get(childSort);
			        			for (Integer grandchildSort : grandchildren) {
			        				Binding grandchildBiunding =  (Binding) FileHandler.semBindingMap.get(grandchildSort);
			        				String grandchildID = grandchildBiunding.getID();
			        				String grandchildBT = grandchildBiunding.getBT();
//			        				String grandchildXPath = grandchildBiunding.getXPath();
				                	ParsedNode parsedNode = FileHandler.nodeMap.get(grandchildSort);
				                	List<Node> grandchildNodes = parsedNode.nodes;
				            		for (int j = 0; j < grandchildNodes.size(); j++) {
				            			Node grandchild = grandchildNodes.get(j);
				            			String grandchildName = grandchild.getNodeName();
				        				String grandchildValue = grandchild.getTextContent().trim();
				            			System.out.println("* 2 fill Data boughMap"+boughMap.toString()+"child "+child.getNodeName()+" "+childID+
				            					" grandchild("+grandchildSort+")"+grandchildID+" level="+childLevel+" "+ childBusinessTerm+"->"+grandchildBT);
				            			System.out.println("    grand child["+j+"]"+grandchildName+"="+grandchildValue);

				            			fillData(grandchildSort, grandchildValue, boughMap);
				            		}
			        			}
			        		}
		            	}
		            } else {
			        	@SuppressWarnings("unchecked")
						TreeMap<Integer,Integer> boughMap1 = (TreeMap<Integer, Integer>) boughMap.clone();
		            	boolean is_multiple = isMultiple(childSort);
		                if (is_multiple && countChildren > 1) {
		                	Integer lastkey = boughMap1.lastKey();
		                	Integer lastvalue = boughMap1.get(lastkey);
		                	System.out.print("    boughMap1 lastKey="+lastkey+" child is multiple level="+childLevel);
			            	if (childSort != lastkey) {
			            		if (boughMap.size() < childLevel + 1) {
			                		boughMap1.put(childSort, i);
			            		} else {
			            			boughMap1.pollLastEntry();
			            			boughMap1.put(childSort, i);
			            			boughMapList.remove(boughMapList.size() - 1);
			            		}
			            	} else if (countChildren > 1) {
			            		Integer lastvalue1 = lastvalue + 1;
			            		boughMap1.put(lastkey, lastvalue1);
			            	}
			            	boughMapList.add(boughMap1);
			            	System.out.println("    UPDATED boughMapList="+boughMapList.toString()+" boughMap1="+boughMap1.toString());
		                }
	                	System.out.println("* fill Group "+childID+" boughMapList="+boughMapList.toString()+" boughMap1"+boughMap1.toString()+
	                			" child("+childSort+") level="+childLevel+" "+ businessTerm+"->"+childBusinessTerm);

	                	fillGroup(child, childSort, boughMap1);
		            }
	            }
            }
        }
	}

	/**
	 * セマンティックソート番号 semSortで指定された要素がXML DOM Documentに複数あるか判定する.<br>
	 * なお、FileHandler.MULTIPLE_IDで指定された要素も、複数と判定する.
	 * 
	 * @param semSort セマンティックソート番号.
	 * 
	 * @return multiple 複数であればtrue.　存在しないか1件しかなければfalse.
	 */
	private static boolean isMultiple(Integer semSort) {
		boolean multiple = false;
		Binding binding = FileHandler.semBindingMap.get(semSort);
		String id = binding.getID();
		String xPath = binding.getXPath();
		xPath = FileHandler.stripSelector(xPath);
		List<Node> founds = FileHandler.getXPath(FileHandler.root, xPath);
		if (founds.size() > 1) {
			multiple = true;
		} else if (Arrays.asList(FileHandler.MULTIPLE_ID).contains(id.toLowerCase())) {
			multiple = true;
		}
		return multiple;
	}

}