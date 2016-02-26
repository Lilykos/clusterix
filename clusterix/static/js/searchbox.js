var SearchBox = (function() {
    var selectors = {
        search: '#search',
        rects: 'rect'
    };

    var colors = {
        grey: '#95a5a6', // FlatUI 'Concrete'
        blue: '#4aa3df'  // FlatUI 'Peter River'
    };

    // Every iteration of searches returns an array of elements. We keep those for faster searches.
    var oldElements = [];

    /**
     * Returns a list of all the cells/nodes that have a name attribute.
     * (In this context, that means all the inner cells (without children) of a treemap.)
     * @returns {rect|jQuery[]} cells
     */
    function getCells() {
        return $(selectors.rects).toArray().filter(function(cell) {
            if (cell.attributes.name) return cell;
        });
    }


    /**
     * Gets a list of queries and finds the right elements.
     * @param {rect|jQuery[]} cells
     * @param {string[]} queries
     */
    function getQueryResults(cells, queries) {
        // We create an array of arrays, that will be used to find the common
        // elements later. We need as many tables as the query strings.
        var cellArrays = [];
        for (var i = 0; i < queries.length; i++) {
            cellArrays.push([]);
            cells.forEach(function (cell) {
                var cellText = cell.attributes.name.textContent.toLowerCase();
                if (cellText.includes(queries[i])) {
                    cellArrays[i].push(cell);
                }
            });
        }

        // There we have all the elements that need to be used now.
        // We need to compare the old elements with the new, in order to:
        //      1. Find the elements that were used, but not anymore (and repaint them).
        //      2. Find only the new elements to be used (and paint them).
        var newElements = Utils.getCommonArrayElements(cellArrays);
        Utils
            .arrayDifference(oldElements, newElements)
            .map(function(cell) { $(cell).attr('fill', cell.attributes.fillBackup.textContent); });
        Utils
            .arrayDifference(newElements, oldElements)
            .map(function(cell) { $(cell).attr('fill', colors.blue); });

        // Replace the used elements for the next iteration
        oldElements = newElements;
    }


    return {
        /**
         * Functionality:
         *      - Creates the event handler for the search function. Takes the arg string and splits
         *        it into different queries. Finds all the cells/nodes that have this string in their name
         *        and paints them accordingly.
         *@constructor
         */
        init: function() {
            $(selectors.search).on('input', Utils.debounce(function() {
                var searchString = $(this).val().toLowerCase();
                var cells = getCells();

                if (searchString) {
                    getQueryResults(cells, searchString.split(' and '));
                } else {
                    oldElements.forEach(function (cell) {
                        $(cell).attr('fill', cell.attributes.fillBackup.textContent)
                    });
                }
            }, 500));

            console.log('Searchbox init.');
        }
    }
})();