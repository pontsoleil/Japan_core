package test;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;

public class SortTest {
    public static void main(String[] args) {
        ArrayList<ArrayList<String>> data = new ArrayList<>();
        data.add(new ArrayList<>(Arrays.asList("1230", "JC0a_11", "1", "", "/JC00/JC0a/JC0a_11", "ドメインID", "Identifier", "1290", "IBT-024", "Specification identifier", "An identification of the specification containing the total set of rules regarding semantic content, cardinalities and business rules to which the data contained in the instance document conforms.", "仕様ID", "取引プロセスのID。セマンティックコンテンツ、カーディナリティや、インスタンス文書に含まれているデータが準拠すべきビジネスルールに関するルール一式を含む、仕様を識別する。", "1010", "/Invoice/ cbc:CustomizationID", "1..1", "urn:peppol:pint:billing-1@jp-1")));
        data.add(new ArrayList<>(Arrays.asList("1010", "JC00", "0", "n", "/JC00", "請求書", "―", "1000", "IBG-00", "Invoice", "Commercial invoice", "請求書", "請求書", "1000", "/Invoice")));
        data.add(new ArrayList<>(Arrays.asList("1020", "JC0a", "0", "1", "/JC00/JC0a", "ヘッダ", "", "1002", "", "", "", "", "", "1005", "/Invoice", "0..1")));
        data.add(new ArrayList<>(Arrays.asList("1070", "JC0a_03", "1", "", "/JC00/JC0a/JC0a_03", "取引プロセスID", "Text", "1280", "IBT-023", "Business process type", "Identifies the business process context in which the transaction appears, to enable the Buyer to process the Invoice in an appropriate way.", "ビジネスプロセスタイプ", "取引プロセスの名称。買い手が適切な方法で請求書を処理することができるように、取引が行われたビジネスプロセスを識別する。", "1020", "/Invoice/ cbc:ProfileID", "1..1", "urn:peppol:bis:billing")));

        data.sort(Comparator.comparingInt(o -> Integer.parseInt(o.get(0))));

        for (ArrayList<String> row : data) {
            System.out.println(row);
        }
    }
}
