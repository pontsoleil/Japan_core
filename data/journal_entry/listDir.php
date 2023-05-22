<?php
$dir = isset($_GET['dir']) ? $_GET['dir'] : '';

if ($dir === '') {
    echo 'ディレクトリが指定されていません。';
} elseif (preg_match('/^[a-zA-Z0-9\/-]+$/', $dir)) {
    $dirPath = __DIR__ . '/' . $dir;
    $files = array_diff(scandir($dirPath), array('.', '..'));

    header('Content-Type: application/json');
    echo json_encode($files);
} else {
    echo '無効なパラメータです。指定できるディレクトリ名は英数字及び_-のみです。';
}
?>

