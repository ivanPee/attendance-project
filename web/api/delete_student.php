<?php
require_once __DIR__ . '/config.php';

$db = get_db();

if(isset($_POST['student_id'])){
    $student_id = $_POST['student_id'];
    $db->query("DELETE FROM students WHERE student_id='$student_id'");
    echo "Student deleted successfully!";
}
?>
