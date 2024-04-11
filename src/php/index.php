<?php

spl_autoload_register(function ($classname) {
    $filename = '../' . ltrim(str_replace('\\', '/', $classname)) . '.php';
    if (file_exists($filename)) require_once $filename;
});

$loader = new \Twig\Loader\FilesystemLoader('../html');
$twig = new \Twig\Environment($loader);

$host = $_ENV['DB_HOST'];
$user = $_ENV['DB_USER'];
$password = $_ENV['DB_PASSWORD'];
$database = $_ENV['DB_DB'];
$port = 5432;

try {
    $dsn = "pgsql:host=$host;port=$port;dbname=$database;user=$user;password=$password";
    $dbh = new PDO($dsn);
    $dbh->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    $sql = "
        SELECT f.common_name, m.temperature, m.humidity
        FROM flowers f
        LEFT JOIN (
            SELECT id_flower, temperature, humidity, MAX(measure_date) as latest_date
            FROM measures
            GROUP BY id_flower, temperature, humidity
        ) m ON f.id_flower = m.id_flower
        WHERE f.possessed = TRUE
        ORDER BY f.common_name;
    ";

    $sth = $dbh->prepare($sql);
    $sth->execute();
    $flowers = $sth->fetchAll(PDO::FETCH_ASSOC);

    echo $twig->render('index.twig', [
        'flowers' => $flowers,
    ]);

} catch (PDOException $e) {
    echo "Error connecting to the database: " . $e->getMessage();
}
?>
