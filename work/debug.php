<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['file'])) {
  // chdir(__DIR__);
  $tmpfile = $_FILES['file']['tmp_name'];
  $uploaddir = __DIR__ . 'data/xml/';
  $uploadfile = $uploaddir . basename($_FILES['file']['name']);
  echo '<pre>';
  echo "copy file from {$tmpfile} to {$uploadfile} .<br>\n";
  if (move_uploaded_file($tmpfile, $uploadfile)) {
      echo "File is valid, and was successfully uploaded.<br>\n";
  } else {
      echo "Possible file upload attack!<br>\n";
      echo 'Here is some more debugging info:';
      print_r($_FILES);
  }
  

  
  print "</pre>";
  
} else {
  echo("ERROR");
}
?>
