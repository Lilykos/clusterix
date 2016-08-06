function ClusterDetailZone() {
    var attr = {
        grey: '#7f8c8d',
        url: '/tfidf',
        d3Color: null,
        clustersWithColors: [],
        dataToCluster: {}
    };


    function translate(a, b) { return "translate(" + a + "," + b + ")" }

    /**
     * TF-IDF Display
     */
    function renderTFIDF(clusteredTFIDFs) {
        attr.clustersWithColors = [];
        for (var cluster in clusteredTFIDFs) {

            attr.clustersWithColors.push({
                cluster: cluster,
                color: attr.d3Color(cluster)
            });
        }
        TermFrequencyChart.createTFIDFChart(attr.clustersWithColors, clusteredTFIDFs)
    }

    function renderFullMetrics(data, cluster_mapping) {
        $(Renderer.get_selector('distributionSelector')).empty();
        ClusterDistributionChart.init(data, cluster_mapping, attr.d3Color)
    }

    function getMetrics(rootData) {
        attr.dataToCluster = {};
        rootData.forEach(function(d) { attr.dataToCluster[d.id] = d.cluster; });

        var data = new FormData();
        data.append('ids', JSON.stringify(attr.dataToCluster));

        $.ajax({
            type: 'POST',
            url: attr.url,
            data: data,
            cache: false,
            contentType: false,
            processData: false,
            success: function(data){
                var clusteredTFIDFs = data['tfidf_metrics'];
                renderTFIDF(clusteredTFIDFs);
            }
        });


    }

    function getContent() {
        var data = new FormData();
        data.append('ids', JSON.stringify(
            attr.data.map(function(d) { return d.id; })
        ));
        
        $.ajax({
            type: 'POST',
            url: '/content',
            data: data,
            cache: false,
            async: false,
            contentType: false,
            processData: false
        })
        .success(function(data) {
            attr.content = data['content'];
            renderFullMetrics(attr.content, attr.dataToCluster);
        });
    }

    return {

        init: function(rootData, selector, id, colors) {
            attr.data = rootData;
            attr.nodeSelector = '.scatterplot-selection circle';
            attr.d3Color = colors;

            getMetrics(rootData);
            getContent();

            var tip = d3.tip()
                .attr("class", "d3-tip")
                .html(function(d) {
                    return attr.content[d.id].text;
                });

        }
    };
}