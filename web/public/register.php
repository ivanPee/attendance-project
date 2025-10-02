<?php require_once __DIR__ . '/../api/config.php'; include 'inc/header.php'; ?>


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
    </div>
</div>


<?php include 'inc/footer.php'; ?>