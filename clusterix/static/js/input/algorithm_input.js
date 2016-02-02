var AlgorithmInput = (function() {
    var attr = {
        algPanel: '#algorithms-panel',
        algSelect: '#algorithms-selection',
        vecSelect: '#vectorizer-selection',
        kmeansSelector: '#kmeans-num',
        bclusterDistSelector: '#distance-method-selection',
        affinitySelector: '#affinity-selection',
        affinityContainerSelector: '#affinity-container',

        selectedAlgorithms: [],
        selectedVectorizer: 'count', //default
        blockBy: '',
        kNumber: 1,
        bclusterDistance: 'single',
        affinity: 'euclidean',

        // Bcluster options
        blockBySelector: '#block-by-field',
        blockByContainer: '#block-by-container',
        blockByTemplate: '#block-by-template'
    };

    /**
     * Renders the block by field according to the user-chosen fields,
     * and sets the variable to the Router.
     */
    function renderBlockByField(data) {
        Utils.compileTemplate(attr.blockByTemplate, attr.blockByContainer, { fields: data }, true);
        Router.data().algorithms.bcluster.blockBy =  data[0];

        $(attr.blockBySelector).dropdown({
            onChange: function(val, text, selected) {
                attr.blockBy = text;
                Router.data().algorithms.bcluster.blockBy = attr.blockBy;
            }
        });
    }

    /**
     * Initialize the algorithm drop-down and notify the Router for changes.
     */
    function initAlgorithmDropdown() {
        $(attr.algSelect).dropdown({
            onChange: function(val, text, selected) {
                attr.selectedAlgorithms = val;
                Router.data().algorithms.algorithmsToUse = val;
                Router.checkUploadButton();
            }
        });
    }

    function initVectorizerDropdown() {
        $(attr.vecSelect).dropdown({
            onChange: function(val, text, selected) {
                attr.selectedVectorizer = val;
                Router.data().vectorizer = val;
            }
        });
    }

    function initBlockClusteringOptions() {
        // Block by
        $(document).on('csv-fields-change', function(ev, fields) {
            renderBlockByField(fields.data);
        });

        // Distance methods
        $(attr.bclusterDistSelector).dropdown({
            onChange: function(val, text, selected) {
                if (val === 'centroid' || val === 'median' || val === 'ward') {
                    $(attr.affinityContainerSelector).hide();
                    attr.affinity = 'euclidean';
                    Router.data().algorithms.bcluster.affinity =  'euclidean';
                } else {
                    $(attr.affinityContainerSelector).show();
                }

                attr.bclusterDistance = val;
                Router.data().algorithms.bcluster.distance = val;
            }
        });

        // Affinity
        $(attr.affinitySelector).dropdown({
            onChange: function(val, text, selected) {
                attr.affinity = val;
                Router.data().algorithms.bcluster.affinity = val;
            }
        });
    }

    function initKMeansOptions() {
        $(attr.kmeansSelector).on('change', function() {
           var kNumber = $(this).val();

            attr.kNumber = kNumber;
            Router.data().algorithms.kmeans.kNumber = kNumber;
        });
    }

    return {

        /**
         * Functionality:
         *      - Initialize Algorithms panel.
         * @constructor
         */
        init: function () {
            initAlgorithmDropdown();
            initVectorizerDropdown();

            initBlockClusteringOptions();
            initKMeansOptions();

            $(attr.algPanel).fadeIn();

            // Panel hide/show
            Utils.attachSliderToPanel('#algorithms-hide', '#algorithms-body', 150);
            console.log('Algorithm Input init');
        }
    }
})();