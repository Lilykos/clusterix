function TreemapMini() {
    var attr = {
        // Colors
        d3Color: d3.scale.category20(),
        defaultColor: '#95a5a6',
        stroke: '#fff',
        bgColor: '#ddd'
    };

    return {

        /**
         * Treemap mini.
         * @param root
         * @param width
         * @param height
         * @param selector
         * @param id
         */
        init: function(root, width, height, selector, id) {
            attr.data = root;
            attr.width = width;
            attr.height = height;
            attr.id = 'treemap-mini-' + id;
            attr.class = 'treemap-mini';
            attr.nodeSelector = selector + ' rect';

            var treemap = d3.layout.treemap()
                .size([width, height])
                .nodes(root);

            var svg = d3.select(selector)
                .append('svg')
                    .attr('width', width)
                    .attr('height', height)
                    .attr('id', attr.id)
                    .attr('class', attr.class);

            svg.selectAll(attr.nodeSelector)
                .data(treemap)
                .enter()
                .append('rect')
                    .attr('x', function (d) { return d.x; })
                    .attr('y', function (d) { return d.y; })
                    .attr('width', function (d) { return d.dx; })
                    .attr('height', function (d) { return d.dy; })
                    .attr('stroke', attr.stroke)
                    .style('stroke-width', 0.2)
                    .attr('class', function(d) { return d.id ? 'node-' + d.id : ''; })
                    .attr('fill', function(d) { return d.children ? null : attr.d3Color(d.parent.name); });

            console.log('Treemap-mini init.');
        }
    };
}