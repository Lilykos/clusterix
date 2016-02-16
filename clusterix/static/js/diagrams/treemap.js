function Treemap() {
    var attr = {
        // Colors
        d3Color: d3.scale.category10(),
        defaultColor: '#95a5a6',
        stroke: '#fff',
        bgColor: '#ddd',

        // Selectors
        treemapID: '#treemap',
        miniID: '#treemap-mini',

        // Treemap Data
        root: {},
        width: 0,
        height: 0
    };


    /**
     * It returns an object containing the basic initialized elements of a treemap,
     * the svg element(canvas) that the treemap will be drawn on, and the cells containing
     * the d3-nodes.
     * @param root The treemap d3 nodes.
     * @param width The width of the map on the screen.
     * @param height The height of the map on the screen.
     * @param treemapID The selector that will be used for this treemap.
     * @returns {{svg: *, cells: *}}
     */
    function getTreemapElements(root, width, height, treemapID) {
        var treemap = d3.layout.treemap()
            .size([width, height])
            .nodes(root);

        var svg = d3.select(treemapID)
            .append('svg')
                .attr('width', width)
                .attr('height', height)
                .attr('background', attr.background);

        return {
            svg: svg,
            cells: svg.selectAll('g')
                .data(treemap).enter()
                .append('svg:g').attr('class', 'cell')
        };
    }


    /**
     * Renders the treemap with the provided attributes.
     */
    function renderTreemap() {
        $(attr.treemapID).empty();

        var elements = getTreemapElements(attr.root, attr.width, attr.height, attr.treemapID);
        var tip = d3.tip().attr('class', 'd3-tip').html(function(d) { return d.name; });

        elements.svg.call(tip);
        elements.cells.append('svg:rect')
            .attr('x', function (d) { return d.x; })
            .attr('y', function (d) { return d.y; })
            .attr('width', function (d) { return d.dx; })
            .attr('height', function (d) { return d.dy; })
            .attr('stroke', attr.stroke)
            .attr('fill', attr.defaultColor)
            .attr('fillBackup', attr.defaultColor)
            .attr('name', function(d) { return d.children ? null : d.name; })
            .on('mouseover', tip.show)
            .on('mouseout', tip.hide);
    }


    return {
        /**
         *Functionality
         *      - Initialize the mini-treemap, as well as render the actual representation.
         *      - Handle the mini-treemap click events (show the big treemap).
         * @constructor
         * @param {Object} root A d3-compatible json, that contains the nodes/structure to create a treemap.
         * @param {{width:int, height:int}} treemapAttrs
         * @param {{width:int, height:int}} miniAttrs
         */
        init: function(root, treemapAttrs, miniAttrs) {

            // Save treemap attrs, they will be used to re-render the treemap
            // if we have multiple of them.
            attr.root = root;
            attr.width = treemapAttrs.width;
            attr.height = treemapAttrs.height;

            var elements = getTreemapElements(root, miniAttrs.width, miniAttrs.height, attr.miniID);
            elements.svg.attr('class', 'mini-treemap');
            elements.cells.append('svg:rect')
                .attr('x', function (d) { return d.x; })
                .attr('y', function (d) { return d.y; })
                .attr('width', function (d) { return d.dx; })
                .attr('height', function (d) { return d.dy; })
                .attr('stroke', attr.stroke)
                .attr('fill', function(d) { return d.children ? null : attr.d3Color(d.parent.name); })
                .attr('fillBackup', function(d) { return d.children ? null : attr.d3Color(d.parent.name); })
                .attr('name', function(d) { return d.children ? null : d.name; });

            renderTreemap();
            elements.svg.on('click', function() {
                renderTreemap();
            });

            console.log('Treemap init.');
        }
    };
}