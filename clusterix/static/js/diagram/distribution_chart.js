/**
 * Created by eamonnmaguire on 21/07/2016.
 */
var ClusterDistributionChart = (function () {

    var render_bar_graph = function (placement, data, options, tip) {

        var svg = d3.select(placement).append("svg").attr(options);

        svg.call(tip);

        var xScale, x_extent, bar_count, bar_width;

        if (typeof data[0].value === "string") {
            x_extent = d3.map(data, function (d) {
                return d.value;
            });

            x_extent = x_extent.keys();


            bar_count = x_extent.length;
            bar_width = Math.min(5, (options.width / bar_count));

            xScale = d3.scale.ordinal()
                .domain(x_extent).rangePoints([bar_width, options.width - bar_width]);
        } else {
            x_extent = d3.extent(data, function (d) {
                return d.value;
            });
            bar_count = x_extent[1] - x_extent[0];
            bar_width = Math.min(5, (options.width / bar_count));
            xScale = d3.scale.linear()
                .domain(x_extent).range([bar_width, options.width - bar_width]);
        }

        if (bar_width < 1) bar_width=1;


        var yScale = d3.scale.linear().domain([0, d3.max(data, function (d) {
            return d.count;
        })]).range([0, options.height]);

        var plot = svg.append('g');
        var rect = plot.selectAll('.rect').data(data).enter().append('rect');

        rect.attr('x', function (d) {
            return xScale(d.value) - (bar_width / 2);
        }).attr('y', function (d) {
            return options.height - yScale(d.count);
        }).attr('width', bar_width)
            .attr('height', function (d) {
                return yScale(d.count);
            })
            .style("fill", function (d) {
                return options.colors(d.cluster);
            })
            .on('mouseover', tip.show)
            .on('mouseout', tip.hide)
    };

    /**
     * dimensions  = {1: {key: [{},{}]}
     * @param dimensions
     * @returns {{}}
     */
    var process_dimensions = function (dimensions) {
        var _processed_dimensions = {};
        $.each(dimensions, function (cluster, cluster_values) {

            $.each(cluster_values, function (k, v) {
                if (!(k in _processed_dimensions)) {
                    _processed_dimensions[k] = [];
                }

                $.each(v, function (value, count) {
                    if(!isNaN(value)) value = +value;
                    _processed_dimensions[k].push({
                        'value': value,
                        'count': count,
                        'cluster': +cluster
                    });
                });
            });
        });

        return _processed_dimensions;
    };

    var process_data = function (data, cluster_mapping) {

        // for each key in the data, a new group will be created with
        // {value:'', count:0} dictionaries to show distributions
        // todo: add automated bin range detection
        var _dimensions = {};
        for (var item_id in data) {
            var _data_item = data[item_id].content[0];

            var cluster = +cluster_mapping[+item_id];

            if (!(cluster in _dimensions)) {
                _dimensions[cluster] = {};
            }

            for (var _key in _data_item) {
                if (!(_key in _dimensions[cluster])) {
                    _dimensions[cluster][_key] = {};
                }

                if (!(_data_item[_key] in _dimensions[cluster][_key])) {
                    _dimensions[cluster][_key][_data_item[_key]] = 0
                }
                _dimensions[cluster][_key][_data_item[_key]] += 1
            }
        }

        return process_dimensions(_dimensions);

    };

    return {

        init: function (data, cluster_mapping, cluster_colors) {

            var _processed_data = process_data(data, cluster_mapping);

            var tip = d3.tip().attr('class', 'd3-tip').html(function (d) {
                return '<p><strong>Cluster ' + d.cluster + '</strong><br/>' + d.value + ' (' + d.count + ')</p>';
            });

            var count = 0;
            for (var _dimension in _processed_data) {

                d3.select("#cluster-comparison")
                    .append("div").attr('class', 'col-md-4').append('div')
                    .attr('class', 'white-background border-white-round distribution-container')
                    .attr('id', 'plot-' + count)
                    .append("p").text(_dimension);

                render_bar_graph('#plot-' + count, _processed_data[_dimension], {
                    width: 150,
                    height: 100,
                    colors: cluster_colors
                }, tip);

                count++;
            }
        }
    }

})();