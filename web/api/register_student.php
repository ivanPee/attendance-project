<?php
require_once __DIR__ . '/config.php';

// Initialize the database connection
$mysqli = get_db();

// Accepts form-data or JSON: student_id, name
$input = $_POST;
if (empty($input['student_id']) || empty($input['name'])) {
    json_response(['error' => 'student_id and name required'], 400);
}

// Escape input values after database connection is initialized
$student_id = $mysqli->real_escape_string($input['student_id']);
$name = $mysqli->real_escape_string($input['name']);

$stmt = $mysqli->prepare("INSERT INTO students (student_id, name) VALUES (?, ?)");
$stmt->bind_param('ss', $student_id, $name);

if (!$stmt->execute()) {
    json_response(['success' => false, 'error' => $stmt->error], 500);
}

json_response(['success' => true, 'student_id' => $student_id]);
