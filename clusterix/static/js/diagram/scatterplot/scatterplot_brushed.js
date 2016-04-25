function ScatterplotBrushed() {
    var attr = {
        grey: '#7f8c8d',
        url: '/tfidf'
    };

    var margins = {
        left: 40,
        right: 30,
        top: 30,
        bottom: 30
    };

    /**
     * Axis/scaling/translation/svg functions
     */
    function getXScale() {
        return d3.scale.linear().domain(d3.extent(attr.data, function (d) { return +d.x; }))
            .range([0, attr.width - margins.left - margins.right]);
    }

    function getYScale() {
        return d3.scale.linear().domain(d3.extent(attr.data, function (d) { return +d.y; }))
            .range([attr.height - margins.top - margins.bottom, 0]);
    }

    function translate(a, b) { return "translate(" + a + "," + b + ")" }

    /**
     * Metrics
     */
    function renderTFIDF(clusteredTFIDFs) {
        var clustersWithColors = [];
        for (var cluster in clusteredTFIDFs) {
            clustersWithColors.push({
                cluster: cluster,
                color: attr.d3Color(cluster)
            });
        }
        TermFrequencyChart.createTFIDFChart(clustersWithColors, clusteredTFIDFs)
    }

    function getMetrics(rootData) {
        var clusteredIDs = {};
        rootData.forEach(function(d) { clusteredIDs[d.id] = d.cluster; });

        var data = new FormData();
        data.append('ids', JSON.stringify(clusteredIDs));

        $.ajax({
            type: 'POST',
            url: attr.url,
            data: data,
            cache: false,
            contentType: false,
            processData: false,
            success: function(data){
                var clusteredTFIDFs = data['tfidf_metrics'];

                console.log(clusteredTFIDFs);
                renderTFIDF(clusteredTFIDFs)
            }
        });
    }

    function get_content(d) {
        var data = new FormData();
        data.append('ids', JSON.stringify(
            attr.data.map(function(d) { return d.id; })
        ));
        
        $.ajax({
            type: 'POST',
            url: '/content',
            data: data,
            cache: false,
            async: false,
            contentType: false,
            processData: false
        })
        .success(function(data) {
            attr.content = data['content']
        });
    }

    return {

        init: function(rootData, width, height, selector, id, color, borderColor) {
            attr.width = width;
            attr.height = height;
            attr.data = rootData;
            attr.d3Color = color;
            attr.nodeSelector = '.scatterplot-selection circle';
            
            get_content();

            // Axis init
            var xScale = getXScale();
            var yScale = getYScale();

            var tip = d3.tip()
                .attr("class", "d3-tip")
                .html(function(d) {
                    return attr.content[d.id].text;
                });

            var zoom = d3.behavior.zoom()
                .x(xScale)
                .y(yScale)
                .scaleExtent([-5, 20])
                .on("zoom", function() {
                    svg.selectAll(attr.nodeSelector).attr('transform', function(d) {
                        return translate(xScale(d.x), yScale(d.y));
                    });
                });

            // SVG init
            var listItem = d3.select(selector).append('li')
                .attr('id', 'scatterplot-selection-' + id);

            var svg = listItem.append("svg")
                .attr("width", width)
                .attr("height", height)
                .attr('class', 'white-background scatterplot-selection')
                .attr('border', 3)
                .attr('margin', '1%');

            svg.append('rect')
                .attr('width', width)
                .attr('height', height)
                .attr("x", 0)
       			.attr("y", 0)
                .style("stroke", borderColor)
       			.style("stroke-width", 3)
                .attr('fill', 'rgba(1,1,1,0)')
                .call(zoom)
                .call(tip);

            // Node init
            svg.selectAll(attr.nodeSelector)
                .data(attr.data)
                .enter()
                .append("circle")
                    .attr("r", 4)
                    .attr('class', function(d) { return 'node node-' + d.id; })
                    .attr("fill", function (d) { return d.fillbackup; })
                    .attr('transform', function(d) {
                        return translate(xScale(d.x), yScale(d.y));
                    })
                    .on("mouseover", tip.show)
                    .on("mouseout", tip.hide);

            getMetrics(rootData);
        }
    };
}