<?php
require_once __DIR__ . '/config.php';
// POST: student_id, files[]
if (empty($_POST['student_id'])) json_response(['error' => 'student_id required'], 400);

$student_id = preg_replace('/[^a-zA-Z0-9_\-]/', '_', $_POST['student_id']);
$target_dir = __DIR__ . '/../public/uploads/' . $student_id;

if (!is_dir($target_dir)) mkdir($target_dir, 0755, true);
$saved = 0;

foreach ($_FILES as $file) {
    if ($file['error'] === UPLOAD_ERR_OK) {
        $ext = pathinfo($file['name'], PATHINFO_EXTENSION);
        $fn = uniqid() . '.' . $ext;
        move_uploaded_file($file['tmp_name'], $target_dir . '/' . $fn);
        $saved++;
    }
}

json_response(['saved' => $saved]);