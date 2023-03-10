<?php
if(isset($_FILES['file']['name'])){
    // file name
    $filename = $_FILES['file']['name'];
    // Location
    $location = 'upload/' . $filename;
    $response = 0;
    // Upload file
    $res = move_uploaded_file($_FILES['file']['tmp_name'], $location);
    if($res) {
        $response = 1;
    } 
    echo $response;
    exit;
} else {
    echo "NOT POST";
}
