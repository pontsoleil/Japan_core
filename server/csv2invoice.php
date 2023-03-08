<?php
class UUID {
// https://www.php.net/manual/ja/function.uniqid.php
// 141 Andrew Moore
    public static function v4() {
        return sprintf('%04x%04x-%04x-%04x-%04x-%04x%04x%04x',
            // 32 bits for "time_low"
            mt_rand(0, 0xffff), mt_rand(0, 0xffff),
            // 16 bits for "time_mid"
            mt_rand(0, 0xffff),
            // 16 bits for "time_hi_and_version",
            // four most significant bits holds version number 4
            mt_rand(0, 0x0fff) | 0x4000,
            // 16 bits, 8 bits for "clk_seq_hi_res", 8 bits for "clk_seq_low",
            // two most significant bits holds zero and one for variant DCE1.1
            mt_rand(0, 0x3fff) | 0x8000,
            // 48 bits for "node"
            mt_rand(0, 0xffff), mt_rand(0, 0xffff), mt_rand(0, 0xffff)
        );
    }
    public static function is_valid($uuid) {
        return preg_match('/^\{?[0-9a-f]{8}\-?[0-9a-f]{4}\-?[0-9a-f]{4}\-?'.
                          '[0-9a-f]{4}\-?[0-9a-f]{12}\}?$/i', $uuid) === 1;
    }
}

function escaped_entities($string) {
    return strtr(
        $string, 
        array(
            " " => "&nbsp;",
            "\n" => "<br/>",
            "<" => "&lt;",
            ">" => "&gt;",
            '"' => "&quot;",
            "'" => "&apos;",
            "&" => "&amp;",
        )
    );
}
error_log("csv2invoice.php debugging info:");
error_log($_SERVER);
error_log($_FILES);
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['file'])) {

    chdir(__DIR__);
    $uuid = UUID::v4();
    $syntax = htmlspecialchars($_POST["syntax"]);
    $file_tmp = $_FILES['file']['tmp_name'];
    $path = 'data/xml/';
    $basename = basename($_FILES['file']['name']);
    $csvfile = $path . $basename;
    list($filename, $extension) = explode('.', $basename);
    $xmlfile = $path . $filename . ".csv";
    if (move_uploaded_file($file_tmp, $csvfile)) {
        $cmd = "java -classpath core-japan-0.0.1.jar wuwei.japan_core.cius.Csv2invoice {$syntax} {$xmlfile} {$csvfile}";
        exec($cmd,$output,$retval);
        $csv_contents = file_get_contents($csvfile);
        $xml_contents = file_get_contents($xmlfile);
        header("HTTP/1.1 200 OK");
        header("Content-Type: application/json; charset=utf-8");
        echo json_encode(
            array(
                'return'=>$retval,
                'uuid'=>$uuid,
                'syntax'=>$syntax,
                'csvfile'=>$basename,
                'xmlfile'=> $filename . ".xml",
                'csv_contents'=>$csv_contents,
                'xml_contents'=>$xml_contents,
            ),
            JSON_UNESCAPED_UNICODE
        );
    } else {
        echo "Possible file upload failure!<br>\n";
        echo 'Here is some more debugging info:';
    }      
}
else {
    echo "NOT POST";
}
