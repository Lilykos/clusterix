 /**
 * Axis/scaling/translation/svg functions
 */
function getXScale(data, w, m) {
    return d3.scale.linear().domain(d3.extent(data, function (d) { return +d.x; }))
        .range([0, w - m.left - m.right]);
}

function getYScale(data, h, m) {
    return d3.scale.linear().domain(d3.extent(data, function (d) { return +d.y; }))
        .range([h - m.top - m.bottom, 0]);
}

function translate(a, b) { return "translate(" + a + "," + b + ")" }


function scatterplot(data) {
    var margins = {left: 20, right: 20, top: 20, bottom: 20},
        height = 550,
        width = 1100;

    // Empty everything in case of new scatterplot
    $('#vizualization-area').empty();
    $('#brushed-area').empty();
    $('#cluster-comparison').empty();
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
            .attr("r", 2)
            .attr('opacity', 0.5)
            .attr("fill", function (d) { return window.d3Color(d['clx_cluster']); })
            .attr('transform', function(d) { return translate(xScale(d.x), yScale(d.y)); });

    initBrush(xScale, yScale, svg);
}