<?php
if (isset($_GET['dir'])) {
    $dir = $_GET['dir'];
    $absolutePath = __DIR__ . '/' . $dir;

    if (is_dir($absolutePath)) {
        $files = scandir($absolutePath);
        $fileList = array_diff($files, array('.', '..'));

        header('Content-Type: application/json');
        echo json_encode($fileList);
    } else {
        echo '指定されたディレクトリが存在しません。';
    }
} else {
    echo 'ディレクトリが指定されていません。';
}
?>

