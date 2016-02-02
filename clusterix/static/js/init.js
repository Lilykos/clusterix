$(function() {
    // JQuery slider init (fade in/out)
    $.fn.fadeThenSlideToggle = function(buttonID, speed, easing, callback) {
        var fadeOutButton = '<span class="glyphicon glyphicon-chevron-down col-lg-1">';
        var fadeInButton = '<span class="glyphicon glyphicon-chevron-up col-lg-1">';

        if (this.is(":hidden")) {
            $(buttonID).html(fadeInButton);
            return this.slideDown(speed, easing).fadeTo(speed, 1, easing, callback);
        } else {
            $(buttonID).html(fadeOutButton);
            return this.fadeTo(speed, 0, easing).slideUp(speed, easing, callback);
        }
    };

    // Inputs
    DataInput.init();

    // Router & Validation
    Router.init();

    // Search
    Search.init();
});