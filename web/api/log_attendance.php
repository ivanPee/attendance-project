<?php
require_once __DIR__ . '/config.php';
// This endpoint requires Bearer token (Authorization: Bearer <API_TOKEN>)
check_auth();
$input = json_decode(file_get_contents('php://input'), true);
if (!$input || empty($input['student_id'])) json_response(['error' => 'student_id required'], 400);

$student_id = $input['student_id'];
$subject = isset($input['subject']) ? $input['subject'] : 'General';
$mysqli = get_db();

$stmt = $mysqli->prepare("INSERT INTO attendance (student_id, subject) VALUES (?, ?)");
$stmt->bind_param('ss', $student_id, $subject);

if (!$stmt->execute()) {
    json_response(['success' => false, 'error' => $stmt->error], 500);
}

json_response(['success' => true, 'student_id' => $student_id]);