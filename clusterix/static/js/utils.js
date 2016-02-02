var Utils = (function() {

    return {

        /**
         * Compile and render a template using Handlebars.
         * @param {string} template
         * @param {string} target
         * @param {Object} data
         * @param {Boolean} emptyElement
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
         * Searches 2 arrays od element ids, and returns an object containing the d3 selectors
         * for the found elements for search/brushing/whatever.
         * @param {Array} first
         * @param {Array} second
         * @returns {{}}
         */
        returnSearchElements: function(first, second) {
            var selectors = {};
            var selectorIDs = Utils.arrayDifference(first, second);

            var scatterSelectors = selectorIDs
                    .map(function(id) { return '.scatterplot .node-' + id; }).join(', '),
                treemapSelectors = selectorIDs
                    .map(function(id) { return '.treemap .node-' + id; }).join(', ');


            // Check if the elements actually exist to avoid exceptions
            // Check for the d3 selector first (exception if empty)
            // And then check if elements were actually returned
            if (treemapSelectors.length) {
                var treemapNodes = d3.selectAll(treemapSelectors);
                if (treemapNodes[0].length) selectors.tree = treemapNodes
            }

            if (scatterSelectors.length) {
                var scatterNodes = d3.selectAll(scatterSelectors);
                if (scatterNodes[0].length) selectors.scatter = scatterNodes
            }

            return selectors;
        },

        /**
         * Attach panel to custom slider.
         * @param {string} buttonID
         * @param {string} contentID
         * @param {int} speed
         */
        attachSliderToPanel: function(buttonID, contentID, speed/*, easing, callback*/) {
            $(buttonID).click(function() {
                $(contentID).fadeThenSlideToggle(buttonID, speed);
            });
        }
    }
})();