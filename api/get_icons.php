<?php
header('Content-Type: application/json');

$icons_file = __DIR__ . '/icons.json';

if (!file_exists($icons_file)) {
    http_response_code(404);
    echo json_encode([]); // Return empty array on error
    exit;
}

$all_icons_json = file_get_contents($icons_file);
$all_icons = json_decode($all_icons_json, true);

if (json_last_error() !== JSON_ERROR_NONE) {
    http_response_code(500);
    echo json_encode([]); // Return empty array on error
    exit;
}

// If no category name is provided, return all icons.
// This is used as a fallback by the frontend.
if (!isset($_GET['category_name']) || empty(trim($_GET['category_name']))) {
    echo $all_icons_json;
    exit;
}

$category_name = strtolower(trim($_GET['category_name']));
// Extract keywords from the category name.
$keywords = preg_split('/[\s,\-]+/', $category_name);
$keywords = array_filter($keywords); // Remove any empty values

$filtered_icons = [];
if (!empty($keywords)) {
    $found_icons = [];
    foreach ($keywords as $keyword) {
        // Skip very short keywords to avoid overly broad matches.
        if (strlen($keyword) < 3) continue;
        foreach ($all_icons as $icon) {
            if (strpos($icon, $keyword) !== false) {
                // Use the icon class as a key to prevent duplicates
                $found_icons[$icon] = true;
            }
        }
    }
    $filtered_icons = array_keys($found_icons);
}

// Return the list of unique, filtered icons.
// If the list is empty, the frontend will make another request for all icons.
echo json_encode(array_values($filtered_icons));

?>
