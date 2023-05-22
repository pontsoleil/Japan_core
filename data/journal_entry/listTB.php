<?php
  // dirの引数を取得
  if (isset($_GET['dir'])) {
    $name = $_GET['dir'];
  } else {
    $dir = './data/hokkaidou-sangyou/TB'; // ファイル一覧を取得するディレクトリ
  }
  $files = array_diff(scandir($dir), array('.', '..')); // ディレクトリ内のファイル一覧を取得
  header('Content-Type: application/json'); // レスポンスのContent-TypeをJSONに設定
  echo json_encode($files); // ファイル名の配列をJSON形式で出力
?>