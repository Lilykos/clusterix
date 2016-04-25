var TermFrequencyChart = (function() {

    return {
        createTFIDFChart: function(clustersWithColors, clustersWithWords/*, tfidf, color*/) {
            Utils.compileTemplate('#tf-idf-template', '#brush-results',
                {clusters: clustersWithColors}, true);

            for (var cluster in clustersWithWords) {
                var tfidfItems = clustersWithWords[cluster];
                
                console.log('Cluster is ' + cluster);
                
                var selector = '#tf-idf-cluster-' + cluster;
                var width = 250 - 60;
                var x = d3.scale.linear()
                        .domain([0, d3.max(tfidfItems, function(d) { return d.tfidf; })])
                        .range([0, width]);

                d3.select(selector)
                    .attr('class', 'chart')
                    .selectAll('div')
                    .data(tfidfItems)
                    .enter()
                    .append('div')
                        .style('width', function(d) { return x(d.tfidf) + 'px'; })
                        .style('background-color', function (d) {
                            return clustersWithColors.filter(function(i) {
                                return i.cluster == cluster;
                            })[0].color;
                        })
                        .style('color', 'white')
                        .text(function(d) { return d.term + ': ' + d.tfidf; });
                
            }

            // tfidf.forEach(function(tfidfList, index) {
            //     var selector = '#tf-idf-cluster-' + index;
            //     var width = 250 - margins.left - margins.right;
            //     var x = d3.scale.linear()
            //             .domain([0, d3.max(tfidfList, function(d) { return d.score; })])
            //             .range([0, width]);
            //
            //     d3.select(selector)
            //         .attr('class', 'chart')
            //         .selectAll('div')
            //         .data(tfidfList)
            //         .enter()
            //         .append('div')
            //             .style('width', function(d) { return x(d.score) + 'px'; })
            //             .style('background-color', clustersWithColors[index].color)
            //             .style('color', 'white')
            //             .text(function(d) { return d.term + ': ' + d.score; });
            // });
        }
    };
})();