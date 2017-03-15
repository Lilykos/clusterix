var TermFrequencyChart = (function () {

    var options = {
        block_width: 20,
        block_height: 20,
        spacing: 2
    };

    return {
        createTFIDFChart: function (tfidfByCluster) {
            for (var cluster in tfidfByCluster) {
                var tfidfItems = tfidfByCluster[cluster],
                    selector = '#tf-idf-cluster-' + cluster;

                var x = d3.scale.linear()
                    .domain([0, d3.max(tfidfItems, function (d) {
                        return d.score;
                    })])
                    .range([0, options.block_width]);

                var svg = d3.select(selector).append("svg")
                    .attr('height', ((tfidfItems.length * (options.block_height + options.spacing)) + options.block_height))
                    .attr('class', 'chart');

                var rect_group = svg

                    .selectAll('.tfidf-group')
                    .data(tfidfItems)
                    .enter()
                    .append('g').attr('class', 'tfidf-group')
                    .attr('transform', function (d, i) {
                        return 'translate(0, ' + (i * (options.block_height + options.spacing)) + ')'
                    });


                rect_group.append('rect').style('fill', '#f6f7f6').attr({
                        'width': options.block_width,
                        'height': options.block_height
                    });

                rect_group.append('rect')
                    .attr('width', function (d) {
                        return x(d.tfidf);
                    })
                    .attr('height', options.block_height)
                    .style('fill', function (d) {
                        return clustersWithColors.filter(function (i) {
                            return i.cluster == cluster;
                        })[0].color;
                    });

                rect_group.append('text').text(function (d) {
                    return d.term + ': ' + d.tfidf;
                }).style('font-size', '10px').attr('x', 50).attr('y', options.block_height/2);

            }

        }
    };
})();