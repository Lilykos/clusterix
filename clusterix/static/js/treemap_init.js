function add_treemap(root, width, height, treemapID) {
    var color = d3.scale.category10(),
        defaultColor = 'lightgrey',
        x = d3.scale.linear()
            .range([0, width]),
        y = d3.scale.linear()
            .range([0, height]);


    // Treemap and Nodes Init
    var treemap = d3.layout.treemap()
        .size([width, height])
        .nodes(root);

    var tip = d3.tip().attr('class', 'd3-tip')
            .html(function(d) { return "<strong>" + d.name + "</strong>"; });


    // Canvas and Cells
    var svg = d3.select(treemapID)
        .append('svg')
            .attr('width', width)
            .attr('height', height)
            .attr('background', '#ddd')
        .call(tip);

    var cells = svg.selectAll('g')
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
            .attr('stroke', '#fff')
            .attr('fill', defaultColor/*defaultColor */ /*function(d) { return d.children ? null : color(d.parent.name); } */)
            //.attr('fillBackup', /*defaultColor */ function(d) { return d.children ? null : color(d.parent.name); })
            .attr('name', function(d) { return d.children ? null : d.name; })
            .attr('hasChildren', function(d) { return d.children; })
            .on('mouseover', tip.show)
            .on('mouseout', tip.hide);
}

function add_treemap_mini(root, width, height, treemapID) {
    var color = d3.scale.category10(),
        x = d3.scale.linear()
            .range([0, width]),
        y = d3.scale.linear()
            .range([0, height]);


    // Treemap and Nodes Init
    var treemap = d3.layout.treemap()
        .size([width, height])
        .nodes(root);

    // Canvas and Cells
    var svg = d3.select(treemapID)
        .append('svg')
            .attr('width', width)
            .attr('height', height)
            .attr('background', '#ddd');

    var cells = svg.selectAll('g')
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
            .attr('stroke', '#fff')
            .attr('fill', function(d) { return d.children ? null : color(d.parent.name); });

    svg.attr('class', 'mini-treemap');
}