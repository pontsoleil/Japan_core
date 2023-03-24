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
 *
 */
public class XML_SchemeValidation {

	/**
 	 * The application's entry point
	 * @param args an array of command-line arguments for the application
	 */
	public static void main(String[] args) {
		String schema_file = args[0];
		String xml_file = args[1];
		boolean result = validateXMLSchema(schema_file, xml_file);
		System.out.println(xml_file + " validates against " + schema_file + " result=" +result);
//		data/pint-jp-resources-dev/trn-invoice/example/Japan PINT Invoice UBL Example.xml
//		System.out.println("EmployeeRequest.xml validates against Employee.xsd? " + validateXMLSchema("xml/UBL-2.1/xsd/maindoc/UBL-Invoice-2.1.xsd", "xml/Example4-SumInv2.xml"));
//		System.out.println("EmployeeRequest.xml validates against Employee.xsd? " + validateXMLSchema("data/aligned/maindoc/UBL-Invoice-2.1.xsd", "data/xml/JP-PINT/Example4-SumInv2_out.xml"));
	}

	/**
	 * 
	 * Copied from following page.<br>
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
			System.out.println("Exception: " + e.getMessage());
			return false;
		}
		return true;
	}
}