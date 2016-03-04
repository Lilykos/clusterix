function Scatterplot() {
    var attr = {
        d3Color: d3.scale.category10(),
        darkgrey: '#7f8c8d',

        root: {},
        width: 0,
        height: 0
    };

    var margins = {
        "left": 40,
        "right": 30,
        "top": 30,
        "bottom": 30
    };

    var brushSelected;

    /**
     * Brush selection init. Click and drag on the svg and return the selected documents.
     * @param xScale
     * @param yScale
     * @param svg
     */
    function initBrush(xScale, yScale, svg) {
        var brushstart = function() {
            brushSelected = {};
        };

        var brushmove = function () {
            var extent = brush.extent();
            d3.selectAll("g.node")
                .select("circle")
                .style("fill", function (d) {
                    var selected =
                        (xScale(d.x) > xScale(extent[0][0]) && xScale(d.x) < xScale(extent[1][0])) &&
                        (yScale(d.y) < yScale(extent[0][1]) && yScale(d.y) > yScale(extent[1][1]));

                    if (selected) brushSelected[d.content.id] = d;
                    return selected ? attr.darkgrey : attr.d3Color(d.cluster);
                });
        };
        var brushend = function() {
            console.log('Brush selected: ' + Object.keys(brushSelected));
        };

        var brush = d3.svg.brush()
            .x(xScale).y(yScale)
            .on("brushstart", brushstart)
            .on("brush", brushmove)
            .on("brushend", brushend);

        svg.append("g")
            .attr("class", "brush")
            .call(brush);
    }


    function initZoom(xScale, yScale, svg, xAxis, yAxis) {
        var zoom = d3.behavior.zoom() // we first define our zoom behaviour
            .x(xScale)
            .y(yScale)
            .scaleExtent([1, 5])
            .on("zoom", function() {

                // what happens when we zoom
                // we want to select all our nodes and make them bigger according to the scale factor recorded by d3,
                // computed from the users interaction with the mouse (d3.event.scale). We want the position to stay
                // relatively constant as well. This is achieved through the use of the x and y scales to position
                // the component appropriately.

                d3.selectAll("g.x.axis").call(xAxis);
                d3.selectAll("g.y.axis").call(yAxis);

                svg.selectAll("g.node").attr("transform", function(d){
                    // we can still get access to the data properties of the items,
                    // so pulling out the price and rating is very easy.
                    return "translate(" + xScale(d.x) + "," + yScale(d.y) + ")scale(" + d3.event.scale + ")"
                });
            });

        svg.call(zoom)
            .append('rect')
            .attr('width', attr.width)
            .attr('height', attr.height)
            .attr('fill', 'rgba(1,1,1,0)');
    }

    return {

        /**
         *
         * @constructor
         * @param {Object} root A d3-compatible json, that contains the nodes/structure to create a treemap.
         * @param {{width:int, height:int}} scatterAttrs
         * @param {{width:int, height:int}} miniAttrs
         * @param {string} plotID
         * @param {string} miniID
         */
        init: function(root, scatterAttrs, miniAttrs, plotID, miniID) {
            attr.root = root;
            attr.width = scatterAttrs.width;
            attr.height = scatterAttrs.height;
            attr.scatterplotID = plotID;
            attr.miniID = miniID;

            var data = attr.root.items,
                centroids = attr.root.centroids,
                kNumber = attr.root.k_num;

            var tip = d3.tip().attr('class', 'd3-tip').html(function(d) {
                return Utils.renderContent(d.content);
            });


            // Axis init
            var xScale = d3.scale.linear()
                .domain(d3.extent(data, function (d) { return d.x; }))
                .range([0, attr.width - margins.left - margins.right]);
            var yScale = d3.scale.linear()
                .domain(d3.extent(data, function (d) { return d.y; }))
                .range([attr.height - margins.top - margins.bottom, 0]);

            var xAxis = d3.svg.axis().scale(xScale).orient("bottom").tickPadding(2);
            var yAxis = d3.svg.axis().scale(yScale).orient("left").tickPadding(2);


            var svg = d3.select(attr.scatterplotID)
                .append("svg")
                    .attr("width", attr.width)
                    .attr("height", attr.height)
                .append("g")
                    .attr("transform", "translate(" + margins.left + "," + margins.top + ")");

            svg.append("g")
                .attr("class", "x axis")
                .attr("transform", "translate(0," + yScale.range()[0] + ")");
            svg.append("g")
                .attr("class", "y axis");

            svg.selectAll("g.y.axis").call(yAxis);
            svg.selectAll("g.x.axis").call(xAxis);
            svg.call(tip);



            $(document).on('keydown', function() {
                if (event.ctrlKey) {
                    console.log('Brushing Enabled');

                    svg.selectAll('rect').remove();
                    initBrush(xScale, yScale, svg);
                } else if (event.shiftKey) {
                    console.log('Zooming enabled');

                    svg.selectAll('.brush').remove();
                    initZoom(xScale, yScale, svg, xAxis, yAxis);
                }
            });


            // Nodes init
            var nodes = svg.selectAll("g.node")
                .data(data, function (d) { return d.content.id;})
                .enter()
                .append("g")
                    .attr("class", "node")
                    .attr('transform', function (d) { return "translate(" + xScale(d.x) + "," + yScale(d.y) + ")"; });

            nodes.append("circle")
                .attr("r", 3)
                .attr("class", "dot")
                .style("fill", function (d) { return attr.d3Color(d.cluster); })
                .on('mouseover', tip.show)
                .on('mouseout', tip.hide);

            //initBrush(xScale, yScale, svg);
        }
    };
}