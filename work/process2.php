<?php 
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['file'])) {
    chdir(__DIR__);
    $file_tmp = $_FILES['file']['tmp_name'];
    $path = 'server/data/xml/';
    $file_name = basename($_FILES['file']['name']);
    $file = $path . $file_name;
    if (move_uploaded_file($file_tmp, $file)) {
        echo "File is valid, and was successfully uploaded.<br>\n";
    } else {
        echo "Possible file upload attack!<br>\n";
        echo 'Here is some more debugging info:';
        print_r($_FILES);                
    }      
}
else {
    echo "NOT POST";
}
