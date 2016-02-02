function Scatterplot() {
    var attr = {
        d3Color: d3.scale.category10(),
        brushColor: d3.scale.category20(),
        grey: '#7f8c8d'
    };

    var margins = {
        left: 40,
        right: 30,
        top: 30,
        bottom: 30
    };

    var brushID = 0;
    var brushSelected;
    var ext_coords;

    function setIDAndSave(d) {
        if (d.id) {
            Search.addToIndex(d.content);
            return 'node-' + d.id;
        } else {
            return '';
        }
    }

    /**
     *
     * Brushing functions for scatterplot.
     *
     */
    function initBrush(xScale, yScale, svg) {
        var brush = d3.svg.brush()
            .x(xScale)
            .y(yScale)
            .on("brushstart", function() { brushSelected = {}; })
            .on("brush", function () {
                var extent = brush.extent();
                d3.selectAll(attr.nodeSelector + '.node')// NODES ONLY, CENTROIDS DON'T MATTER
                    .attr("fill", function (d) {
                        ext_coords = {
                            x1: xScale(extent[0][0]), x2: xScale(extent[1][0]),
                            y1: yScale(extent[0][1]), y2: yScale(extent[1][1])
                        };

                        var selected =
                            (xScale(d.x) > ext_coords.x1 && xScale(d.x) < ext_coords.x2) &&
                            (yScale(d.y) < ext_coords.y1 && yScale(d.y) > ext_coords.y2);

                        if (selected) brushSelected[d.id] = d.cluster;
                        return selected ? d.fillbackup : attr.grey;
                    });
            })
            .on("brushend", function() {
                var selectedKeys = Object.keys(brushSelected);

                if (!selectedKeys.length){
                    svg.selectAll(attr.nodeSelector + '.node')
                        .attr("fill", function (d) {
                            return d.fillbackup;
                        });

                } else {
                    // if NOT centroid and IN selected keys
                    var data = attr.data.filter(function (d) {
                        if (d.id) return Utils.inArray(d.id.toString(), selectedKeys);
                    });

                    // Create the new scatterplot and keep the brushed area on the map
                    var borderColor = attr.brushColor(ext_coords.x1 + ext_coords.y2);

                    new ScatterplotBrushed()
                        .init({nodes: data}, brushSelected, 350, 140, '#selections-area ul', brushID, attr.d3Color, borderColor);
                    drawBrush(svg, borderColor);

                    brushID++;
                }

                console.log('Brush selected: ' + selectedKeys);
            });

        svg.append("g")
            .attr("class", "brush")
            .call(brush);
    }

    function drawBrush(svg, borderColor) {
        var width = ext_coords.x2 - ext_coords.x1,
            height = ext_coords.y1 - ext_coords.y2;

        svg.append('rect')
            .attr('stroke', borderColor)
            .attr('id', 'scatterplot-brushed-' + brushID)
            .attr('class', 'brushed-area')
            .attr('x', ext_coords.x1)
            .attr('y', ext_coords.y2)
            .attr('width', width)
            .attr('height', height);
    }


    /**
     *
     * Get classes for svg/centroids/nodes.
     *
     */
    function getSVGClasses(d) { return 'white-background ' + attr.class; }

    function getNodeClasses(d) {
        var centroidOrNode = d.isCentroid ? ' centroid centroid-' + d.cluster : ' node';
        return setIDAndSave(d) + centroidOrNode;
    }


    /**
     *
     * Axis/scaling/translation functions
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

    function getAxis(xy) { return '#' + attr.id + ' g.' + xy + '.axis'; }
    function translate(a, b) { return "translate(" + a + "," + b + ")" }

    return {

        /**
         *
         * @param root
         * @param width
         * @param height
         * @param selector
         * @param id
         */
        init: function(root, width, height, selector, id) {
            attr.width = width;
            attr.height = height;
            attr.data = root.nodes;

            attr.idNum = id;
            attr.id = 'scatterplot-' + id;
            attr.class = 'scatterplot';
            attr.nodeSelector = '.scatterplot circle';


            // Axis init
            var xScale = getXScale();
            var yScale = getYScale();

            var xAxis = d3.svg.axis().scale(xScale).orient('bottom').tickPadding(2);
            var yAxis = d3.svg.axis().scale(yScale).orient('left').tickPadding(2);

            // SVG init
            var svg = d3.select(selector)
                .append("svg")
                    .attr("width", width)
                    .attr("height", height)
                    .attr('id', attr.id)
                    .attr('class', getSVGClasses)
                .append("g")
                    .attr("transform", translate(margins.left, margins.top));

            svg.append('rect')
                .attr('width', width)
                .attr('height', height)
                .attr('fill', 'rgba(1,1,1,0)');

            svg.append("g")
                .attr("class", "x axis")
                .attr("transform", translate(0, yScale.range()[0]));
            svg.append("g")
                .attr("class", "y axis");

            svg.selectAll(getAxis('x')).call(xAxis);
            svg.selectAll(getAxis('y')).call(yAxis);

            // Node init
            svg.selectAll(attr.nodeSelector)
                .data(attr.data)
                .enter()
                .append("circle")
                    .attr("r", function(d) { return d.isCentroid ? 8 : 1.5 })
                    .attr('class', getNodeClasses)
                    .attr("fill", function (d) { return attr.d3Color(d.cluster); })
                    .attr('fillbackup', function (d) {
                        d.fillbackup = attr.d3Color(d.cluster);
                        return d.fillbackup;
                    })
                    .attr('transform', function(d) {
                        return translate(xScale(d.x), yScale(d.y));
                    });

            initBrush(xScale, yScale, svg);
            console.log('Scatterplot init.');
        }
    };
}