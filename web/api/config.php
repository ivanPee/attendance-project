<?php
// config.php - put outside webroot in production
define('DB_HOST', 'localhost');
define('DB_USER', 'db_user');
define('DB_PASS', 'db_password');
define('DB_NAME', 'attendance_db');


// API token used by Raspberry Pi client
define('API_TOKEN', 'REPLACE_WITH_SECURE_TOKEN');


function json_response($data, $code = 200) {
    header('Content-Type: application/json');
    http_response_code($code);
    echo json_encode($data);
    exit;
}


function get_db() {
    $mysqli = new mysqli(DB_HOST, DB_USER, DB_PASS, DB_NAME);
    if ($mysqli->connect_errno) {
        json_response(['error' => 'DB connect error: ' . $mysqli->connect_error], 500);
    }
    $mysqli->set_charset('utf8mb4');
    return $mysqli;
}


function check_auth() {
    $headers = getallheaders();
    if (!isset($headers['Authorization']) && !isset($headers['authorization'])) {
        json_response(['error' => 'Missing Authorization header'], 401);
    }

    $auth = isset($headers['Authorization']) ? $headers['Authorization'] : $headers['authorization'];

    if (stripos($auth, 'Bearer ') === 0) {
        $token = trim(substr($auth, 7));
        if ($token !== API_TOKEN) {
            json_response(['error' => 'Invalid API token'], 403);
        }
        return true;
    }
    
    json_response(['error' => 'Invalid Authorization format'], 401);
}