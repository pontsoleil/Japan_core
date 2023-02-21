package wuwei.japan_core.utils;

import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStream;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import javax.xml.transform.OutputKeys;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerException;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;

import org.w3c.dom.CDATASection;
import org.w3c.dom.Comment;
import org.w3c.dom.Document;
import org.w3c.dom.Element;

/**
 * 
 * https://mkyong.com/java/how-to-create-xml-file-in-java-dom/#write-xml-to-a-file
 * 
 *
 */
public class WriteXmlDom {

	/**
	 * XML DOM DocumentをXMLインスタンス文書としてファイル出力する.
	 * 
	 * @param args 使用しない
	 * @throws ParserConfigurationException 構成パラメタ不正
	 * @throws TransformerException         変換処理不正
	 */
	public static void main(String[] args)
			throws ParserConfigurationException, TransformerException {

		DocumentBuilderFactory docFactory = DocumentBuilderFactory.newInstance();
		DocumentBuilder docBuilder = docFactory.newDocumentBuilder();

		// root elements
		Document doc = docBuilder.newDocument();
		Element rootElement = doc.createElement("company");
		doc.appendChild(rootElement);

		// staff 1001
		// add xml elements
		Element staff = doc.createElement("staff");
		// add staff to root
		rootElement.appendChild(staff);
		// add xml attribute
		staff.setAttribute("id", "1001");

		// alternative
		// Attr attr = doc.createAttribute("id");
		// attr.setValue("1001");
		// staff.setAttributeNode(attr);

		Element name = doc.createElement("name");
		// JDK 1.4
		// name.appendChild(doc.createTextNode("mkyong"));
		// JDK 1.5
		name.setTextContent("mkyong");
		staff.appendChild(name);

		Element role = doc.createElement("role");
		role.setTextContent("support");
		staff.appendChild(role);

		Element salary = doc.createElement("salary");
		salary.setAttribute("currency", "USD");
		salary.setTextContent("5000");
		staff.appendChild(salary);

		// add xml comment
		Comment comment = doc.createComment(
				"for special characters like < &, need CDATA");
		staff.appendChild(comment);

		Element bio = doc.createElement("bio");
		// add xml CDATA
		CDATASection cdataSection = doc.createCDATASection("HTML tag <code>testing</code>");
		bio.appendChild(cdataSection);
		staff.appendChild(bio);

		// staff 1002
		Element staff2 = doc.createElement("staff");
		// add staff to root
		rootElement.appendChild(staff2);
		staff2.setAttribute("id", "1002");

		Element name2 = doc.createElement("name");
		name2.setTextContent("yflow");
		staff2.appendChild(name2);

		Element role2 = doc.createElement("role");
		role2.setTextContent("admin");
		staff2.appendChild(role2);

		Element salary2 = doc.createElement("salary");
		salary2.setAttribute("currency", "EUD");
		salary2.setTextContent("8000");
		staff2.appendChild(salary2);

		Element bio2 = doc.createElement("bio");
		// add xml CDATA
		bio2.appendChild(doc.createCDATASection("a & b"));
		staff2.appendChild(bio2);

		// コンソールにメッセージとして出力
		// writeXml(doc, System.out);
		// ファイルに出力
		try (FileOutputStream output = new FileOutputStream("data/xml/staff-dom.xml")) {
			writeXml(doc, output);
		} catch (IOException e) {
			e.printStackTrace();
		}

	}

	// 出力ストリームに出力する
	public static void writeXml(Document doc,
			OutputStream output)
			throws TransformerException {
		TransformerFactory transformerFactory = TransformerFactory.newInstance();
		Transformer transformer = transformerFactory.newTransformer();
		DOMSource source = new DOMSource(doc);
		StreamResult result = new StreamResult(output);
		// 整形して出力
		transformer.setOutputProperty(OutputKeys.INDENT, "yes");
		transformer.transform(source, result);

	}
}