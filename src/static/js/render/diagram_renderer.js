var Renderer = (function() {
    var sizeMap = {width: 900, height: 400};
    var sizeMini = {width: 200, height: 100};

    var selectors = {
        diagramSelector: '#vizualization-area',
        infoSelector: '#selections-area ul',
        miniSelector: '#viz-mini',
        resultsSelector: '#brush-results',
        distributionSelector: '#cluster-comparison',
        tfidfSelector: '#tf-idf-results'
    };

    var idNumber = 0;

    function getNewId() {
        idNumber++;
        return idNumber;
    }

    return {

        get_selector: function(selector) { return selectors[selector]; },

        /**
         * Renders the returned data.
         * @param data
         */
        render: function(data) {
            var id = getNewId();

            // Empty the div, we only want a single scatterplot
            // Also empty the brushed content
            $(selectors.diagramSelector).empty();
            $(selectors.infoSelector).empty();
            $(selectors.tfidfSelector).empty();
            $(selectors.distributionSelector).empty();

            new Scatterplot().init(data['cluster_results'], sizeMap.width, sizeMap.height, selectors.diagramSelector, id);
            // new ScatterplotMini().init(data, sizeMini.width, sizeMini.height, selectors.miniSelector, id);
        }
    }

})();