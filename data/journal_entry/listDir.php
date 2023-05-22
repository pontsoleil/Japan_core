<?php
  // dirの引数を取得
  $dir = isset($_GET['dir']) ? $_GET['dir'] : ''; // パラメータが存在しない場合は空文字列をデフォルト値とする

  if (preg_match('/^[a-zA-Z0-9\/-]+$/', $dir)) {
    // 正規表現にマッチする場合の処理
    $files = array_diff(scandir($dir), array('.', '..')); // ディレクトリ内のファイル一覧を取得
    header('Content-Type: application/json'); // レスポンスのContent-TypeをJSONに設定
    echo json_encode($files); // ファイル名の配列をJSON形式で出力
  } else {
      // 正規表現にマッチしない場合の処理
      echo '無効なパラメータです。指定できるディレクトリ名は英数字及び_-のみです';
  } 
?>