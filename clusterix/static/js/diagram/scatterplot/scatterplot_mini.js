function ScatterplotMini() {
    var attr = {
        d3Color: d3.scale.category10(),
        darkgrey: '#7f8c8d'
    };

    var margins = {
        left: 40,
        right: 30,
        top: 30,
        bottom: 30
    };

    function getSVGClasses(d) {
        return 'white-background ' + attr.class;
    }

    function getXScale() {
        return d3.scale.linear().domain(d3.extent(attr.data, function (d) { return d.x; }))
            .range([0, attr.width - margins.left - margins.right]);
    }

    function getYScale() {
        return d3.scale.linear().domain(d3.extent(attr.data, function (d) { return d.y; }))
            .range([attr.height - margins.top - margins.bottom, 0]);
    }

    function translate(a, b) {
        return "translate(" + a + "," + b + ")"
    }

    return {

        /**
         *
         * @param root
         * @param width
         * @param height
         * @param selector
         * @param id
         */
        init: function(root, width, height, selector, id) {
            attr.width = width;
            attr.height = height;
            attr.data = root.nodes.filter(function(d) { return !d.isCentroid }); // NO centroids needed
            attr.kNumber = root.k_num;
            attr.id = 'scatterplot-mini-' + id;
            attr.class = 'scatterplot-mini';
            attr.nodeSelector = selector + ' circle';

            var xScale = getXScale();
            var yScale = getYScale();

            // SVG Init
            var svg = d3.select(selector)
                .append("svg")
                    .attr("width", width)
                    .attr("height", height)
                    .attr('id', attr.id)
                    .attr('class', getSVGClasses)
                .append("g")
                    .attr("transform", translate(margins.left, margins.top));

            svg.append('rect')
                .attr('width', width)
                .attr('height', height)
                .attr('fill', 'rgba(1,1,1,0)');

            // Node init (minimal, just to show the pattern in small scale)
            svg.selectAll()
                .data(attr.data)
                .enter()
                .append("circle")
                    .attr("r", 0.5)
                    .attr("cx", function(d) { return xScale(d.x); })
                    .attr("cy", function(d) { return yScale(d.y); })
                    .attr("class", function (d) { return 'node-' + d.content.id;})
                    .attr("fill", function (d) { return attr.d3Color(d.cluster); })
                    .attr('fillbackup', function (d) {
                        d.fillbackup = attr.d3Color(d.cluster);
                        return d.fillbackup;
                    });

            console.log('Scatterplot mini init.')
        }
    }
}