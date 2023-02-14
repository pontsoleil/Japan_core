package wuwei.japan_core.utils;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.nio.charset.Charset;
import java.util.ArrayList;
/**
 * RFC4180形式のCSVファイルとの入出力を制御するクラス.
 * 『Java：CSVパーサを作る - RFC4180対応』　[山中秀一氏]を参考に一部改変しています。
 * http://endeavour.cocolog-nifty.com/developer_room/2008/06/javacsv_793b.html<br>
 * RFC4180<br>
 * https://www.rfc-editor.org/rfc/rfc4180.txt
 *
 */
public class CSV {
	public static ArrayList<String> columns         = new ArrayList<>();
	public static ArrayList<ArrayList<String>> data = new ArrayList<>();

    /**
     * x
     * @param args
     */
	public static void main(String[] args) 
    {
    	String IN_CSV = "CIUS/data/csv/Example0.csv";
    	String OUT_CSV = "CIUS/data/csv/Example0_out.csv";
    	String CHARSET = "UTF-8";

    	try {
			data = csvFileRead(IN_CSV, CHARSET);
		} catch (FileNotFoundException e) {
			System.out.println("File not found "+IN_CSV);
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
    	
    	try {
    		csvFileWrite(data, OUT_CSV, CHARSET);
		} catch (FileNotFoundException e) {
			System.out.println("File not found "+OUT_CSV);
			e.printStackTrace();
		} catch (Exception e) {
			e.printStackTrace();
		}

    	try {
			data = csvFileRead(OUT_CSV, CHARSET);
		} catch (FileNotFoundException e) {
			System.out.println("File not found "+OUT_CSV);
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
    }
    
	public static void csvFileWrite(
			ArrayList<ArrayList<String>> data,
			String filename, 
			String charset ) 
		throws 
			FileNotFoundException, 
			IOException 
	{
		System.out.println("- csvFileWrite " + filename + " " + charset);
		FileOutputStream fileOutputStream = new FileOutputStream(filename);

		writeFile(fileOutputStream, data, charset);
		
		fileOutputStream.close();
	}

	public static void writeFile(
			FileOutputStream stream,
			ArrayList<ArrayList<String>> data,
			String charset ) 
	{
		OutputStreamWriter outputStreamWriter = null;
		BufferedWriter bufferedWriter         = null;
		try {
			Charset cs         = Charset.forName(charset);
			outputStreamWriter = new OutputStreamWriter(stream, cs);
			bufferedWriter     = new BufferedWriter(outputStreamWriter);
			for (ArrayList<String> columns : data) {
				for (int i=0; i < columns.size(); i++) {
					String cell_value = columns.get(i);
					if (cell_value.indexOf("\"") != -1 || cell_value.indexOf(",") != -1) {
						cell_value = "\"" + cell_value.replaceAll("\"", "\"\"") + "\"";
					}
					bufferedWriter.write(cell_value);
					System.out.print(cell_value);
					if (i < columns.size() - 1) {
						bufferedWriter.write(",");
						System.out.print(",");
					}
				}
				bufferedWriter.write("\n");
				System.out.print("\n");
			}
		}
		catch (Exception ex) {
			ex.printStackTrace();
		}
		finally {
			try {
				if (bufferedWriter != null) {
					bufferedWriter.close();
				}
				if (outputStreamWriter != null) {
					outputStreamWriter.close();
				}
				stream.close();
			} catch (IOException ex) {
				ex.printStackTrace();
			}
		}
	}

	public static ArrayList<ArrayList<String>> csvFileRead(
			String filename, 
			String charset )
		throws
			FileNotFoundException,
			IOException
	{
		System.out.println("- csvFileRead " + filename + " " + charset);
		FileInputStream fileInputStream = new FileInputStream(filename);
		
		data = readFile(fileInputStream,charset);
		
        return data;
	}

	/**
	 * CSVファイルの読み込み。
	 * 
	 * @param stream 入力ストリーム。FileInputStream，ByteArrayInputStreamなど。
	 * @param charser 文字コードセット
	 * 
	 * @return data ２次元のArrayList
	 */
	public static ArrayList<ArrayList<String>> readFile(
			InputStream stream,
			String charset )
	{
		ArrayList<ArrayList<String>> data = new ArrayList<>();
		InputStreamReader inputSteramReader = null;
		BufferedReader bufferedReader = null;
		try {
			Charset cs = Charset.forName(charset);
			inputSteramReader = new InputStreamReader(stream, cs);
			bufferedReader    = new BufferedReader(inputSteramReader);
			String record;
			int lineNum = 0;
			while ((record = buildRecord(bufferedReader)) != null) {
				lineNum++;
				if (record.length() <= 0)
					continue;
				if (record.startsWith("#"))
					continue;
				
				columns = splitRecord(record);
				
				if (columns.size() <= 0)
					continue;
				if (0 < columns.size()) {
					System.out.println("line "+lineNum);
					for (String cell : columns)
						System.out.print(cell+"|");
				}
				System.out.println("");
				data.add(columns);
			}
		} catch (Exception ex) {
			ex.printStackTrace();
		} finally {
			try {
				if (bufferedReader != null) {
					bufferedReader.close();
				}
				if (inputSteramReader != null) {
					inputSteramReader.close();
				}
				stream.close();
			} catch (IOException ex) {
				ex.printStackTrace();
			}
		}
		return data;
	}

	/**
	 * レコードの確定
	 * レコード確定では，入力テキストデータに対して，ダブルクォーテーション（二重引用符）のペアをヒントに各レコードの末尾を確定して，レコードの切り分けを行います。
	 * 処理手順は以下のようになります。
	 * BufferedReaderのreadLineメソッドを使ってテキストを１行分（現在の位置から改行が現れるまで，またはファイルの終了まで）取り出して，行の先頭からダブルクォーテーションを探す。
	 * 見つからなければその１行を１レコードとして確定する。（readLineメソッドは「CR」「LF」「CRLF」を改行と認識するので，「CRLF以外の改行も考慮する」仕様の要求を満たしています。）
	 * ダブルクォーテーションが見つかった場合，ペアになる後ろのダブルクォーテーションを探す。後ろのダブルクォーテーションが見つかったらその位置から後続のダブルクォーテーションのペアを探す。
	 * この手順を行の終わりまで繰り返す。ダブルクォーテーションペアの外側で行が終了していれば，その行を１レコードとして確定する。
	 * ペアの後ろのダブルクォーテーションが見つからずにダブルクォーテーションペアの内側で改行に達したら，
	 * その改行を文字列フィールドに含まれる改行と見なしてBufferedReaderのreadLineメソッドより次の行を取り出して前の行と連結し，
	 * ペアの後ろのダブルクォーテーションを探すところから処理から継続する。これをダブルクォーテーションペアの外側で改行が見つかるまで繰り返す。
	 * 後ろのダブルクォーテーションが見つからずにファイルの末尾に達したときは，ファイルの末尾にダブルクォーテーションを付加して行の末尾とする。
	 * この連結した行を１レコードとして確定する。
	 */
	// ------------------------------------------------------------------
	/**
	 * BufferedReaderから1レコード分のテキストを取り出す。
	 * 
	 * @param reader 行データを取り出すBufferedReader。
	 * @return 1レコード分のテキスト。
	 * @throws IOException 入出力エラー
	 */
	public static String buildRecord(BufferedReader reader) throws IOException {
		String result = reader.readLine();
		int pos;
		if (result != null && 0 < result.length() && 0 <= (pos = result.indexOf("\""))) {
			boolean inString  = true;
			String rawline    = result;
			String newline    = null;
			StringBuffer buff = new StringBuffer(1024);
			while (true) {
				while (0 <= (pos = rawline.indexOf("\"", ++pos))) {
					inString = !inString;
				}
				if (inString && (newline = reader.readLine()) != null) {
					buff.append(rawline);
					buff.append("\n");
					pos     = -1;
					rawline = newline;
					continue;
				} else {
					if (inString || 0 < buff.length()) {
						buff.append(rawline);
						if (inString) {
							buff.append("\"");
						}
						result = buff.toString();
					}
					break;
				}
			}
		}
		return result;
	}

	/**
	 * レコードのフィールドへの分割
	 * フィールド分割では，レコードに切り分けたテキストに対して，最初にレコード全体をカンマで分割し，分割した個々の文字列にダブルクォーテーションをヒントに
	 * 必要な連結やエスケープ処理を行って，
	 * 個々のフィールドを確定します。処理手順は以下のようになります。
	 * レコード全体をStringクラスのsplitメソッドを使ってカンマで分割し，分割した個々の文字列データを順に先頭からダブルクォーテーションを探す。
	 * 見つからなければその文字列は１フィールドとして確定する。
	 * ダブルクォーテーションが見つかったら，次のダブルクォーテーションを探す。次のダブルクォーテーションの直後にダブルクォーテーションがあれば，
	 * エスケープされたダブルクォーテーションとして処理し，
	 * そうでなければフィールドの終わりと見なす。
	 * フィールドで後ろのダブルクォーテーションが見つからない場合，フィールドに含まれるカンマでsplitメソッドが分割したものと見なして，
	 * フィールドの後ろに（splitメソッドが削除した）カンマと次のフィールドを連結する。
	 * フィールドの開始と終了のダブルクォーテーションは削除する。
	 */
	/**
	 * 1レコード分のテキストを分割してフィールドの配列にする。
	 * 
	 * @param src  1レコード分のテキストデータ。
	 * @param dest フィールドの配列の出力先。
	 */
	public static ArrayList<String> splitRecord(String src) {
		ArrayList<String> dest = new ArrayList<>();
		String[] columns       = src.split(",");
		int maxlen             = columns.length;
		StringBuffer buff      = new StringBuffer(1024);
		int startPos, endPos, columnlen;
		String column;
		boolean isInString, isEscaped;
		for (int index = 0; index < maxlen; index++) {
			column = columns[index];
			if ((endPos = column.indexOf("\"")) < 0) {
				dest.add(column);
			} else {
				isInString = (endPos == 0);
				isEscaped  = false;
				columnlen  = column.length();
				startPos   = (isInString) ? 1 : 0;
				buff.setLength(0);
				while (startPos < columnlen) {
					if (0 <= (endPos = column.indexOf("\"", startPos))) {
						buff.append((startPos < endPos) ? column.substring(startPos, endPos) : isEscaped ? "\"" : "");
						isEscaped  = !isEscaped;
						isInString = !isInString;
						startPos   = ++endPos;
					} else {
						buff.append(column.substring(startPos));
						if (isInString && index < maxlen - 1) {
							column    = columns[++index];
							columnlen = column.length();
							buff.append(",");
							startPos = 0;
						} else {
							break;
						}
					}
				}
				dest.add(buff.toString());
			}
		}
		return dest;
	}

}
