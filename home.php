<?php
$conn = new mysqli('localhost','root','','count');
header("Refresh: 60");
$file = fopen("test.txt","r");

while (!feof($file)) {
    $content = fgets($file);
    $sql = "INSERT INTO `test` (`number_of_cars`) VALUES ('$content')";
    $conn->query($sql);
}
fclose($file);
?>

<!DOCTYPE html>
<html>
<head>
	<title>HOME</title>
    <link href='https://fonts.googleapis.com/css?family=Orbitron' rel='stylesheet' type='text/css'>

</head>
<body>
    <img src="parking.jpg" width="1600" height="950">
    <div style="font-family: 'Orbitron', sans-serif; position:absolute; bottom:350px; right:220px; font-size:90px; color:RED"><p><?php echo "<p>{$content}</p>"; ?></p></div>


</body>
</html>