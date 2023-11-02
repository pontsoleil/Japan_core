package test;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import java.util.Arrays;
import java.util.List;

import wuwei.japan_core.cius.Invoice2csv;

public class Invoice2csvTest {
	private List<String> fileList;

    @BeforeEach
    public void setUp() {
//    	fileList = Arrays.asList("Ex5-AllowanceCharge-PINT");
    	fileList = Arrays.asList(
    			"Ex-PINT","Ex1-minimum-PINT","Ex2-TaxAcctCur-PINT","Ex3-SumInv1-PINT","Ex4-SumInv2-PINT","Ex5-AllowanceCharge-PINT",
    			"Ex6-CorrInv-PINT","Ex7-Return.Quan.ItPr-PINT","Ex9-SumInv1andO-PINT"
    	    );
    }
    
    @Test
    public void processCSV_PINT() {
    	for (String fileName : fileList) {
	    	String params = "JP-PINT data/xml/"+fileName+".xml data/csv/"+fileName+".csv T";
	        String[] args = params.split(" ");
	        Invoice2csv.main(args);
    	}
        assertTrue(true);
    }
}
