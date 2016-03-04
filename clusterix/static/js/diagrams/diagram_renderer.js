var Renderer = (function() {
    var sizeMap = {width: 900, height: 675};
    var sizeMini = {width: 260, height: 195};

    var selectors = {
        plotID: '#viz',
        miniID: '#viz-mini'
    };

    return {

        /**
         * Renders the returned data.
         * @param data
         */
        render: function(data) {
            var keys = Object.keys(data);

            keys.forEach(function(key) {
                switch (key) {
                    case 'kmeans':
                        new Scatterplot().init(data[key], sizeMap, sizeMini, selectors.plotID, selectors.miniID);
                        break;
                    case 'bcluster':
                        new Treemap().init(data[key], sizeMap, sizeMini, selectors.plotID, selectors.miniID);
                        break;
                }
            });
        }
    }

})();