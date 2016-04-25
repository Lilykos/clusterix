function ScatterplotMini() {
    var d3Color = d3.scale.category20();
    var attr = {};

    var margins = {
        left: 30,
        right: 30,
        top: 30,
        bottom: 30
    };

    function getXScale() {
        return d3.scale.linear()
            .domain(d3.extent(attr.data, function (d) { return d.x; }))
            .range([0, attr.width - margins.left - margins.right]);
    }

    function getYScale() {
        return d3.scale.linear()
            .domain(d3.extent(attr.data, function (d) { return d.y; }))
            .range([attr.height - margins.top - margins.bottom, 0]);
    }

    function translate(a, b) { return "translate(" + a + "," + b + ")"; }

    return {

        /**
         * Scatterplot minimap.
         */
        init: function(root, width, height, selector, id) {
            attr.width = width;
            attr.height = height;
            attr.kNumber = root.k_num;
            attr.nodeSelector = selector + ' circle';

            // NO centroids needed & filter elements to make minimap less heavy
            attr.data = root.nodes.filter(function(d, index) {
                return !d.isCentroid && index % 5 == 0
            });

            var xScale = getXScale();
            var yScale = getYScale();

            // SVG Init
            var svg = d3.select(selector)
                .append("svg")
                    .attr("width", width)
                    .attr("height", height)
                    .attr('id', 'scatterplot-mini-' + id)
                    .attr('class', 'white-background scatterplot-mini')
                .append("g")
                    .attr("transform", translate(margins.left, margins.top));

            // Node init (minimal, just to show the pattern in small scale)
            svg.selectAll(attr.nodeSelector)
                .data(attr.data)
                .enter()
                .append("circle")
                    .attr("r", 1)
                    .attr("cx", function(d) { return xScale(d.x); })
                    .attr("cy", function(d) { return yScale(d.y); })
                    .attr("fill", function (d) { return d3Color(d.cluster); });

            console.log('Scatterplot mini init.');
        }
    }
}