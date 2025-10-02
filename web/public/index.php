<?php require_once __DIR__ . '/../api/config.php'; include 'inc/header.php'; ?>


<div class="row">
    <div class="col-12">
        <h1 class="mt-3">Dashboard</h1>
        <p class="text-muted">Overview of system</p>
    </div>
</div>


<div class="row mt-4">
    <div class="col-md-4">
        <div class="card shadow-sm">
            <div class="card-body">
                <h5 class="card-title">Students</h5>
                <?php
                    $db = get_db();
                    $c = $db->query('SELECT COUNT(*) AS c FROM students')->fetch_assoc();
                    echo '<h2>' . intval($c['c']) . '</h2>';
                ?>
            </div>
        </div>
    </div>
    <div class="col-md-4">
        <div class="card shadow-sm">
            <div class="card-body">
                <h5 class="card-title">Attendance Records</h5>
                <?php
                    $c = $db->query('SELECT COUNT(*) AS c FROM attendance')->fetch_assoc();
                    echo '<h2>' . intval($c['c']) . '</h2>';
                ?>
            </div>
        </div>
    </div>
    <div class="col-md-4">
        <div class="card shadow-sm">
            <div class="card-body">
                <h5 class="card-title">Last Trained</h5>
                <?php
                    $ts = file_exists(__DIR__ . '/../../pi/trained_model.yml') ? date('Y-m-d H:i:s', filemtime(__DIR__ . '/../../pi/trained_model.yml')) : 'Never';
                    echo '<h6>' . htmlspecialchars($ts) . '</h6>';
                ?>
            </div>
        </div>
    </div>
</div>


<?php include 'inc/footer.php'; ?>