var AlgorithmInput = (function() {
    var attr = {
        algPanel: '#algorithms-panel',
        algSelect: '#algorithms-selection',

        selectedAlgorithms: []
    };

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
        init: function () {
            initAlgorithmDropdown();

            $(attr.algPanel).fadeIn();
            console.log('Algorithm Input init');
        }
    }
})();