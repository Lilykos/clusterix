function Treemap() {
    var attr = {
        // Colors
        d3Color: d3.scale.category20(),
        defaultColor: '#95a5a6',
        stroke: '#fff',
        bgColor: '#ddd',

        // Treemap Data
        root: {},
        width: 0,
        height: 0
    };

    return {

        /**
         *Functionality
         *      - Initialize the mini-treemap, as well as render the actual representation.
         * @constructor
         * @param {Object} root A d3-compatible json, that contains the nodes/structure to create a treemap.
         * @param width
         * @param height
         * @param selector
         * @param id
         */
        init: function(root, width, height, selector, id) {
            attr.width = width;
            attr.height = height;
            attr.data = root;
            attr.id = 'treemap-' + id;
            attr.class = 'treemap';
            attr.nodeSelector = selector;

            $(selector).empty();

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
                    .style('stroke-width', 0.5)
                    .attr('class', function(d) { return d.id ? 'node-' + d.id : ''; })
                    .attr('fill', function(d) { return d.children ? null : attr.defaultColor; })
                    .attr('fillbackup', function(d) {
                        if (!d.children) {
                            d.fillbackup = attr.defaultColor;
                            return d.fillbackup;
                        }
                    });


            // D3-Tip
            //var tip = d3.tip().attr('class', 'd3-tip').html(function(d) {
            //    if (d !== undefined && d.content !== undefined) return Utils.renderContent(d.content);
            //});
            //
            //svg.call(tip)
            //    .on('mouseover', tip.show)
            //    .on('mouseout', tip.hide);

            console.log('Treemap init.');
        }
    };
}