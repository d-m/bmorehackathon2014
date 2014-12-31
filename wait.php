<!doctype html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Tweetku</title>
        <link rel="stylesheet" href="css/app.css">
<?php
$haikuFile = "haikuStore.txt";
$prevErr = (file_exists('err.log') && filesize('err.log') > 0);
if (empty($_GET) || $prevErr){
    $timeNow = time();
    if (!empty($_POST) || $prevErr){
        if ($prevErr){
            unlink('err.log');
            $term = 'error';
        }else{
            $term = $_POST["name"];
        }
        exec('/usr/local/bin/python streamTester_PRIVATE.py '.$term.' > output.log 2>err.log &');
        print '        <meta http-equiv="refresh" content="3; url=wait.php?time='.$timeNow.'" />';
    } else{
        print '        <meta http-equiv="refresh" content="0; url=index.php" />'; 
    }
} else{
    $timeStart = $_GET["time"];
    date_default_timezone_set('America/New_York');
    $modTime = date("U",filemtime($haikuFile)); 
    if ($modTime > $timeStart) {
        print '        <meta http-equiv="refresh" content="0; url=index.php" />';    
    } else {
        print '        <meta http-equiv="refresh" content="3; url=wait.php?time='.$timeStart.'" />';    
    }
}

?>

    </head>
    <body>
        <div id="haiku">
            <div id="finalText">
                <br>Listening for tweetkus...                
            </div>            
        </div>
    </body>
</html>