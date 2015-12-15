function add_treemap(data) {
    var root = data.children[0],
        node = root,
        color = d3.scale.category20(),
        defaultColor = 'lightgrey',

        width = 1024,
        height = 768,

        x = d3.scale.linear()
            .domain([0, width])
            .range([0, width]),
        y = d3.scale.linear()
            .domain([0, height])
            .range([0, height]);


    // Treemap and Nodes Init
    var treemap = d3.layout.treemap()
        .size([width, height])
        .nodes(root);


    // Canvas and Cells
    var canvas = d3
        .select('#treemap')
            .style("width", width + "px")
            .style("height", height + "px")
        .append('svg')
            .attr('width', width)
            .attr('height', height)
            .attr('background', '#ddd');

    var cells = canvas.selectAll('g')
        .data(treemap)
        .enter()
        .append('svg:g')
            .attr('class', 'cell');


    cells
        .append('svg:rect')
            .attr('x', function (d) { return d.x; })
            .attr('y', function (d) { return d.y; })
            .attr('width', function (d) { return d.dx; })
            .attr('height', function (d) { return d.dy; })
            .attr('fill', /*defaultColor */ function(d) { return d.children ? null : color(d.parent.name); })
            .attr('fillBackup', /*defaultColor */ function(d) { return d.children ? null : color(d.parent.name); })
            .attr('name', function(d) { return d.children ? null : d.name; })
            .attr('hasChildren', function(d) { return d.children; })
        .append('svg:title')
            .text(function(d) { return d.children ? null : d.name; });
}