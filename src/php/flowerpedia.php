<?php

spl_autoload_register(function ($classname) {
    $filename = '../' . ltrim(str_replace('\\', '/', $classname)) . '.php';
    if (file_exists($filename))
        require_once $filename;
});

$loader = new \Twig\Loader\FilesystemLoader('../html');
$twig = new \Twig\Environment($loader);

$host = $_ENV['DB_HOST']; // Host address
$user = $_ENV['DB_USER']; // Database user
$password = $_ENV['DB_PASSWORD']; // Database password
$database = $_ENV['DB_DB']; // Database name
$port = 5432; // Port, PostgreSQL default is 5432

$search = isset($_GET['search']) ? '%' . $_GET['search'] . '%' : '%';

try {
    $dsn = "pgsql:host=$host;port=$port;dbname=$database;user=$user;password=$password";
    $dbh = new PDO($dsn);
    $dbh->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    $sql = "SELECT common_name, scientific_name, family, plant_type, blooming_period, colors, pollinators FROM flowers WHERE (common_name ILIKE :search OR family ILIKE :search)";

    // Add conditions for each filter
    if (!empty($_GET['plant_type'])) {
        $sql .= " AND plant_type = :plant_type";
    }
    if (!empty($_GET['blooming_period'])) {
        $sql .= " AND blooming_period = :blooming_period";
    }
    if (isset($_GET['possessed'])) {
        $sql .= " AND possessed = TRUE";
    }

    $sql .= " ORDER BY common_name;";

    $sth = $dbh->prepare($sql);
    $sth->bindParam(':search', $search, PDO::PARAM_STR);

    // Bind filter parameters if they exist
    if (!empty($_GET['plant_type'])) {
        $sth->bindParam(':plant_type', $_GET['plant_type'], PDO::PARAM_STR);
    }
    if (!empty($_GET['blooming_period'])) {
        $sth->bindParam(':blooming_period', $_GET['blooming_period'], PDO::PARAM_STR);
    }

    $sth->execute();
    $flowers = $sth->fetchAll(PDO::FETCH_ASSOC);

    // Check if the request is an AJAX request
    if (!empty($_SERVER['HTTP_X_REQUESTED_WITH']) && strtolower($_SERVER['HTTP_X_REQUESTED_WITH']) == 'xmlhttprequest') {
        header('Content-Type: application/json'); // Set correct content type for JSON
        echo json_encode($flowers); // Echo the flowers as JSON
        exit; // Prevent further execution, important to avoid sending additional data after the JSON response
    }

    // Fetch distinct values for filters
    $plantTypesSql = "SELECT DISTINCT plant_type FROM flowers ORDER BY plant_type;";
    $plantTypesResult = $dbh->query($plantTypesSql);
    $plantTypes = $plantTypesResult->fetchAll(PDO::FETCH_COLUMN);

    $sqlBloomingPeriods = "SELECT DISTINCT blooming_period FROM flowers ORDER BY blooming_period;";
    $stmtBloomingPeriods = $dbh->query($sqlBloomingPeriods);
    $bloomingPeriods = $stmtBloomingPeriods->fetchAll(PDO::FETCH_COLUMN);

    $sqlColors = "SELECT DISTINCT UNNEST(STRING_TO_ARRAY(colors, ', ')) AS color FROM flowers ORDER BY color;";
    $stmtColors = $dbh->query($sqlColors);
    $colors = $stmtColors->fetchAll(PDO::FETCH_COLUMN);

    $sqlPollinators = "SELECT DISTINCT UNNEST(STRING_TO_ARRAY(pollinators, ', ')) AS pollinator FROM flowers ORDER BY pollinator;";
    $stmtPollinators = $dbh->query($sqlPollinators);
    $pollinators = $stmtPollinators->fetchAll(PDO::FETCH_COLUMN);

    echo $twig->render('flowerpedia.twig', [
        'data' => $flowers,
        'plant_types' => $plantTypes,
        'blooming_periods' => $bloomingPeriods,
        'colors' => $colors,
        'pollinators' => $pollinators
    ]);

} catch (PDOException $e) {
    echo "Erreur lors de la connexion à la base de données : " . $e->getMessage();
}
?>