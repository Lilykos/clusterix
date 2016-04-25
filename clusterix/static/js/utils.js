var Utils = (function() {

    return {

        /**
         * Compile and render a template using Handlebars.
         */
        compileTemplate: function(template, target, data, emptyElement) {
            var rendered = Handlebars.compile($(template).html())(data);

            if (emptyElement)
                $(target).empty().append(rendered);
            else
                $(target).append(rendered);
        },

        /**
         * Returns true/ false depending on whether an element is found in an array or not.
         */
        inArray: function(value, array) {
            return array.indexOf(value) > -1;
        },

        /**
         * Accepts two arrays, and returns an array containing all the elements that
         * exist on the first array but not the second.
         */
        arrayDifference: function(first, second) {
            return $(first).not(second).get();
        },

        /**
         * Delays the trigger of a function by the provided time.
         */
        debounce: function(fn, delay) {
            var timer = null;
            return function() {
                var context = this;
                var args = arguments;

                clearTimeout(timer);
                timer = setTimeout(function () {
                    fn.apply(context, args);
                }, delay);
            };
        },

        /**
         * Attach panel to custom slider.
         */
        attachSliderToPanel: function(buttonID, contentID, speed/*, easing, callback*/) {
            $(buttonID).click(function() {
                $(contentID).fadeThenSlideToggle(buttonID, speed);
            });
        }
    }
})();