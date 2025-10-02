<?php include 'inc/header.php'; ?>
    <div class="content">
        <h2>Upload Student Images</h2>
        <form method="POST" enctype="multipart/form-data" class="mt-3">
            <div class="mb-3">
                <label for="student_id" class="form-label">Student ID</label>
                <input type="text" class="form-control" id="student_id" name="student_id" required>
            </div>
            <div class="mb-3">
                <label for="images" class="form-label">Select Images</label>
                <input class="form-control" type="file" id="images" name="images[]" multiple required>
            </div>
            <button type="submit" class="btn btn-success">Upload</button>
        </form>


        <?php
            if ($_SERVER['REQUEST_METHOD'] == 'POST') {
                $student_id = $_POST['student_id'];
                $target_dir = "uploads/" . $student_id . "/";


                if (!is_dir($target_dir)) {
                    mkdir($target_dir, 0777, true);
                }


                foreach ($_FILES['images']['tmp_name'] as $key => $tmp_name) {
                    $file_name = basename($_FILES['images']['name'][$key]);
                    move_uploaded_file($tmp_name, $target_dir . $file_name);
                }
                echo "<div class='alert alert-success mt-3'>Images uploaded successfully for student $student_id!</div>";
            }
        ?>
    </div>
<?php include 'inc/footer.php'; ?>