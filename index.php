<!doctype html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Tweetku</title>
        <link rel="stylesheet" href="css/app.css">
    </head>
    <body>
        <form action="wait.php" method="post">
            Tweetku Topic: <input type="text" name="name"><br>
            <input type="submit">
        </form>
        <div id="haiku">
            <div id="finalText">
                <i><?php echo file_get_contents('haikuStore.txt') ?></i>
            </div>                      
        </div>
    </body>
</html>