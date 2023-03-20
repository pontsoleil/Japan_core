<?php
function wh_log($log_msg) {
    $log_filename = "log";
    if (!file_exists($log_filename))
    {
        // create directory/folder uploads.
        mkdir($log_filename, 0777, true);
    }
    $log_file_data = $log_filename.'/log_' . date('d-M-Y') . '.log';
    file_put_contents($log_file_data, $log_msg . "\n", FILE_APPEND);
}
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

chdir(__DIR__);
// wh_log(__DIR__);
wh_log($_SERVER['REQUEST_METHOD']);
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['file'])) {
    $uuid = UUID::v4();
    $syntax = htmlspecialchars($_POST["syntax"]);
    $file_tmp = $_FILES['file']['tmp_name'];
    $basename = basename($_FILES['file']['name']);
    $file_dirXML = 'data/' . $syntax . '/';
    $xmlfile = $file_dirXML . $basename;
    list($filename, $extension) = explode('.', $basename);
    $file_dirCSV = 'data/CSV/';
    $csvbasename = $filename . '.csv';
    $csvfile = $file_dirCSV . $csvbasename;
    $workfile = $file_dirCSV . $filename . '_work.csv';
    $transposedfile = $file_dirCSV . $filename . '_transposed.csv';
    if (move_uploaded_file($file_tmp, $xmlfile)) {
        $cmd1 = "java -classpath core-japan-0.0.1.jar wuwei.japan_core.cius.Invoice2csv {$syntax} {$xmlfile} {$workfile}";
        wh_log($cmd1);
        
        exec($cmd1,$output1,$retval1);

        $cmd2 = "python3 transpose.py {$workfile} -c {$csvfile} -t {$transposedfile}";
        wh_log($cmd2);

        exec($cmd2,$output2,$retval2);

        $transposed_contents = file_get_contents($transposedfile);
        wh_log('transposed contents : '.substr($transposed_contents,0,1000));

        $csv_contents = file_get_contents($csvfile);
        wh_log('csv contents : '.substr($csv_contents,0,1000));

        header("HTTP/1.1 200 OK");
        header("Content-Type: application/json; charset=utf-8");
        echo json_encode(
            array(
                'return'=>$retval2,
                'uuid'=>$uuid,
                'syntax'=>$syntax,
                'xmlfile'=>$basename,
                'csvfile'=>$csvbasename,
                'transposed_contents'=>$transposed_contents,
                'csv_contents'=>$csv_contents,
            ),
            JSON_UNESCAPED_UNICODE
        );
    } else {
        echo "Possible file upload failure!<br>\n";
        echo 'Here is some more debugging info:';
        print_r($_FILES);                
    }      
}
else {
    echo "NOT POST";
}