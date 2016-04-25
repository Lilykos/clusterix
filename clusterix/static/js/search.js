var Search = (function() {
    var oldElements = [];
    var searchSelector = '#search';
    var grey = '#7f8c8d';
    var url = '/search';



    function searchInScatterplot(newElements) {
        d3.selectAll('.node')
            .attr('fill', function(d) {
                return Utils.inArray(d.id, newElements)
                    ? d.fillbackup
                    : grey;
            })
            .attr('r', function(d) {
                return Utils.inArray(d.id, newElements)
                    ? 4 : 1
            });
    }

    function repaintScatterplot() {
        d3.selectAll('.node')
            .attr('fill', function(d) { return d.fillbackup; })
            .attr('r', 1.5);
    }


    /**
     * Searches 2 arrays od element ids, and returns an object containing the d3 selectors
     * for the found elements for search/brushing/whatever.
     * @param {Array} first
     * @param {Array} second
     * @returns {{}}
     */
    function returnSearchElements(first, second) {
        var selectors = {};
        var selectorIDs = Utils.arrayDifference(first, second);

        var scatterSelectors = selectorIDs
                .map(function(id) { return '.node .node-' + id; }).join(', '),
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
    }
    
    /**
     * Color the ids of the newly searched elements.
     */
    function colorNewElements(newElements, oldElements) {
        var selectors = returnSearchElements(newElements, oldElements);
        if ('tree' in selectors) {
            selectors.tree.attr('fill', function(d) { return d.fillbackup; });
        }
        if ('scatter' in selectors) {
            selectors.scatter.attr('fill', function(d) { return d.fillbackup; }).attr('r', 2.5);
        }
    }

    /**
     * Return the original fill to the elements that the search no longer applies to.
     */
    function restoreUnusedElements(allElements, newElements) {
        //var selectors = Utils.returnSearchElements(oldElements, newElements);
        var selectors = returnSearchElements(allElements, newElements);

        if (allElements.length === selectors.scatter[0].length) {

            // no query, everything colored
            if ('tree' in selectors) {
                selectors.tree.attr('fill', function(d) { return d.fillbackup; });
            }
            if ('scatter' in selectors) {
                selectors.scatter.attr('fill', function(d) { return d.fillbackup; }).attr('r', 1.5);
            }
        } else {

            // query, grey out remaining elements
            if ('tree' in selectors) {
                selectors.tree.attr('fill', grey);
            }
            if ('scatter' in selectors) {
                selectors.scatter.attr('fill', grey).attr('r', 1);
            }
        }
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
            $(searchSelector).on('input', Utils.debounce(function() {
                var query = $(this).val();

                $.ajax({
                    type: 'POST',
                    url: url,
                    data: query,
                    cache: false,
                    contentType: false,
                    processData: false,
                    success: function(data){
                        var newElements = data['ids'];

                        if (newElements.length) {
                            console.log('NEW ELEMENTS SEARCHED AND FOUND');
                            console.log(newElements);

                            //colorNewElements(newElements);
                            //restoreUnusedElements(newElements);

                            searchInScatterplot(newElements)
                        } else {
                            repaintScatterplot();
                        }

                        oldElements = newElements;
                    }
                });
            }, 400));
        }
    };
})();