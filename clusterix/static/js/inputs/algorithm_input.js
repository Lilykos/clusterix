var AlgorithmInput = (function() {
    var attr = {
        algPanel: '#algorithms-panel',
        algSelect: '#algorithms-selection',

        selectedAlgorithms: []
    };

    /**
     * Initialize the algorithm drop-down and notify the Router for changes.
     */
    function initAlgorithmDropdown() {
        $(attr.algSelect).dropdown({
            onChange: function(val, text, selected) {
                attr.selectedAlgorithms = val;
                Router.set('algorithms', val);
                Router.checkUploadButton();
            }
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

            $(attr.algPanel).fadeIn();
            console.log('Algorithm Input init');
        }
    }
})();