<?php 
require_once __DIR__ . '/../api/config.php'; 
include 'inc/header.php'; 

$db = get_db();
?>

<div class="row">
    <div class="col-12">
        <h2 class="mt-3">Register Student</h2>
        <div class="card mt-3">
            <div class="card-body">
                <form id="formRegister">
                    <div class="mb-3">
                        <label class="form-label">Student ID</label>
                        <input class="form-control" name="student_id" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Full Name</label>
                        <input class="form-control" name="name" required>
                    </div>
                    <button class="btn btn-primary" type="submit">Register</button>
                </form>
            </div>
        </div>

        <!-- Students Table -->
        <div class="card mt-4">
            <div class="card-body">
                <h4>Registered Students</h4>
                <table id="studentsTable" class="table table-striped table-bordered mt-3">
                    <thead>
                        <tr>
                            <th>Student ID</th>
                            <th>Name</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php
                        $result = $db->query("SELECT * FROM students ORDER BY name ASC");
                        while ($row = $result->fetch_assoc()) {
                            echo "<tr>
                                    <td>{$row['student_id']}</td>
                                    <td>{$row['name']}</td>
                                    <td><button class='btn btn-danger btn-sm deleteStudent' data-id='{$row['student_id']}'>Delete</button></td>
                                  </tr>";
                        }
                        ?>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>

<?php include 'inc/footer.php'; ?>

<!-- DataTables & JS -->
<link rel="stylesheet" href="https://cdn.datatables.net/1.13.5/css/jquery.dataTables.min.css">
<script src="https://code.jquery.com/jquery-3.7.0.min.js"></script>
<script src="https://cdn.datatables.net/1.13.5/js/jquery.dataTables.min.js"></script>

<script>
$(document).ready(function() {
    $('#studentsTable').DataTable();

    // Handle form submission
    $('#formRegister').on('submit', function(e){
        e.preventDefault();
        $.ajax({
            url: '../api/register_student.php',
            type: 'POST',
            data: $(this).serialize(),
            success: function(res) {
                alert(res);
                location.reload(); // Reload to update table
            }
        });
    });

    // Delete student
    $('.deleteStudent').on('click', function() {
        if(confirm('Are you sure you want to delete this student?')) {
            let student_id = $(this).data('id');
            $.ajax({
                url: '../api/delete_student.php',
                type: 'POST',
                data: { student_id: student_id },
                success: function(res) {
                    alert(res);
                    location.reload(); // Reload to update table
                }
            });
        }
    });
});
</script>
