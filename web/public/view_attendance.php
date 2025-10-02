<?php 
require_once __DIR__ . '/../api/config.php'; // make sure config.php is included

$db = get_db(); // get a mysqli connection
?>
<?php include 'inc/header.php'; ?>
<div class="content">
    <h2>Attendance Records</h2>
    <table id="attendanceTable" class="table table-striped table-bordered mt-3">
        <thead>
            <tr>
                <th>Student ID</th>
                <th>Name</th>
                <th>Timestamp</th>
            </tr>
        </thead>
        <tbody>
            <?php
                $result = $db->query("SELECT a.student_id, s.name, a.timestamp
                    FROM attendance a
                    LEFT JOIN students s ON a.student_id = s.student_id
                    ORDER BY a.timestamp DESC");
                while ($row = $result->fetch_assoc()) {
                    echo "<tr><td>{$row['student_id']}</td><td>{$row['name']}</td><td>{$row['timestamp']}</td></tr>";
                }
            ?>
        </tbody>
    </table>
</div>
<?php include 'inc/footer.php'; ?>
<script>
    $(document).ready(function(){
        $('#attendanceTable').DataTable();
    });
</script>
