<?php
header('Content-Type: application/json');

$icons_file = __DIR__ . '/icons.json';

if (file_exists($icons_file)) {
    $file_content = file_get_contents($icons_file);
    echo $file_content;
} else {
    http_response_code(404);
    echo json_encode(['success' => false, 'message' => 'Icons file not found.']);
}
?>
