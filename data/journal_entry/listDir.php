<?php
if (isset($_GET['dir'])) {
    $dir = $_GET['dir'];
    $absolutePath = __DIR__ . '/' . $dir;

    if (preg_match('/^[a-zA-Z0-9\.\/_-]+$/', $dir)) {

      if (is_dir($absolutePath)) {
          $files = scandir($absolutePath);
          $fileList = array_diff($files, array('.', '..'));

          header('Content-Type: application/json');
          echo json_encode($fileList);
      } else {
          echo '指定されたディレクトリが存在しません。';
      }
    } else {
      // 正規表現にマッチしない場合の処理
      echo '無効なパラメータです。指定できるディレクトリ名は英数字及び . _ - / のみです。';
    }
} else {
    echo 'ディレクトリが指定されていません。';
}
?>
