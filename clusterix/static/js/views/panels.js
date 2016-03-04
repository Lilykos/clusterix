var Panels = (function() {
    var fadeOutButton = '<span class="glyphicon glyphicon-chevron-down col-lg-1">';
    var fadeInButton = '<span class="glyphicon glyphicon-chevron-up col-lg-1">';

    var panelSelectors = [
        ['#data-input-hide', '#data-input-body'],
        ['#algorithms-hide', '#algorithms-body'],
        ['#csv-fields-hide', '#csv-fields-body']
    ];

    /**
     * Attach the JQuery function.
     */
    function registerJQuerySlide() {
        // Init jQuery animations (fade in/out).
        $.fn.fadeThenSlideToggle = function(buttonID, speed, easing, callback) {
            if (this.is(":hidden")) {
                $(buttonID).html(fadeInButton);
                return this.slideDown(speed, easing).fadeTo(speed, 1, easing, callback);
            } else {
                $(buttonID).html(fadeOutButton);
                return this.fadeTo(speed, 0, easing).slideUp(speed, easing, callback);
            }
        };
    }


    return {

        /**
         * Initialize JQuery function that allows panel fade in/out.
         * @constructor
         */
        init: function() {
            registerJQuerySlide();

            // For each of the panels create the animation,
            // by passing the panel id and button id.
            panelSelectors.forEach(function(item) {
                $(item[0]).click(function() {
                    $(item[1]).fadeThenSlideToggle(item[0], 150);
                });
            });

            console.log('Panels init');
        }
    }

})();