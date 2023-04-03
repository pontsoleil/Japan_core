<?php
/**
 * source2target.php
 *
 * convert source e-Invoice XML document to target  e-Invoice XML document
 *
 * designed by SAMBUICHI, Nobuyuki (Sambuichi Professional Engineers Office)
 * written by SAMBUICHI, Nobuyuki (Sambuichi Professional Engineers Office)
 *
 * MIT License
 *
 * (c) 2023 SAMBUICHI Nobuyuki (Sambuichi Professional Engineers Office)
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 **/
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
            "\r" => "",
            "\n" => "",
            '"' => '\\"',
        )
    );
}

// 定義したエラーハンドラを設定する
$old_error_handler = set_error_handler("errorHandler");

chdir(__DIR__);
wh_log($_SERVER['REQUEST_METHOD']);
if ($_SERVER['REQUEST_METHOD'] === 'POST')
{
    $uuid = UUID::v4();
    $syntax = htmlspecialchars($_POST["syntax"]);
    list($source, $target) = explode('_', $syntax);
    if (isset($_FILES['file'])) {
        $file_tmp = $_FILES['file']['tmp_name'];
        $basename = basename($_FILES['file']['name']);
        $file_dirFrom = 'data/source/xml/'.$source.'/';
        $source_xml = $file_dirFrom . $basename;
        if (move_uploaded_file($file_tmp, $source_xml)) {
            wh_log("moved uploaded file to {$source_xml}");
        }
        else {
            echo "Possible file upload failure!<br>\n";
            echo 'Failed to move uploaded file to {$source_xml}';
            return FALSE;
        }
    }
    else {
        $basename = htmlspecialchars($_POST["selected"]);
        $file_dirFrom = $source . '/';
        $source_xml = $file_dirFrom . $basename;
    }
    list($filename, $extension) = explode('.', $basename);
    $file_dirCSV = 'data/target/csv/';
    $csv_basename = $filename . '.csv';
    $csv_file = $file_dirCSV . $csv_basename;
    $workfile = $file_dirCSV . $filename . '_work.csv';
    $transposed_file = $file_dirCSV . $filename . '_transposed.csv';

    $file_dirTo = 'data/target/xml/'.$target.'/';
    $target_xml = $file_dirTo . $basename;

    $cmd1 = 'java -classpath lib/core-japan-0.0.2.jar wuwei.japan_core.cius.Invoice2csv '.$source.' "'.$source_xml.'" "'.$csv_file.'"';
    exec($cmd1,$output1,$retval1);
    wh_log($cmd1.'returns '.$retval1);
    if ($retval1 > 0)
    {
        trigger_error("Failed {$retval1}<br />\n{$cmd1}<br />\n{$output1}", E_USER_ERROR);
    }

    $cmd2 = 'python3 transpose.py "'.$csv_file.'" -c "'.$workfile.'" -t "'.$transposed_file.'"';
    exec($cmd2,$output2,$retval2);
    wh_log($cmd2.'returns '.$retval2);
    if ($retval2 > 0)
    {
        trigger_error("Failed {$retval2}<br />\n$cmd2}<br />\n{$output2}", E_USER_ERROR);
    }

    $cmd3 = 'java -classpath lib/core-japan-0.0.2.jar wuwei.japan_core.cius.Csv2invoice '.$target.' "'.$csv_file.'" "'.$target_xml.'"';
    exec($cmd3,$output3,$retval3);
    wh_log($cmd3.'returns '.$retval3);
    if ($retval3 > 0)
    {
        trigger_error("Failed {$retval3}<br />\n{$cmd3}<br />\n{$output3}", E_USER_ERROR);
    }

    $source_contents = file_get_contents($source_xml);
    wh_log($source_xml.' source contents: '.substr($source_contents,0,1024));
    $transposed_contents = file_get_contents($transposed_file);
    wh_log($transposed_file.' transposed contents: '.substr($transposed_contents,0,1024));
    $csv_contents = file_get_contents($csv_file);
    wh_log($csv_file.' csv contents: '.substr($csv_contents,0,1024));
    $target_contents = file_get_contents($target_xml);
    wh_log($target_xml.' target contents: '.substr($target_contents,0,1024));

    header("HTTP/1.1 200 OK");
    header("Content-Type: application/json; charset=utf-8");
    echo json_encode(
        array(
            'uuid'=>$uuid,
            'source'=>$source,
            'target'=>$target,
            'source_xml'=>$source_xml,
            'csv_file'=>$csv_file,
            'transposed_file'=>$transposed_file,
            'target_xml'=>$target_xml,
            'source_contents'=>$source_contents,
            'csv_contents'=>$csv_contents,
            'transposed_contents'=>$transposed_contents,
            'target_contents'=>$target_contents,
        ),
        JSON_UNESCAPED_UNICODE
    );
}
else {
    echo "NOT POST";
}
// source2target.phhp 2023-03-31