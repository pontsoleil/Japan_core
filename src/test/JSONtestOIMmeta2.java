package test;

import org.json.*;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

import wuwei.japan_core.utils.JSONHandler;

public class JSONtestOIMmeta2 {
    @SuppressWarnings("unchecked")
	public static void main(String[] args) {
        // Define column name list
        String[] columns = {"d_NC00", "d_NC39-NC46", "NC00-01", "NC00-04", "NC46-01"};

        // Create JSON object
        JSONObject json = new JSONObject();

        // Add documentInfo object
        JSONObject documentInfoObj = new JSONObject();
        documentInfoObj.put("documentType", "https://xbrl.org/2021/xbrl-csv");
        JSONObject namespacesObj = new JSONObject();
        namespacesObj.put("core", "http://www.xbrl.jp/audit-data-collection");
        namespacesObj.put("ns0", "http://www.example.com");
        namespacesObj.put("link", "http://www.xbrl.org/2003/linkbase");
        namespacesObj.put("iso4217", "http://www.xbrl.org/2003/iso4217");
        namespacesObj.put("xsi", "http://www.w3.org/2001/XMLSchema-instance");
        namespacesObj.put("xbrli", "http://www.xbrl.org/2003/instance");
        namespacesObj.put("xbrldi", "http://xbrl.org/2006/xbrldi");
        namespacesObj.put("xlink", "http://www.w3.org/1999/xlink");
        documentInfoObj.put("namespaces", namespacesObj);
        JSONArray taxonomyArr = new JSONArray();
        taxonomyArr.add("../taxonomy/core/core.xsd");
        documentInfoObj.put("taxonomy", taxonomyArr);
        json.put("documentInfo", documentInfoObj);

        // Add tableTemplates object
        JSONObject tableTemplatesObj = new JSONObject();
        JSONObject coreObj = new JSONObject();
        JSONObject columnsObj = new JSONObject();
        for (String column : columns) {
            JSONObject columnObj = new JSONObject();
            if (column.startsWith("d_")) {
                columnsObj.put(column,new JSONObject());
            } else if (column.equals("NC46-01")) {
                JSONObject dimensionsObj = new JSONObject();
                dimensionsObj.put("concept", "core:NC46-01");
                dimensionsObj.put("unit", "iso4217:JPY");
                columnObj.put("dimensions", dimensionsObj);
                columnsObj.put(column,columnObj);
            } else {
                String conceptName = column.replace("-", ":");
                JSONObject dimensionsObj = new JSONObject();
                dimensionsObj.put("concept", "core:" + conceptName);
                columnObj.put("dimensions", dimensionsObj);
                columnsObj.put(column,columnObj);
            }
            
        }
        coreObj.put("columns", columnsObj);
        JSONObject dimensionsObj = new JSONObject();
        dimensionsObj.put("core:d_NC00", "$d_NC00");
        dimensionsObj.put("core:d_NC39-NC46", "$d_NC39-NC46");
        dimensionsObj.put("period", "2023-11-01T00:00:00");
        dimensionsObj.put("entity", "ns0:Example co.");
        coreObj.put("dimensions", dimensionsObj);
        tableTemplatesObj.put("core", coreObj);
        json.put("tableTemplates", tableTemplatesObj);

        // Add tables object
        JSONObject tablesObj = new JSONObject();
        JSONObject coreTablesObj = new JSONObject();
        coreTablesObj.put("url", "core-instances.csv");
        tablesObj.put("core", coreTablesObj);
        json.put("tables", tablesObj);
        
        // create a JSON object from the invoice Map using JSONHandler
        JSONHandler jsonHandler = new JSONHandler();
        JSONObject jsonObj = jsonHandler.convertMapToJSONObject(json);
        
        // print the JSON object
        System.out.println(jsonObj.toJSONString());

        // Write JSON object to file
        JSONHandler.writeJSONToFile(jsonObj, "src/test/test.json");
    }
}
