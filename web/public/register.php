<?php include 'config.php'; ?>
<!DOCTYPE html>
<html>
<head>
  <title>Register Student</title>
</head>
<body>
  <h2>Register Student</h2>
  <form method="POST">
    Student ID: <input type="text" name="student_id" required><br>
    Name: <input type="text" name="name" required><br>
    <button type="submit">Register</button>
  </form>

<?php
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $student_id = $_POST['student_id'];
    $name = $_POST['name'];
    $stmt = $conn->prepare("INSERT INTO students (student_id, name) VALUES (?, ?)");
    $stmt->bind_param("ss", $student_id, $name);
    if ($stmt->execute()) {
        echo "<p>Student registered successfully!</p>";
    } else {
        echo "<p>Error: " . $stmt->error . "</p>";
    }
}
?>
</body>
</html>