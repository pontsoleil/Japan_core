package wuwei.japan_core.cius;

import java.util.HashSet;
import java.util.Set;

/**
 * セマンティックモデル定義と構文バインディング定義のための情報を保持するクラス
 */
public class Binding {
	Integer semSort;
	String  id;
	String  semPath;
	Integer level;
	String  businessTerm;
	String  defaultValue;
	String  card;
	String  datatype;
	Integer synSort;
	String  xPath;
	Set<String/*XPath*/> additionalXPath;
	String occur;
	boolean isUsed;
	
	/**
	 * セマンティックモデル定義の項目
	 * 
	 * @param semSort　セマンティックモデルの項目のソート順
	 * @param id 項目id
	 * @param semPath セマンティックモデルのPath
	 * @param level セマンティックモデルの階層
	 * @param businessTerm ビジネス項目名
	 * @param defaultValue 規定値
	 * @param card 繰り返し
	 * @param datatype セマンティックデータ型
	 * @param synSort 構文バインディングのXML要素のソート順
	 * @param xPath XML要素が定義された位置のXPath
	 * @param occur XML要素の出現回数指定
	 * @param fixed XML要素の固定値指定
	 */
	public Binding(Integer semSort, String id, String semPath, Integer level, String businessTerm, String defaultValue, String card, String datatype, Integer synSort, String xPath, String occur) {
		this.semSort         = semSort;
		this.id              = id;
		this.semPath         = semPath;
		this.level           = level;
		this.businessTerm    = businessTerm;
		this.defaultValue    = defaultValue;
		this.card            = card;
		this.datatype        = datatype;
		this.synSort         = synSort;
		this.xPath           = xPath;
		this.occur           = occur;
		this.additionalXPath = new HashSet<String>();
		this.isUsed = false;
	}
	
	// getter
	public Integer getSemSort() { return this.semSort; }
	public String  getID() { return this.id; }
	public String  getSemPath() { return this.semPath; }
	public Integer getLevel() { return this.level; }
	public String  getBT() { return this.businessTerm; }
	public String  getDefaultValue() { return this.defaultValue; }
	public String  getCard() { return this.card; }
	public String  getDatatype() { return this.datatype; }
	public Integer getSynSort() { return this.synSort; }
	public String  getXPath() { return this.xPath; }
	public String  getOccur() { return this.occur; }
	public boolean isUsed() { return this.isUsed; }
	public Set<String> getAdditionalXPath() { return this.additionalXPath; }
	
	// setter
	public Integer setSemSort(Integer x) { return this.semSort = x; }
	public String  setID(String x) { return this.id = x; }
	public String  setSemPath(String x) { return this.semPath = x; }
	public Integer setLevel(Integer x) { return this.level = x; }
	public String  setBT(String x) { return this.businessTerm = x; }
	public String  setDefaultValue(String x) { return this.defaultValue = x; }
	public String  setCard(String x) { return this.card = x; }
	public String  setDatatype(String x) { return this.datatype = x; }
	public Integer setSynSort(Integer x) { return this.synSort = x; }
	public String  setXPath(String x) { return this.xPath = x; }
	public String  setOccur(String x) { return this.occur = x; }
	public boolean setUsed(boolean x) { return this.isUsed = x; }
	public Set<String> addAdditionalXPath(String x) {
		additionalXPath.add(x);
		return this.additionalXPath;
	}	
}
