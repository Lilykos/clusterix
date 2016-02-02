var TermFrequencyChart = (function() {
    var margins = {
        left: 40,
        right: 30,
        top: 30,
        bottom: 30
    };

    return {

        createTFChart: function(clustersWithColors, term_freq) {
            Utils.compileTemplate('#tf-template', '#results', {clusters: clustersWithColors}, true);
            Utils.attachSliderToPanel('#tf-hide', '#tf-body', 150);

            term_freq.forEach(function(freqList, index) {
                var selector = '#tf-cluster-' + index;
                var width = 250 - margins.left - margins.right;
                var x = d3.scale.linear()
                        .domain([0, d3.max(freqList, function(d) { return d.total; })])
                        .range([0, width]);

                d3.select(selector)
                    .attr('class', 'chart')
                    .selectAll('div')
                    .data(freqList)
                    .enter()
                    .append('div')
                        .style('width', function(d) { return x(d.total) + 'px'; })
                        .style('background-color', '#bdc3c7')
                    .append('div')
                            .style('width', function(d) { return x(d.freq) + 'px'; })
                            .style('background-color', clustersWithColors[index].color)
                            .style('color', 'white')
                            .text(function(d) { return d.term + ': (' + d.freq + '/' + d.total + ')'; })
            });
        },

        createTFIDFChart: function(clustersWithColors, tfidf, color) {
            Utils.compileTemplate('#tf-idf-template', '#results', {clusters: clustersWithColors}, false);
            Utils.attachSliderToPanel('#tf-idf-hide', '#tf-idf-body', 150);

            tfidf.forEach(function(tfidfList, index) {
                var selector = '#tf-idf-cluster-' + index;
                var width = 250 - margins.left - margins.right;
                var x = d3.scale.linear()
                        .domain([0, d3.max(tfidfList, function(d) { return d.score; })])
                        .range([0, width]);

                d3.select(selector)
                    .attr('class', 'chart')
                    .selectAll('div')
                    .data(tfidfList)
                    .enter()
                    .append('div')
                        .style('width', function(d) { return x(d.score) + 'px'; })
                        .style('background-color', clustersWithColors[index].color)
                        .style('color', 'white')
                        .text(function(d) { return d.term + ': ' + d.score; });
            });
        }
    };
})();