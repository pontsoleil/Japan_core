package test;

import java.util.HashMap;
import java.util.Map;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.JSONValue;

public class JSONtest2 {

    @SuppressWarnings("unchecked")
	public static void main(String[] args) {
     
        // Create a JSON object for person 1
        JSONObject person1 = new JSONObject();
        person1.put("name", "John");
        person1.put("age", 30);
        person1.put("key", "http://www.example.com/foo/bar");
        
        // Create a JSON object for person 2
        JSONObject person2 = new JSONObject();
        person2.put("name", "Mary");
        person2.put("age", 25);
        
        // Create a JSON array and add the two JSON objects to it
        JSONArray jsonArray = new JSONArray();
        jsonArray.add(person1);
        jsonArray.add(person2);
        
        // Print the JSON array
        System.out.println(jsonArray.toString());
    }
}