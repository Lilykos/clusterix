function scatterplot(data) {
    // data model
    // [
    //     {'clx_cluster': 0, 'clx_id': 2, 'x': 2.658062848683116e-16, 'y': 1.7320508075688774},
    //     {'clx_cluster': 1, 'clx_id': 1, x': 1.5034503553765397, 'y': 0.0}, ...
    // ]

    var margins = {left: 20, right: 20, top: 20, bottom: 20},
        height = 550,
        width = 1100;

    // Empty everything in case of new scatterplot
    $('#vizualization-area').empty();
    $('#brushed-area').empty();
    $('#tf-idf-results').empty();

    // Scaling init
    var xScale = getXScale(data, width, margins);
    var yScale = getYScale(data, height, margins);

    // SVG init
    var svg = d3.select('#vizualization-area')
        .append("svg")
            .attr("width", width)
            .attr("height", height)
            .attr('class', 'white-background scatterplot')
        .append("g")
            .attr("transform", translate(margins.left, margins.top));

    svg.append('rect')
        .attr('width', width)
        .attr('height', height)
        .attr('fill', 'rgba(1,1,1,0)');

    // Node init
    svg.selectAll('.scatterplot circle')
        .data(data)
        .enter()
        .append("circle")
            .attr("r", 3)
            .attr('opacity', 0.5)
            .attr("fill", function (d) { return window.d3Color(d['clx_cluster']); })
            .attr('transform', function(d) { return translate(xScale(d.x), yScale(d.y)); });

    initBrush(xScale, yScale, svg);
}