<?php 

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (isset($_FILES['file'])) {
        $errors = [];
        $path = 'upload/';
        $extensions = ['xml', 'jpg', 'jpeg', 'png', 'gif'];
        $file = count($_FILES['file']['tmp_name']);
        $file_name = $_FILES['file']['name'];
        $file_tmp = $_FILES['file']['tmp_name'];
        $file_type = $_FILES['file']['type'];
        $file_size = $_FILES['file']['size'];
        $tmp = explode('.', $_FILES['file']['name']);
        $file_ext = strtolower(end($tmp));

        $file = $path . $file_name;

        if (!in_array($file_ext, $extensions)) {
            $errors[] = 'Extension not allowed: ' . $file_name . ' ' . $file_type;
        }

        if ($file_size > 2097152) {
            $errors[] = 'File size exceeds limit: ' . $file_name . ' ' . $file_type;
        }

        if (empty($errors)) {
            // move_uploaded_file($file_tmp, $file);
            echo "copy file from {$file_tmp} to {$file} .<br>\n";
            if (move_uploaded_file($file_tmp, $file)) {
                echo "File is valid, and was successfully uploaded.<br>\n";
            } else {
                echo "Possible file upload attack!<br>\n";
                echo 'Here is some more debugging info:';
                print_r($_FILES);                
            }
        }
    }
    if ($errors) print_r($errors);
    
}
