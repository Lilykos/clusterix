var Utils = (function() {
    return {
        /**
         * Compile and render a template using Handlebars.
         * @param template
         * @param target
         * @param data
         */
        compileTemplate: function(template, target, data) {
            var rendered = Handlebars.compile($(template).html())(data);
            $(target).empty().append(rendered);
        },

        /**
         * Returns treue/ false depending on whether an element is found in an array or not.
         * @param value
         * @param array
         * @returns {boolean}
         */
        inArray: function(value, array) {
            return array.indexOf(value) > -1;
        },

        /**
         * Returns true if array is empty.
         * @param array
         * @returns {boolean}
         */
        isEmpty: function(array) {
            return array.length == 0
        },

        /**
         * Accepts an array of arrays, and returns the common elements of these arrays.
         * @param {Array} arrays
         * @returns {Array}
         */
        getCommonArrayElements: function(arrays) {
            return arrays.shift()
                .reduce(function(res, v) {
                    if (!res.includes(v) && arrays.every(function(a) {
                            return a.indexOf(v) !== -1;
                        }))
                        res.push(v);
                    return res;
            }, []);
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

        debounce: function(fn, delay) {
            var timer = null;
            return function () {
                var context = this;
                var args = arguments;

                clearTimeout(timer);
                timer = setTimeout(function () {
                    fn.apply(context, args);
                }, delay);
            };
        }
    }
})();