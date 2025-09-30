<!DOCTYPE html>
<html>
<head>
  <title>Train Model</title>
</head>
<body>
  <h2>Train Face Recognition Model</h2>
  <form method="POST">
    <button type="submit" name="train">Start Training</button>
  </form>

<?php
if (isset($_POST['train'])) {
    // adjust path to Python on your server
    $output = shell_exec("python3 train_model.py 2>&1");
    echo "<pre>$output</pre>";
}
?>
</body>
</html>