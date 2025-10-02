<?php include 'inc/header.php'; ?>
    <div class="content">
        <h2>Train Face Recognition Model</h2>
        <form method="POST">
            <button type="submit" name="train" class="btn btn-primary">Start Training</button>
        </form>


        <?php
            if (isset($_POST['train'])) {
                // call python training script
                $output = shell_exec("py train_model.py 2>&1");
                echo "<div class='mt-3'><h5>Training Output:</h5><pre>$output</pre></div>";
            }
        ?>
    </div>
<?php include 'inc/footer.php'; ?>