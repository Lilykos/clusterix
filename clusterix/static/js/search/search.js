var Search = (function() {
    var ids;
    var index;
    var store;
    var fields;
    var fieldNames;

    var oldElements;
    var searchSelector = '#search';

    /**
     * Every time a new file is uploaded, initialize lunr, using the fields of the uploaded file
     * as the indexing fields, and the provided scaling as the boost.
     */
    function init_search_engine() {
        $(document).on('data-uploaded', function(ev, fields_used) {
            fields = fields_used.data;
            fieldNames = fields.map(function (field) {return field.name});
            store = {allIDs: []};

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

            SearchModifier.colorNewElements(newElements, oldElements);
            //SearchModifier.restoreUnusedElements(newElements, oldElements);
            SearchModifier.restoreUnusedElements(Search.data().store.allIDs, newElements);

            oldElements = newElements;
        }, 250));
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
            store.allIDs.push(
                parseInt(item.id)
            )
        },

        /**
         * Debugging function, returns all the search data/attributes.
         * @returns {{index: *, store: *, fields: *}}
         */
        data: function() {
            return {index: index, store: store, fields: fields, ids: ids}
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