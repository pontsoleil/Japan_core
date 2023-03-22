<?php
// cf. https://www.php.net/manual/ja/function.set-error-handler.php
function errorHandler($errno, $errstr, $errfile, $errline)
{
    if (!(error_reporting() & $errno)) {
        // error_reporting 設定に含まれていないエラーコードのため、
        // 標準の PHP エラーハンドラに渡されます。
        return;
    }
    // $errstr はエスケープする必要があるかもしれません。
    $errstr = htmlspecialchars($errstr);
    switch ($errno) {
    case E_USER_ERROR:
        echo "<b>ERROR</b> [$errno] $errstr<br />\n";
        echo "  Fatal error on line $errline in file $errfile";
        echo ", PHP " . PHP_VERSION . " (" . PHP_OS . ")<br />\n";
        echo "Aborting...<br />\n";
        exit(1);
    case E_USER_WARNING:
        echo "<b>My WARNING</b> [$errno] $errstr<br />\n";
        break;
    case E_USER_NOTICE:
        echo "<b>My NOTICE</b> [$errno] $errstr<br />\n";
        break;
    default:
        echo "Unknown error type: [$errno] $errstr<br />\n";
        break;
    }
    /* PHP の内部エラーハンドラを実行しません */
    return true;
}

function wh_log($log_msg)
{
    $log_filename = "log";
    if (!file_exists($log_filename))
    {
        // create directory/folder uploads.
        mkdir($log_filename, 0777, true);
    }
    $log_file_data = $log_filename.'/log_' . date('d-M-Y') . '.log';
    file_put_contents($log_file_data, $log_msg . "\n", FILE_APPEND);
}

class UUID
{
// https://www.php.net/manual/ja/function.uniqid.php
// 141 Andrew Moore
    public static function v4()
    {
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
    public static function is_valid($uuid)
    {
        return preg_match('/^\{?[0-9a-f]{8}\-?[0-9a-f]{4}\-?[0-9a-f]{4}\-?'.
                          '[0-9a-f]{4}\-?[0-9a-f]{12}\}?$/i', $uuid) === 1;
    }
}

function escaped_entities($string)
{
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
wh_log($_SERVER['REQUEST_METHOD']);
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['file']))
{
    $uuid = UUID::v4();
    $syntax = htmlspecialchars($_POST["syntax"]);
    $file_tmp = $_FILES['file']['tmp_name'];
    $basename = basename($_FILES['file']['name']);
    $csv_file = 'data/source/csv/' . $basename;
    list($filename, $extension) = explode('.', $basename);
    $xml_basename = $filename . ".xml";
    $xml_file = 'data/target/xml/'.$syntax.'/' . $xml_basename;
    if (move_uploaded_file($file_tmp, $csv_file)) {
        $cmd = "java -classpath lib/core-japan-0.0.1.jar wuwei.japan_core.cius.Csv2invoice {$syntax} {$csv_file} {$xml_file}";
        exec($cmd,$output,$retval);
        wh_log($cmd.' returns '.$retval);
        if ($retval > 0)
        {
            trigger_error("Failed {$retval}<br />\n{$cmd}<br />\n{$output}", E_USER_ERROR);
        }

        $csv_contents = file_get_contents($csv_file);
        $xml_contents = file_get_contents($xml_file);
        wh_log($csv_file.' csv_contents: '.substr($csv_contents,0,1024));
        wh_log($xml_file.' xml_contents: '.substr($xml_contents,0,1024));

        header("HTTP/1.1 200 OK");
        header("Content-Type: application/json; charset=utf-8");
        echo json_encode(
            array(
                'uuid'=>$uuid,
                'syntax'=>$syntax,
                'csv_file'=>$csv_file,
                'xml_file'=>$xml_file,
                'csv_contents'=>$csv_contents,
                'xml_contents'=>$xml_contents,
            ),
            JSON_UNESCAPED_UNICODE
        );
    } else
    {
        echo "Possible file upload failure!<br>\n";
        echo 'Here is some more debugging info:';
    }
} else
{
    echo "NOT POST";
}
