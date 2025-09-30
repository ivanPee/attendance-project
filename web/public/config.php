<?php
$host = "localhost";
$user = "root";   // adjust
$pass = "";       // adjust
$db   = "attendance_db";

$conn = new mysqli($host, $user, $pass, $db);
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
?>