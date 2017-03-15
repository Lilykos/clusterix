/**
 * Brushing functions for scatterplot.
 */
function initBrush(xScale, yScale, svg) {
    var brushSelectedIDs;
    var ext_coords;

    var brushStart = function() { brushSelectedIDs = new Set(); };

    var brushAction = function() {
        var extent = brush.extent();
        d3.selectAll('.scatterplot circle').each(function (d) {
            ext_coords = {
                x1: xScale(extent[0][0]), x2: xScale(extent[1][0]),
                y1: yScale(extent[0][1]), y2: yScale(extent[1][1])
            };

            var selected =
                (xScale(d.x) > ext_coords.x1 && xScale(d.x) < ext_coords.x2) &&
                (yScale(d.y) < ext_coords.y1 && yScale(d.y) > ext_coords.y2);

            if (selected) brushSelectedIDs.add(d);
        });
    };

    var brushEnd = function() {
        if (brushSelectedIDs.size) {
            var selectedItemsList = Array.from(brushSelectedIDs);
            var ids = new Set(selectedItemsList.map(function (d) { return d['clx_cluster']; }));

            drawBrushArea(selectedItemsList);
            $('body').trigger('tfidf-request', [ids]);
            // new ClusterDetailZone().init(selectedItemsList, '#selections-area ul', brushID, window.d3Color);
        }
    };

    var brush = d3.svg.brush()
        .x(xScale).y(yScale)
        .on("brushstart", brushStart)
        .on("brush", brushAction)
        .on("brushend", brushEnd);

    svg.append("g")
        .attr("class", "brush")
        .call(brush);
}