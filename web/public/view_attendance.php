<?php include 'config.php'; ?>
<!DOCTYPE html>
<html>
<head>
  <title>View Attendance</title>
</head>
<body>
  <h2>Attendance Records</h2>
  <table border="1">
    <tr><th>Student ID</th><th>Name</th><th>Timestamp</th></tr>
<?php
$result = $conn->query("SELECT a.student_id, s.name, a.timestamp 
                        FROM attendance a 
                        LEFT JOIN students s ON a.student_id = s.student_id 
                        ORDER BY a.timestamp DESC");
while ($row = $result->fetch_assoc()) {
    echo "<tr><td>{$row['student_id']}</td><td>{$row['name']}</td><td>{$row['timestamp']}</td></tr>";
}
?>
  </table>
</body>
</html>