<?php
require_once __DIR__ . '/config.php';
// Accepts form-data or JSON: student_id, name
$input = $_POST;
if (empty($input['student_id']) || empty($input['name'])) {
    json_response(['error' => 'student_id and name required'], 400);
}

$student_id = $mysqli->real_escape_string($input['student_id']);
$name = $mysqli->real_escape_string($input['name']);
$mysqli = get_db();

$stmt = $mysqli->prepare("INSERT INTO students (student_id, name) VALUES (?, ?)");
$stmt->bind_param('ss', $input['student_id'], $input['name']);

if (!$stmt->execute()) {
    json_response(['success' => false, 'error' => $stmt->error], 500);
}

json_response(['success' => true, 'student_id' => $input['student_id']]);