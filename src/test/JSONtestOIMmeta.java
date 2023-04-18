package test;


import java.util.ArrayList;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

import wuwei.japan_core.utils.JSONHandler;

public class JSONtestOIMmeta 
{
/**
 * 
 {
    "documentInfo": {
        "documentType": "https://xbrl.org/2021/xbrl-csv",
        "namespaces": {
            "core": "http://www.xbrl.jp/audit-data-collection",
            "ns0": "http://www.example.com",
            "link": "http://www.xbrl.org/2003/linkbase",
            "iso4217": "http://www.xbrl.org/2003/iso4217",
            "xsi": "http://www.w3.org/2001/XMLSchema-instance",
            "xbrli": "http://www.xbrl.org/2003/instance",
            "xbrldi": "http://xbrl.org/2006/xbrldi",
            "xlink": "http://www.w3.org/1999/xlink"
        },
        "taxonomy": [
            "../taxonomy/core/core.xsd"
        ]
    },
    "tableTemplates": {
        "core": {
            "columns": {
                "d_NC00": {},
                "d_NC39-NC46": {},
                "NC00-01": {
                    "dimensions": {
                        "concept": "core:NC00-01"
                    }
                },
                "NC00-04": {
                    "dimensions": {
                        "concept": "core:NC00-04"
                    }
                },
                "NC46-01": {
                    "dimensions": {
                        "concept": "core:NC46-01"
                        "unit": "iso4217:JPY"
                    }
                },
            },
            "dimensions": {
                "core:d_NC00": "$d_NC00",
                "core:d_NC39-NC46": "$d_NC39-NC46",
                "period": "2023-11-01T00:00:00",
                "entity": "ns0:Example co."
            }
        }
    },
    "tables": {
        "core": {
            "url": "core-instances.csv"
        }
    }
}
 *
 */
	    @SuppressWarnings("unchecked")
		public static void main(String[] args) {
	    	Map<String, Object> documentInfo = new LinkedHashMap<>();
	    	documentInfo.put("documentType", "https://xbrl.org/2021/xbrl-csv");

	    	Map<String, String> namespaces = new LinkedHashMap<>();
	    	namespaces.put("adc", "http://www.xbrl.jp/audit-data-collection");
	    	namespaces.put("ns0", "http://www.example.com");
	    	namespaces.put("xlink", "http://www.w3.org/1999/xlink");
	    	documentInfo.put("namespaces", namespaces);

	    	String[] taxonomy = {"../taxonomy/ADC/core.xsd"};
	    	documentInfo.put("taxonomy", taxonomy);

	    	Map<String, Object> columns = new LinkedHashMap<>();
	    	
	    	
	    	Map<String, Object> column1 = new LinkedHashMap<>();
	    	columns.put("d_A025", column1);

	    	Map<String, Object> column2 = new LinkedHashMap<>();
	    	columns.put("d_A026", column2);

	    	Map<String, Object> column3 = new LinkedHashMap<>();
	    	Map<String, Object> dimensions1 = new LinkedHashMap<>();
	    	dimensions1.put("concept", "adc:A025-001");
	    	column3.put("dimensions", dimensions1);
	    	columns.put("A025-001", column3);

	    	Map<String, Object> column4 = new LinkedHashMap<>();
	    	Map<String, Object> dimensions2 = new LinkedHashMap<>();
	    	dimensions2.put("concept", "adc:A025-A026-008");
	    	column4.put("dimensions", dimensions2);
	    	columns.put("A025-A026-008", column4);

	    	Map<String, Object> column5 = new LinkedHashMap<>();
	    	Map<String, Object> dimensions3 = new LinkedHashMap<>();
	    	dimensions3.put("concept", "adc:A026-A089-001");
	    	dimensions3.put("unit", "iso4217:JPY");
	    	column5.put("dimensions", dimensions3);
	    	columns.put("A026-A089-001", column5);

	    	Map<String, Object> column6 = new LinkedHashMap<>();
	    	Map<String, Object> dimensions4 = new LinkedHashMap<>();
	    	dimensions4.put("concept", "adc:A026-A089-002");
	    	column6.put("dimensions", dimensions4);
	    	columns.put("A026-A089-002", column6);

	    	Map<String, Object> tableTemplates = new LinkedHashMap<>();
	    	Map<String, Object> adcTableTemplate = new LinkedHashMap<>();
	    	adcTableTemplate.put("columns", columns);

	    	Map<String, Object> dimensions = new LinkedHashMap<>();
	    	dimensions.put("adc:d_A025", "$d_A025");
	    	dimensions.put("adc:d_A026", "$d_A026");
	    	dimensions.put("period", "2023-11-01T00:00:00");
	    	dimensions.put("entity", "ns0:Example co.");
	    	adcTableTemplate.put("dimensions", dimensions);
	    	tableTemplates.put("adc", adcTableTemplate);

	    	Map<String, Object> tables = new LinkedHashMap<>();
	    	Map<String, Object> adcTable = new LinkedHashMap<>();
	    	adcTable.put("url", "adc-instances.csv");
	    	tables.put("adc", adcTable);

	    	Map<String, Object> json = new LinkedHashMap<>();
	    	json.put("documentInfo", documentInfo);
	    	json.put("tableTemplates", tableTemplates);
	    	json.put("tables", tables);

	        // create a JSON object from the invoice Map using JSONHandler
	        JSONHandler jsonHandler = new JSONHandler();
	        JSONObject jsonObj = jsonHandler.convertMapToJSONObject(json);
	        
	        // print the JSON object
	        System.out.println(jsonObj.toJSONString());

	        // To write a Map<String, Object> to a JSON file
	        jsonHandler.writeJSONToFile(jsonObj, "src/test/test.json");


	    }
}
