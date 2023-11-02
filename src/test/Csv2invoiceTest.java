package test;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import java.util.Arrays;
import java.util.List;

import wuwei.japan_core.cius.Csv2invoice;

public class Csv2invoiceTest {
	private List<String> fileList;

    @BeforeEach
    public void setUp() {
    	fileList = Arrays.asList(
    			"Ex-PINT","Ex1-minimum-PINT","Ex2-TaxAcctCur-PINT","Ex3-SumInv1-PINT","Ex4-SumInv2-PINT","Ex5-AllowanceCharge-PINT",
    			"Ex6-CorrInv-PINT","Ex7-Return.Quan.ItPr-PINT","Ex9-SumInv1andO-PINT"
    	    );
    }
      
    @Test
    public void processInvoice_PINT() {
    	for (String fileName : fileList) {
	    	String params = "JP-PINT data/csv/"+fileName+".csv data/xml/"+fileName+"2.xml T";
	        String[] args = params.split(" ");
	        Csv2invoice.main(args);
    	}
        assertTrue(true);
    }
    
    @Test
    public void processInvoice_SME() {
    	for (String fileName : fileList) {
	    	String params = "SME-COMMON data/csv/"+fileName+".csv data/xml/"+fileName.replace("PINT", "SME")+"2.xml T";
	        String[] args = params.split(" ");
	        Csv2invoice.main(args);
    	}
        assertTrue(true);
    }
}
