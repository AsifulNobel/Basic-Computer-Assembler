/**
 * Created by nobel on 3/29/16.
 */
var test1 = 'XwqloqwenkjaUas';
var test2 = 'oqweApasdkIKASD';
var test3 = 'LKSDKLJsaaklSDF';
var chosen_file = $('#id_uploaded_file').get(0).files.length;
var errorOccured = $('#error').length;

$(document).ready(function() {
    if (!chosen_file && errorOccured) {
        $('#error').css('display', 'none')
    }

    var options_uploaded = {
        target: ".output"
    };

    var options_local = {
        target: ".output",
        type: 'get'
    };

    $('#post-form').submit(function(event) {
        event.preventDefault();

        $(this).ajaxSubmit(options_uploaded);
    });

    $('#id_uploaded_file').change(function() {
        var path = $('#id_uploaded_file').val();

        if (path) {
            if ((path.indexOf('\\') !== -1 || path.indexOf('/') !== -1)) {
                path = path.split('\\');
                $("#fileChoose > span").html(path[2])
            } else if (path) {
                $('#fileChoose > span').html(path)
            }
            else {
                $('#fileChoose > span').html('Select a file...')
            }
        } else if (path) {
            $('#fileChoose > span').html(path)
        }
        else {
            $('#fileChoose > span').html('Select a file...')
        }
    });
    
    $('#test1').click(function () {
        $('#fileChoose > span').html('Sample Code 1')
        options_local['url'] = test1 + "/";

        $(this).ajaxSubmit(options_local);

    });

    $('#test2').click(function () {
        $('#fileChoose > span').html('Sample Code 2')
        options_local['url'] = test2 + "/"

        $(this).ajaxSubmit(options_local);

    });

    $('#test3').click(function () {
        $('#fileChoose > span').html('Sample Code 3');
        options_local['url'] = test3 + "/";

        $(this).ajaxSubmit(options_local);

    });
});