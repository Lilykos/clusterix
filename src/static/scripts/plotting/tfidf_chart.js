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
    svg.selectAll('.scatterplot-selection circle')
        .data(data)
        .enter()
        .append('circle')
            .attr("r", 4)
            .attr('fill', function (d) { return window.d3Color(d['clx_cluster']); })
            .attr('transform', function(d) { return translate(xScale(d.x), yScale(d.y)); })
            .on("mouseover", showTooltip)
            // .on("mouseout", hideTooltip);
}


function drawTfidf(_data) {
    $("#tf-idf-results").empty();
    var margins = { left: 40, right: 30, top: 30, bottom: 30 },
        width = 500,
        height = 250,
        innerWidth  = width  ,
        innerHeight = height,
        clusters = Object.keys(_data);


//     var options = {
//         block_width: 20,
//         block_height: 20,
//         spacing: 2
//     };
//
//     for (var cluster in _data) {
//     var tfidfItems = _data[cluster];
//
//     var x = d3.scale.linear()
//         .domain([0, d3.max(tfidfItems, function (d) {
//             return d.score;
//         })])
//         .range([0, options.block_width]);
//
//     var svg = d3.select("#tf-idf-results").append('svg')
//         .attr('height', ((tfidfItems.length * (options.block_height + options.spacing)) + options.block_height))
//         .attr('class', 'chart');
//
//     var rect_group = svg
//
//         .selectAll('.tfidf-group')
//         .data(tfidfItems)
//         .enter()
//         .append('g').attr('class', 'tfidf-group')
//         .attr('transform', function (d, i) {
//             return 'translate(0, ' + (i * (options.block_height + options.spacing)) + ')'
//         });
//
//
//     rect_group.append('rect').style('fill', '#f6f7f6').attr({
//             'width': options.block_width,
//             'height': options.block_height
//         });
//
//     rect_group.append('rect')
//         .attr('width', function (d) {
//             return x(d.score);
//         })
//         .attr('height', options.block_height)
//         .style('fill', function (d) {
//             return window.d3Color(cluster);
//         });
//
//     rect_group.append('text').text(function (d) {
//         return d.term + ': ' + d.score;
//     }).style('font-size', '10px').attr('x', 50).attr('y', options.block_height/2);
//
// }

    clusters.forEach(function(cluster) {
        var data = _data[cluster];

        // x, y scaling & axis
        var xScale = d3.scale.linear().range([0, innerWidth]);
        var yScale = d3.scale.ordinal().rangeRoundBands([0, innerHeight]);

        xScale.domain([0, d3.max(data, function (d){ return d.score; })]);
        yScale.domain(data.map(function (d){ return d.term; }));


        // Main SVG
        var yAxis = d3.svg.axis().scale(yScale).orient("left").outerTickSize(0);
        var svg = d3.select("#tf-idf-results")
            .append("svg")
            .attr("width", width)
            .attr("height", height);
        var g = svg.append("g")
            .call(yAxis)
            .attr("transform", translate(margins.left, 0));


        // Bars init
        var bar = g.selectAll('rect')
            .data(data)
            .enter()
            .append('rect')
                .attr('class', 'bar')
                .attr('fill', function (d) { return window.d3Color(cluster); })
                .attr('height', yScale.rangeBand())
                .attr('width', function (d){ return xScale(d.score); })
                .attr('x', 0)
                .attr('y', function (d){ return yScale(d.term); });

        // Bar labels
        g.selectAll(".bartext")
            .data(data)
            .enter()
            .append("text")
            .attr("class", "bartext")
            .attr("x", 10)
            .attr("y", function(d) { return yScale(d.term) + 14; })
            .text(function(d){ return (d.score/1000).toFixed(5); });
    });
}