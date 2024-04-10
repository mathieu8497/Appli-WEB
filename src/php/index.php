<?php

spl_autoload_register(function ($classname) {
    $filename = '../' . ltrim(str_replace('\\', '/', $classname)) . '.php';
    if (file_exists($filename))
        require_once $filename;
});
$loader = new \Twig\Loader\FilesystemLoader('../html');
$twig = new \Twig\Environment($loader);

echo $twig->render('index.twig', [
    // Pass any dynamic content to your template here.
    // For now, it appears there's no dynamic content to pass.
]);
