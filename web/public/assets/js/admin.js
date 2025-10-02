// admin.js - sidebar toggle, ajax helpers, datatable init
$(document).on('submit', '#formRegister', function(e){

    e.preventDefault();
    var $btn = $(this).find('button[type=submit]').prop('disabled', true);
    $.post('../api/register_student.php', $(this).serialize(), function(res){
        if (res.success) {
            alert('Registered: ' + res.student_id);
            $('#formRegister')[0].reset();
        } else {
            alert('Error: ' + (res.error || 'unknown'));
        }
    }, 'json').always(function(){ $btn.prop('disabled', false); });
});


// Upload images handler
$(document).on('submit', '#formUploadImages', function(e){
    e.preventDefault();
    var formData = new FormData(this);
    var $btn = $(this).find('button[type=submit]').prop('disabled', true);


    $.ajax({
        url: '../api/upload_images.php',
        method: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function(res){
            if (res.saved !== undefined) {
                alert('Saved ' + res.saved + ' files');
                $('#formUploadImages')[0].reset();
            } else if (res.error) {
                alert('Error: ' + res.error);
            }
        },
            error: function(xhr){ alert('Upload failed: ' + xhr.responseText); },
            complete: function(){ $btn.prop('disabled', false); }
        });
});


// Train model button
$(document).on('submit', '#formTrain', function(e){
    e.preventDefault();
    var $btn = $(this).find('button[type=submit]').prop('disabled', true).text('Training...');

    $.post('../api/train.php', {}, function(res){
        if (res.success) {
            $('#trainOutput').text(res.output);
            alert('Training complete');
        } else {
            $('#trainOutput').text(res.output || res.error || 'Unknown error');
            alert('Training failed: ' + (res.error || 'see output'));
        }
    }, 'json').always(function(){ $btn.prop('disabled', false).text('Start Training'); });
});


// Attendance datatable (page view_attendance.php)
$(document).ready(function() {
    if ($('#tableAttendance').length) {
        $('#tableAttendance').DataTable({
            ajax: {
                url: '../api/get_students.php',
                dataSrc: 'data'
            },
            columns: [
                { data: 'student_id' },
                { data: 'name' },
                { data: 'subject' },
                { data: 'timestamp' }
            ],
            order: [[3, 'desc']],
            pageLength: 25
        });
    }
});

