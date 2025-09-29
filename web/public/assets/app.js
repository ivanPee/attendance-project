$(function(){
    $('#registerForm').on('submit', function(e){
        e.preventDefault();
        var data = $(this).serialize();
        $.post('/api/register_student.php', data, function(res){
            if (res.success) {
                $('#msg').text('Registered: ' + res.student_id);
            } else {
                $('#msg').text('Error: ' + (res.error || 'unknown'));
            }
            }, 'json').fail(function(xhr){
                
            $('#msg').text('Failed: ' + xhr.responseText);
        });
    });
});