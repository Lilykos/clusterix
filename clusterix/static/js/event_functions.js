$(function() {
    $('#country-select').on('click', function () {
        var country = $('#country-input').val();

        $.ajax({
            url: '/cluster_country/' + country
        }).done(function (data) {
            add_treemap(data);
        })
    });

    $('#search-box').on('input', function () {
        var search_string = $('#search-box').val().toLowerCase();
        var cells = $('rect').toArray().filter(function (cell) {
            if (!cell.attributes.has_children) return cell;
        });

        if (search_string) {
            cells.forEach(function (cell) {
                var color = d3.scale.category10()(search_string);
                var cell_text = cell.attributes.name.textContent.toLowerCase();
                if (cell_text.indexOf(search_string) > -1) {
                    $(cell).attr('fill', color);
                } else {
                    $(cell).attr('fill', 'lightgrey');
                }
            });
        } else {
            cells.forEach(function (cell) {
                $(cell).attr('fill', 'lightgrey');
            });
        }
    });
});