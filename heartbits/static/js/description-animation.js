$(document).ready(function () {
    $(document).on('click', '.flipcard', function () {
        if ($(this).hasClass('flag')) {
            $(this).removeClass('is-flipped');
            $(this).removeClass('flag');
        } else {
            $(this).addClass('is-flipped');
            $(this).addClass('flag');
        }
    });
});
