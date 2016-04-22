var AlgorithmInput = (function() {
    var attr = {
        algPanel: '#algorithms-panel',
        algSelect: '#algorithms-selection',
        vecSelect: '#vectorizer-selection'
    };

    /**
     * Initialize the algorithm drop-down and notify the Router for changes.
     */
    function initAlgorithmSelection() {
        $(attr.algSelect).dropdown({
            onChange: function(val, text, selected) {
                Router.data().algorithms.algorithmsToUse = val;
                Router.checkUploadButton();
            }
        });
    }

    function initVectorizerSelection() {
        $(attr.vecSelect).dropdown({
            onChange: function(val, text, selected) {
                Router.data().vectorizer = val;
            }
        });
    }

    return {

        /**
         * Functionality:
         *      - Initialize Algorithms panel.
         *      - Init the respective algorithm options.
         * @constructor
         */
        init: function () {
            initAlgorithmSelection();
            initVectorizerSelection();

            // init algorithms & options
            KMeans.init();
            HCluster.init();

            // show the panel
            $(attr.algPanel).fadeIn();

            // Panel hide/show init
            Utils.attachSliderToPanel('#algorithms-hide', '#algorithms-body', 150);
            console.log('Algorithm Input init');
        }
    }
})();