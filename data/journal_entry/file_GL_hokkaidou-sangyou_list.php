<?php
  $dir = __DIR__ . '/' . 'XBRL_GLinstances'; // ファイル一覧を取得するディレクトリ
  $files = array_diff(scandir($dir), array('.', '..')); // ディレクトリ内のファイル一覧を取得
  header('Content-Type: application/json'); // レスポンスのContent-TypeをJSONに設定
  echo json_encode($files); // ファイル名の配列をJSON形式で出力
?>