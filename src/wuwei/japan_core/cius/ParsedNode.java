package wuwei.japan_core.cius;

import java.util.List;

import org.w3c.dom.Node;

/**
 * セマンティックモデル定義と構文バインディング定義のための情報を保持するBindingと
 * それに対応するXMLインスタンス文書を読み取って取得したXML DOM DocumentのNode情報リストから定義されたクラス
 *
 */
public class ParsedNode {
	public Binding binding;
	public List<Node> nodes;
	
	/**
	 * コンストラクタ
	 * 
	 * @param binding セマンティックモデル定義と構文バインディング定義のための情報を保持するBinding
	 * @param nodes XMLインスタンス文書を読み取って取得したXML DOM DocumentのNode情報リスト
	 */
	public ParsedNode(Binding binding, List<Node> nodes) {
		this.binding = binding;
		this.nodes = nodes;
	}
}