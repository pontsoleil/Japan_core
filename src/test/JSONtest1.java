package test;

import java.util.HashMap;
import java.util.Map;

import org.json.simple.JSONObject;

import wuwei.japan_core.utils.JSONHandler;

public class JSONtest1 
{
	    @SuppressWarnings("unchecked")
		public static void main(String[] args) {
	        // create a nested Map representing an invoice
	        Map<String, Object> invoice = new HashMap<>();
	        invoice.put("invoiceNumber", "123456");
	        invoice.put("date", "2023-04-17");
	        
	        Map<String, Object> customer = new HashMap<>();
	        customer.put("name", "John Doe");
	        customer.put("email", "john.doe@example.com");
	        
	        Map<String, Object> address = new HashMap<>();
	        address.put("street", "123 Main St");
	        address.put("city", "Anytown");
	        address.put("state", "CA");
	        address.put("zip", "12345");
	        
	        customer.put("address", address);
	        invoice.put("customer", customer);
	        
	        Map<String, Object> items = new HashMap<>();
	        
	        Map<String, Object> item1 = new HashMap<>();
	        item1.put("description", "Widget");
	        item1.put("quantity", 2);
	        item1.put("price", 9.99);
	        
	        Map<String, Object> item2 = new HashMap<>();
	        item2.put("description", "Gadget");
	        item2.put("quantity", 1);
	        item2.put("price", 19.99);
	        
	        items.put("item1", item1);
	        items.put("item2", item2);
	        
	        invoice.put("items", items);
	        
	        // create a JSON object from the invoice Map using JSONHandler
	        JSONHandler jsonHandler = new JSONHandler();
	        JSONObject jsonObj = jsonHandler.convertMapToJSONObject(invoice);
	        
	        // print the JSON object
	        System.out.println(jsonObj.toJSONString());

	        // To write a Map<String, Object> to a JSON file
	        jsonHandler.writeJSONToFile(jsonObj, "src/test/test.json");
	        
	    }
}
