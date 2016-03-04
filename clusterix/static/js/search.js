var Search = (function() {
    var index;
    var store;
    var fields;
    var fieldNames;

    var searchSelector = '#search';

    var colors = {
        grey: '#95a5a6', // FlatUI 'Concrete'
        blue: '#4aa3df'  // FlatUI 'Peter River'
    };

    var oldElements;

    /**
     * Every time a new file is uploaded, initialize lunr, using the fields of the uploaded file
     * as the indexing fields, and the provided scaling as the boost.
     */
    function init_search_engine() {
        $(document).on('data-uploaded', function(ev, fields_used) {
            fields = fields_used.data;
            fieldNames = fields.map(function (field) {return field.name});
            store = {};

            index = lunr(function() {
                var $this = this;
                $this.ref('id');
                fields.forEach(function(field) { $this.field(field.name, {boost: field.scale}) });
            });
        });

        oldElements = [];
    }

    /**
     * Use lunr to get the ids of the elements that contain the query, and color them
     * for inspection. Each id is used as a class and has a 'fill' and 'fillbackup' attribute.
     *
     * We also use a debounce function to wai a bit before searching, to avoid computations.
     */
    function init_search_results() {
        $(searchSelector).on('input', Utils.debounce(function() {
            var query = $(this).val().toLowerCase();
            var newElements = search(query).map(function(i) { return i.ref; });

            // Array difference functions, in orderto figure out:
            //      1. New elements that need to be colored.
            //      2. Old elements that need to revert to the original coloring.
            Utils.arrayDifference(oldElements, newElements).map(function(id) {
                $('.' + id).get().forEach(function(el) {
                    $(el).attr('fill', $(el).attr('fillbackup'));
                });
            });

            Utils.arrayDifference(newElements, oldElements).map(function(id) {
                $('.' + id).attr('fill', colors.blue);
            });

            // Replace the used elements for the next iteration
            oldElements = newElements;
        }, 500));
    }

    /**
     * Search based on lunr.
     * @param {string} query
     * @returns {*|Number}
     */
    function search(query) {
        return index.search(query);
    }

    return {

        /**
         * Functionality:
         *      - Every time we upload a new file, re-initialize the search index.
         *      - Handle how search bar works.
         *
         * Important: The id of each element is used as a class, to make search easier and
         * have the option for representation of multiple elements with the same id.
         * @constructor
         */
        init: function() {
            init_search_engine();
            init_search_results();
        },

        /**
         * Add an item to the search index, by indexing all the fields from the content.
         * @param {Object} content
         */
        addToIndex: function(content) {
            if (Utils.inArray(content.id, Object.keys(store))) return;

            var item = {id: content.id};
            fieldNames.forEach(function(field) {
                item[field] = content[field]
            });

            index.add(item);
            store[item.id] = content;
        },

        /**
         * Debugging function, returns all the search data/attributes.
         * @returns {{index: *, store: *, fields: *}}
         */
        data: function() {
            return {index: index, store: store, fields: fields}
        },

        /**
         * Debug function, used for searching.
         * @param query
         * @returns {*|Number}
         */
        search: function(query) {
            return search(query)
        }
    };
})();