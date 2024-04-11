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

    // Adjusted SQL to fetch last measure date and last three measurements
    $sql = "
        WITH ranked_measures AS (
            SELECT
                id_flower,
                temperature,
                humidity,
                measure_date,
                ROW_NUMBER() OVER (PARTITION BY id_flower ORDER BY measure_date DESC) AS rn
            FROM measures
        )
        SELECT
            f.common_name,
            rm1.temperature AS last_temperature,
            rm1.humidity AS last_humidity,
            rm1.measure_date AS last_measure_date,
            ARRAY_AGG(rm2.temperature ORDER BY rm2.rn) AS temperatures,
            ARRAY_AGG(rm2.humidity ORDER BY rm2.rn) AS humidities,
            ARRAY_AGG(rm2.measure_date ORDER BY rm2.rn) AS measure_dates
        FROM flowers f
        LEFT JOIN ranked_measures rm1 ON f.id_flower = rm1.id_flower AND rm1.rn = 1
        LEFT JOIN ranked_measures rm2 ON f.id_flower = rm2.id_flower AND rm2.rn <= 3
        WHERE f.possessed = TRUE
        GROUP BY f.common_name, rm1.temperature, rm1.humidity, rm1.measure_date
        ORDER BY f.common_name;
    ";

    $sth = $dbh->prepare($sql);
    $sth->execute();
    $flowers = $sth->fetchAll(PDO::FETCH_ASSOC);

    // Preprocess flowers data for Twig
    foreach ($flowers as $key => $flower) {
        $flowers[$key]['measure_dates'] = array_reverse(array_filter(explode(',', trim($flower['measure_dates'], '{}'))));
        $flowers[$key]['temperatures'] = array_reverse(array_filter(explode(',', trim($flower['temperatures'], '{}'))));
        $flowers[$key]['humidities'] = array_reverse(array_filter(explode(',', trim($flower['humidities'], '{}'))));
    }

    echo $twig->render('index.twig', [
        'flowers' => $flowers,
    ]);

} catch (PDOException $e) {
    echo "Error connecting to the database: " . $e->getMessage();
}
?>
