<?php
require_once __DIR__ . '/config.php';
$mysqli = get_db();

$res = $mysqli->query("SELECT student_id, name, photo_dir FROM students ORDER BY name");
$rows = [];

while ($r = $res->fetch_assoc()) $rows[] = $r;
json_response(['students' => $rows]);