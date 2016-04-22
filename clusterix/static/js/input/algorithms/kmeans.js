var KMeans = (function() {
    var kmeansSelector = '#kmeans-num';

    return {
        init: function() {
            $(kmeansSelector).on('change', function() {
                Router.data().algorithms.kmeans.kNumber = $(this).val();
            });
        }
    }
})();