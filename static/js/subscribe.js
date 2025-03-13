/**
 * Subscribe
 */
$(document).ready(function ($) {

    $('#formSubscribe').submit(function(e){
        $.ajax({
            type: "POST",
            url: $(this).attr("action"),
            data: $(this).serialize(),
            success: function (data) {
                var okMessage = $('#divSubscribeOk');
                var errorMessage = $('#divSubscribeError');
                if (data.result === "ok") {
                    okMessage.show();
                    errorMessage.hide();
                } else {
                    okMessage.hide();
                    errorMessage.show();
                }

            },
            error: function (xhr, textStatus, errorThrown) {
                console.log("Error: " + errorThrown + xhr.status + xhr.responseText);
            }
        });

        e.preventDefault();
    });

    $('#form-subscribe-on-course').submit(function(e){
        $.ajax({
            type: "POST",
            url: $(this).attr("action"),
            data: $(this).serialize(),
            success: function (data) {
                var okMessage = $('#div-subscribe-on-course-ok');
                var errorMessage = $('#div-subscribe-on-course-error');
                if (data.result === "ok") {
                    okMessage.show();
                    errorMessage.hide();
                } else {
                    okMessage.hide();
                    errorMessage.show();
                }

            },
            error: function (xhr, textStatus, errorThrown) {
                console.log("Error: " + errorThrown + xhr.status + xhr.responseText);
            }
        });

        e.preventDefault();
    });

});