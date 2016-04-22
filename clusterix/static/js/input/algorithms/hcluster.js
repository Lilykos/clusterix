var HCluster = (function() {

    var attr = {
        bclusterDistSelector: '#distance-method-selection',
        affinitySelector: '#affinity-selection',
        affinityContainerSelector: '#affinity-container'

        // Bcluster options
        //blockBySelector: '#block-by-field',
        //blockByContainer: '#block-by-container',
        //blockByTemplate: '#block-by-template'
    };

    ///**
    // * Renders the block by field according to the user-chosen fields,
    // * and sets the variable to the Router.
    // */
    //function renderBlockByField(data) {
    //    Utils.compileTemplate(attr.blockByTemplate, attr.blockByContainer, { fields: data }, true);
    //    Router.data().algorithms.bcluster.blockBy =  data[0];
    //
    //    $(attr.blockBySelector).dropdown({
    //        onChange: function(val, text, selected) {
    //            attr.blockBy = text;
    //            Router.data().algorithms.bcluster.blockBy = attr.blockBy;
    //        }
    //    });
    //}
    //
    //function initBlockClusteringOptions() {
    //    // Block by
    //    $(document).on('csv-fields-change', function(ev, fields) {
    //        renderBlockByField(fields.data);
    //    });
    //}

    return {
        init: function() {
            // Distance methods
            $(attr.bclusterDistSelector).dropdown({
                onChange: function(val, text, selected) {
                    if (val === 'centroid' || val === 'median' || val === 'ward') {
                        $(attr.affinityContainerSelector).hide();
                        Router.data().algorithms.bcluster.affinity =  'euclidean';
                    } else {
                        $(attr.affinityContainerSelector).show();
                    }
                    Router.data().algorithms.bcluster.distance = val;
                }
            });

            // Affinity
            $(attr.affinitySelector).dropdown({
                onChange: function(val, text, selected) {
                    Router.data().algorithms.bcluster.affinity = val;
                }
            });
        }
    }
})();