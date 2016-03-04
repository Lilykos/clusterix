var Utils = (function() {

    return {

        /**
         * Compile and render a template using Handlebars.
         * @param {string} template
         * @param {string} target
         * @param {Object} data
         */
        compileTemplate: function(template, target, data) {
            var rendered = Handlebars.compile($(template).html())(data);
            $(target).empty().append(rendered);
        },

        /**
         * Returns true/ false depending on whether an element is found in an array or not.
         * @param value
         * @param {Array} array
         * @returns {boolean}
         */
        inArray: function(value, array) {
            return array.indexOf(value) > -1;
        },

        /**
         * Accepts two arrays, and returns an array containing all the elements that
         * exist on the first array but not the second.
         * @param {Array} first
         * @param {Array} second
         * @return {Array}
         */
        arrayDifference: function(first, second) {
            return $(first).not(second).get();
        },

        /**
         * Delays the trigger of a function by the provided time.
         * @param {function} fn
         * @param {int} delay
         * @return {function}
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
         * Renders the content of the node (used for the tooltip).
         * @param {Object} content
         * @return {string}
         */
        renderContent: function(content) {
            if (content) {
                var content_txt = '';
                Object.keys(content).forEach(function (key) {
                    if (key !== 'id')
                        content_txt += key + ':' + content[key] + ', '
                });

                return content_txt;
            }
        }
    }
})();