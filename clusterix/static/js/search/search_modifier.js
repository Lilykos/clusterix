var SearchModifier = (function() {
    var grey = '#7f8c8d';

    return {
        /**
         * Color the ids of the newly searched elements.
         * @param {Array} newElements
         * @param {Array} oldElements
         */
        colorNewElements: function(newElements, oldElements) {
            var selectors = Utils.returnSearchElements(newElements, oldElements);
            if ('tree' in selectors) {
                selectors.tree.attr('fill', function(d) { return d.fillbackup; });
            }
            if ('scatter' in selectors) {
                selectors.scatter.attr('fill', function(d) { return d.fillbackup; }).attr('r', 2.5);
            }
        },

        /**
         * Return the original fill to the elements that the search no longer applies to.
         */
        restoreUnusedElements: function(allElements, newElements) {
            //var selectors = Utils.returnSearchElements(oldElements, newElements);
            var selectors = Utils.returnSearchElements(allElements, newElements);

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
    }
})();