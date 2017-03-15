function scatterplotMatrix(data) {
    $('#matrix-area').empty();
    var width = 1100,
        size = 250,
        padding = 20;

    // Axis/Scale
    var x = d3.scale.linear().range([padding / 2, size - padding / 2]),
        y = d3.scale.linear().range([size - padding / 2, padding / 2]);

    var xAxis = d3.svg.axis().scale(x).orient("bottom").ticks(6),
        yAxis = d3.svg.axis().scale(y).orient("left").ticks(6);


    var domainByField = {},
        fields = d3.keys(data[0]).filter(function(d) { return d !== "clx_cluster" && d!== 'clx_id'; }),
        n = fields.length;

    fields.forEach(function(field) {
        domainByField[field] = d3.extent(data, function(d) { return d[field]; });
    });

    xAxis.tickSize(size * n);
    yAxis.tickSize(-size * n);

    var brush = d3.svg.brush().x(x).y(y)
        .on("brushstart", brushstart)
        .on("brush", brushmove)
        .on("brushend", brushend);

    var svg = d3.select('#matrix-area')
        .append("svg")
            .attr("width", size * n + padding + 30)
            .attr("height", size * n + padding + 30)
            .attr('class', 'white-background scatterplot matrix')
        .append("g")
            .attr("transform", translate(padding, padding/2));


    svg.selectAll(".x.axis")
        .data(fields)
        .enter()
        .append("g")
            .attr("class", "x axis")
            .attr("transform", function(d, i) { return translate((n - i - 1) * size, 0); })
        .each(function(d) {
            x.domain(domainByField[d]);
            d3.select(this).call(xAxis);
        });

    svg.selectAll(".y.axis")
        .data(fields)
        .enter()
        .append("g")
            .attr("class", "y axis")
            .attr("transform", function(d, i) { return translate(0, i * size); })
        .each(function(d) {
            y.domain(domainByField[d]);
            d3.select(this).call(yAxis);
        });



    var cell = svg.selectAll(".cell")
        .data(cross(fields, fields))
        .enter()
        .append("g")
            .attr("class", "cell")
            .attr("transform", function(d) { return translate((n - d.i - 1) * size, d.j * size); })
      .each(plot);

    // Titles for the diagonal.
    cell.filter(function(d) { return d.i === d.j; })
        .append("text")
        .attr("x", padding)
        .attr("y", padding)
        .attr("dy", ".71em")
        .text(function(d) { return d.x; });
    cell.call(brush);



    function plot(p) {
        var cell = d3.select(this);

        x.domain(domainByField[p.x]);
        y.domain(domainByField[p.y]);

        cell.append("rect")
            .attr("class", "frame")
            .attr("x", padding / 2)
            .attr("y", padding / 2)
            .attr("width", size - padding)
            .attr("height", size - padding);

        cell.selectAll("circle")
            .data(data)
            .enter()
            .append("circle")
                .attr("cx", function(d) { return x(d[p.x]); })
                .attr("cy", function(d) { return y(d[p.y]); })
                .attr("r", 3)
                .attr('opacity', 0.5)
            .style("fill", function(d) { return window.d3Color(d['clx_cluster']); });
    }

    var brushCell;

    // Clear the previously-active brush, if any.
    function brushstart(p) {
        if (brushCell !== this) {
            d3.select(brushCell).call(brush.clear());
            x.domain(domainByField[p.x]);
            y.domain(domainByField[p.y]);
            brushCell = this;
        }
    }

    // Highlight the selected circles.
    function brushmove(p) {
        var e = brush.extent();
        svg.selectAll("circle")
            .classed("hidden", function(d) {
                return e[0][0] > d[p.x] || d[p.x] > e[1][0] ||
                    e[0][1] > d[p.y] || d[p.y] > e[1][1];
        });
    }

    // If the brush is empty, select all circles.
    function brushend() {
        if (brush.empty()) svg.selectAll(".hidden").classed("hidden", false);
    }
}