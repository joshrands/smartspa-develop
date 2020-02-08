<?php

echo "Thank you! Connecting to the Internet now...<br>";

$wifi_network = $_POST['wifiNetwork'];
$wifi_password = $_POST['wifiPassword'];

/* Run python script to setup network... */ 
//$command = escapeshellcmd('./setup_network.py ' . $wifi_network . ' ' . $wifi_password);
$output = shell_exec('python3 setup_network.py ' . $wifi_network . ' ' . $wifi_password);
echo $output;

echo "<br>";
echo "Network connection complete.";

?>
