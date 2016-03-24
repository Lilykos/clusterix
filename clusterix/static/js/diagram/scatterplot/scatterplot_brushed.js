function ScatterplotBrushed() {
    var attr = {
        grey: '#7f8c8d'
    };

    var margins = {
        left: 40,
        right: 30,
        top: 30,
        bottom: 30
    };

    /**
     *
     * Axis/scaling/translation/svg functions
     *
     */
    function getXScale() {
        return d3.scale.linear().domain(d3.extent(attr.data, function (d) { return +d.x; }))
            .range([0, attr.width - margins.left - margins.right]);
    }

    function getYScale() {
        return d3.scale.linear().domain(d3.extent(attr.data, function (d) { return +d.y; }))
            .range([attr.height - margins.top - margins.bottom, 0]);
    }

    function translate(a, b) { return "translate(" + a + "," + b + ")" }
    function getSVGClasses(d) { return 'white-background ' + attr.class; }



    function showTermFreq() {
        var clusterNum = attr.term_freq.length;
        var clustersWithColors = [];

        for (var i = 0; i < clusterNum; i++) {
            clustersWithColors.push({ cluster: i, color: attr.d3Color(i) });
        }
        TermFrequencyChart.createTFChart(clustersWithColors, attr.term_freq);
        TermFrequencyChart.createTFIDFChart(clustersWithColors, attr.tfidf);
    }



    function getNodesData(ids) {

    }

    return {

        init: function(root, elementIDs, width, height, selector, id, color, borderColor) {
            attr.width = width;
            attr.height = height;
            attr.data = root.nodes;
            attr.d3Color = color;

            attr.id = 'scatterplot-selection-' + id;
            attr.class = 'scatterplot-selection';
            attr.nodeSelector = '.scatterplot-selection circle';

            // Axis init
            var xScale = getXScale();
            var yScale = getYScale();

            // SVG init

            var listItem = d3.select(selector).append('li');

            //var svg = d3.select(selector)
            var svg = listItem.append("svg")
                .attr("width", width)
                .attr("height", height)
                .attr('class', getSVGClasses)
                .attr('border', 3)
                .attr('margin', '1%');

            svg.append('rect')
                .attr('width', width)
                .attr('height', height)
                .attr("x", 0)
       			.attr("y", 0)
                .style("stroke", borderColor)
       			.style("stroke-width", 3)
                .attr('fill', 'rgba(1,1,1,0)');

            // Node init
            svg.selectAll(attr.nodeSelector)
                .data(attr.data)
                .enter()
                .append("circle")
                    .attr("r", 3)
                    .attr('class', function(d) { return 'node node-' + d.content.id; })
                    .attr("fill", function (d) { return attr.d3Color(d.cluster); })
                    .attr('fillbackup', function (d) {
                        d.fillbackup = attr.d3Color(d.cluster);
                        return d.fillbackup;
                    })
                    .attr('transform', function(d) {
                        return translate(xScale(d.x), yScale(d.y));
                    });

            var zoom = d3.behavior.zoom()
                .x(xScale)
                .y(yScale)
                .scaleExtent([-5, 15])
                .on("zoom", function() {
                    svg.selectAll(attr.nodeSelector).attr('transform', function(d) {
                        return translate(xScale(d.x), yScale(d.y));
                    });
                });

            svg.call(zoom);
            //getNodesData(elementIDs);
        }
    };
}