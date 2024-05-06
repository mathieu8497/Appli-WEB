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
        to_char(rm1.measure_date, 'YYYY-MM-DD HH24:MI') AS last_measure_date,
        ARRAY_AGG(rm2.temperature ORDER BY rm2.measure_date DESC) AS temperatures,
        ARRAY_AGG(rm2.humidity ORDER BY rm2.measure_date DESC) AS humidities,
        ARRAY_AGG(to_char(rm2.measure_date, 'YYYY-MM-DD HH24:MI') ORDER BY rm2.measure_date DESC) AS measure_dates
    FROM flowers f
    LEFT JOIN ranked_measures rm1 ON f.id_flower = rm1.id_flower AND rm1.rn = 1
    LEFT JOIN ranked_measures rm2 ON f.id_flower = rm2.id_flower
    WHERE f.possessed = TRUE
    GROUP BY f.common_name, rm1.temperature, rm1.humidity, rm1.measure_date
    ORDER BY f.common_name;
    ";

    $sth = $dbh->prepare($sql);
    $sth->execute();
    $flowers = $sth->fetchAll(PDO::FETCH_ASSOC);

    // Preprocess flowers data for Twig
    foreach ($flowers as $key => $flower) {
        // Parse all measurements for charts
        $measureDates = trim($flower['measure_dates'], "{}");
        $temperatures = trim($flower['temperatures'], "{}");
        $humidities = trim($flower['humidities'], "{}");
    
        // Convert string to array
        $dateArray = explode(',', $measureDates);
        $temperatureArray = explode(',', $temperatures);
        $humidityArray = explode(',', $humidities);
    
        // Since data is fetched in reverse chronological order, reverse them for the chart
        $flowers[$key]['all_measure_dates'] = array_reverse($dateArray);
        $flowers[$key]['all_temperatures'] = array_reverse($temperatureArray);
        $flowers[$key]['all_humidities'] = array_reverse($humidityArray);
    
        // Last three measurements for the table, already handled correctly
        $flowers[$key]['measure_dates'] = array_slice($dateArray, 0, 3);
        $flowers[$key]['temperatures'] = array_slice($temperatureArray, 0, 3);
        $flowers[$key]['humidities'] = array_slice($humidityArray, 0, 3);
    }
                        
        
    echo $twig->render('index.twig', [
        'flowers' => $flowers,
    ]);

} catch (PDOException $e) {
    echo "Error connecting to the database: " . $e->getMessage();
}
?>
