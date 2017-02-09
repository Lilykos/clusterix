function Scatterplot() {

    var attr = {
        brushColor: d3.scale.category20(),
        grey: '#7f8c8d'
    };

    var margins = {
        left: 20,
        right: 20,
        top: 20,
        bottom: 20
    };

    var brushID = 0;
    var brushSelectedIDs;
    var ext_coords;

    /**
     * Brushing functions for scatterplot.
     */
    function initBrush(xScale, yScale, svg) {
        var brushStart = function() {
            brushSelectedIDs = new Set();
        };

        var brushAction = function() {
            var extent = brush.extent();
            d3.selectAll(attr.nodeSelector + '.node').each(function (d) {
                ext_coords = {
                    x1: xScale(extent[0][0]), x2: xScale(extent[1][0]),
                    y1: yScale(extent[0][1]), y2: yScale(extent[1][1])
                };

                var selected =
                    (xScale(d.x) > ext_coords.x1 && xScale(d.x) < ext_coords.x2) &&
                    (yScale(d.y) < ext_coords.y1 && yScale(d.y) > ext_coords.y2);

                if (selected) brushSelectedIDs.add(d);
            });
        };

        var brushEnd = function() {
            if (brushSelectedIDs.size) {
                var selectedItemsList = Array.from(brushSelectedIDs);

                new ClusterDetailZone().init(selectedItemsList,
                    '#selections-area ul', brushID, window.d3Color);
            }
        };

        var brush = d3.svg.brush()
            .x(xScale)
            .y(yScale)
            .on("brushstart", brushStart)
            .on("brush", brushAction)
            .on("brushend", brushEnd);

        svg.append("g")
            .attr("class", "brush")
            .call(brush);
    }

    /**
     * Axis/scaling/translation functions
     */
    function getXScale() {
        return d3.scale.linear().domain(d3.extent(attr.data, function (d) { return + d.x; }))
            .range([0, attr.width - margins.left - margins.right]);
    }

    function getYScale() {
        return d3.scale.linear().domain(d3.extent(attr.data, function (d) { return + d.y; }))
            .range([attr.height - margins.top - margins.bottom, 0]);
    }

    function translate(a, b) { return "translate(" + a + "," + b + ")" }

    return {

        /**
         * Scatterplot with brush feature.
         */
        init: function(root, width, height, selector, id) {
            attr.width = width;
            attr.height = height;
            attr.nodeSelector = '.scatterplot circle';
            attr.data = root.nodes;


            // Scaling init
            var xScale = getXScale();
            var yScale = getYScale();

            // SVG init
            var svg = d3.select(selector)
                .append("svg")
                    .attr("width", width)
                    .attr("height", height)
                    .attr('id', 'scatterplot-' + id)
                    .attr('class', 'white-background border-white-round scatterplot')
                .append("g")
                    .attr("transform", translate(margins.left, margins.top));

            svg.append('rect')
                .attr('width', width)
                .attr('height', height)
                .attr('fill', 'rgba(1,1,1,0)');

            // Node init
            svg.selectAll(attr.nodeSelector)
                .data(attr.data)
                .enter()
                .append("circle")
                    .attr("r", function(d) { return d.isCentroid ? 8 : 1.5 })
                    .attr('class', function(d) {
                        return d.isCentroid ? 'centroid centroid-' + d.cluster : 'node node-' + d.id;
                    })
                    .attr("fill", function (d) { return window.d3Color(d.cluster); })
                    .attr('fillbackup', function (d) {
                        d.fillbackup = window.d3Color(d.cluster);
                        return d.fillbackup;
                    })
                    .attr('transform', function(d) { return translate(xScale(d.x), yScale(d.y)); });

            initBrush(xScale, yScale, svg);
            console.log('Scatterplot init.');
        }
    };
}