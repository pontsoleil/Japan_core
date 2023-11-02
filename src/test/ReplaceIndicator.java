package test;


import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class ReplaceIndicator {

	 public static void main(String[] args) {
		 String xPath, updatedXPath;
	        xPath = "/Invoice/cac:AllowanceCharge[cbc:ChargeIndicator=true()]/cbc:AllowanceChargeReasonCode";
	        updatedXPath = replaceChargeIndicator(xPath);
	        System.out.println(updatedXPath);
	        xPath = "/Invoice/cac:AllowanceCharge[cbc:ChargeIndicator=false()]/cbc:AllowanceChargeReasonCode";
	        updatedXPath = replaceChargeIndicator(xPath);
	        System.out.println(updatedXPath);
	    }

	    static String replaceChargeIndicator(String xPath) {
	        // 正規表現パターンを修正して、括弧内の内容もマッチするようにします。
	        String regex = "\\[(\\w+)=((true|false)\\(\\))\\]";

	        // 正規表現のコンパイル
	        Pattern pattern = Pattern.compile(regex);
	        Matcher matcher = pattern.matcher(xPath);

	        // 置換結果を保持する StringBuffer
	        StringBuffer updatedXPath = new StringBuffer();

	        // すべてのマッチを探して、それに対応する形式に置き換えます。
	        while (matcher.find()) {
	            // キャプチャグループから要素名と値（true()またはfalse()）を取得します。
	            String elementName = matcher.group(1);
	            String boolValue = matcher.group(2).equals("true()") ? "true" : "false";

	            // 新しい形式に置き換えます。
	            String replacement = String.format("[normalize-space(%s/text())='%s']", elementName, boolValue);

	            // 置換内容を matcher に適用します。
	            matcher.appendReplacement(updatedXPath, replacement);
	        }

	        // 残りの部分を追加します。
	        matcher.appendTail(updatedXPath);

	        return updatedXPath.toString();
	    }
	}