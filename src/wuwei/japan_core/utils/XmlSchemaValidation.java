package wuwei.japan_core.utils;

import java.io.File;
import java.io.IOException;

import javax.xml.XMLConstants;
import javax.xml.transform.stream.StreamSource;
import javax.xml.validation.Schema;
import javax.xml.validation.SchemaFactory;
import javax.xml.validation.Validator;

import org.xml.sax.SAXException;

/**
 * XMLスキーマ検証
 */
public class XmlSchemaValidation {

	/**
 	 * The application's entry point
	 * @param args an array of command-line arguments for the application
	 */
	public static void main(String[] args) {
		String schema_file = args[0];
		String xml_file = args[1];
		boolean result = validateXMLSchema(schema_file, xml_file);
		if (result)
			System.out.println(xml_file + " は、 " + schema_file + " で定義されているXMLスキーマ定義に従った、妥当な定義内容です。");
		else
			System.out.println(xml_file + " は、 " + schema_file + " で定義されているXMLスキーマ定義に違反しています。");
	}

	/**
	 * 
	 * Reprinted from the page below.<br>
	 * https://www.digitalocean.com/community/tutorials/how-to-validate-xml-against-xsd-in-java
	 * 
	 * @param xsdPath XMLスキーマファイル
	 * @param xmlPath XMLインスタンス文書ファイル
	 * @return boolean XMLスキーマ検証結果
	 */
	public static boolean validateXMLSchema(String xsdPath, String xmlPath) {

		try {
			SchemaFactory factory = SchemaFactory.newInstance(XMLConstants.W3C_XML_SCHEMA_NS_URI);
			Schema schema = factory.newSchema(new File(xsdPath));
			Validator validator = schema.newValidator();
			validator.validate(new StreamSource(new File(xmlPath)));
		} catch (IOException | SAXException e) {
			String message = e.getMessage();
			message = message.replaceAll("\"urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2\"", "cbc");
			message = message.replaceAll("\"urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2\"", "cac");
			System.out.println("Exception: " + message);
			return false;
		}
		return true;
	}
}