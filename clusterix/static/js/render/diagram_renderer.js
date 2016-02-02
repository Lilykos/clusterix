var Renderer = (function() {
    var sizeMap = {width: 1100, height: 460};
    var sizeMini = {width: 200, height: 100};

    var selectors = {
        diagramSelector: '#vizualization-area',
        infoSelector: '#selections-area ul',
        miniSelector: '#viz-mini'
    };

    var idNumber = 0;

    function getNewId() {
        idNumber++;
        return idNumber;
    }

    return {

        /**
         * Renders the returned data.
         * @param data
         */
        render: function(data) {
            var keys = Object.keys(data);
            var id = getNewId();

            // Empty the div, we only want a single scatterplot
            // Also empty the brushed content
            $(selectors.diagramSelector).empty();
            $(selectors.infoSelector).empty();

            keys.forEach(function(key) {
                switch (key) {
                    case 'kmeans':
                        new Scatterplot().init(data[key], sizeMap.width, sizeMap.height, selectors.diagramSelector, id);
                        new ScatterplotMini().init(data[key], sizeMini.width, sizeMini.height, selectors.miniSelector, id);

                        break;

                    case 'bcluster':
                        new Treemap().init(data[key], sizeMap.width, sizeMap.height, selectors.diagramSelector, id);
                        new TreemapMini().init(data[key], sizeMini.width, sizeMini.height, selectors.miniSelector, id);

                        break;
                }
            });
        }
    }

})();