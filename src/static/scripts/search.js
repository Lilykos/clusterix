function initSearch() {
    $('#search').on('keypress', function (e) {
        if(e.which === 13){
            e.preventDefault();
            var query = $(this).val();

            if (query.length) {
                $('body').trigger('search-request', [query]);
            } else {
                showDefaultPlot();
            }
        }
   });
}

function showSearchResults(ids) {
    if (!ids.length) {
        d3.selectAll('.scatterplot circle')
            .attr('fill', '#7f8c8d')
            .attr('opacity', 0.5)
            .attr('r', 3);
    } else {
        d3.selectAll('.scatterplot circle')
            .attr('fill', function(d) {
                return ids.contains(d['clx_id']) ? window.d3Color(d['clx_cluster']) : '#7f8c8d';
            })
            .attr('opacity', 0.7)
            .attr('r', function(d) {
                return ids.contains(d['clx_id']) ? 4 : 1;
            });
    }
}

function showDefaultPlot() {
    d3.selectAll('.scatterplot circle')
        .attr('fill', function(d) { return window.d3Color(d['clx_cluster']); })
        .attr('opacity', 0.5)
        .attr('r', 3);
}