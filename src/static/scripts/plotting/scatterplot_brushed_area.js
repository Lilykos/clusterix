function drawBrushArea(data) {
    var margins = { left: 40, right: 30, top: 30, bottom: 30 },
        width = 500,
        height = 250;

    // Axis init
    var xScale = getXScale(data, width, margins);
    var yScale = getYScale(data, height, margins);

    var zoom = d3.behavior.zoom()
        .x(xScale).y(yScale)
        .scaleExtent([-5, 20])
        .on("zoom", function() {
            svg.selectAll('#brushed-area circle').attr('transform', function(d) {
                return translate(xScale(d.x), yScale(d.y));
            });
        });

    // SVG init
    var svg = d3.select('#brushed-area')
        .append("svg")
            .attr("width", width)
            .attr("height", height)
            .attr('class', 'white-background scatterplot-brushed');

    svg.append('rect')
        .attr('width', width)
        .attr('height', height)
        .attr("x", 0)
        .attr("y", 0)
        .style("stroke-width", 3)
        .attr('fill', 'rgba(1,1,1,0)')
        .call(zoom);

    // Node init
    svg.selectAll('circle')
        .data(data)
        .enter()
        .append('circle')
            .attr("r", 3)
            .attr('fill', function (d) {
                return window.d3Color(d['clx_cluster']);
            })
            .attr('transform', function(d) { return translate(xScale(d.x), yScale(d.y)); });
            // .on("mouseover", showTooltip)
            // .on("mouseout", hideTooltip);
}