<?php
$target_dir = "uploads/";

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $student_id = $_POST['student_id'];
    $upload_path = $target_dir . $student_id . "/";

    if (!is_dir($upload_path)) {
        mkdir($upload_path, 0777, true);
    }

    foreach ($_FILES['images']['tmp_name'] as $key => $tmp_name) {
        $file_name = basename($_FILES['images']['name'][$key]);
        move_uploaded_file($tmp_name, $upload_path . $file_name);
    }
    echo "<p>Images uploaded for student $student_id!</p>";
}
?>

<!DOCTYPE html>
<html>
<head>
  <title>Upload Images</title>
</head>
<body>
  <h2>Upload Student Images</h2>
  <form method="POST" enctype="multipart/form-data">
    Student ID: <input type="text" name="student_id" required><br>
    Select Images: <input type="file" name="images[]" multiple required><br>
    <button type="submit">Upload</button>
  </form>
</body>
</html>