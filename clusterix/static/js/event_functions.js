$(function() {
    $('#country-select').on('click', function () {
        var country = $('#country-input').val();
        $.ajax({
            url: '/cluster_country/' + country
        })
        .done(function (data) {
            add_treemap_mini(data.children[0], 260, 195, '#treemap-mini');
            add_treemap(data.children[0], 900, 675, '#treemap');
        });
    });

    //$('#all-countries').on('click', function () {
    //    $.ajax({
    //        url: '/cluster_country/all'
    //    })
    //    .done(function (data) {
    //        //
    //    });
    //});


    $('#search-box').on('input', function () {
        var searchString = $('#search-box').val().toLowerCase();
        var cells = $('#treemap rect').toArray().filter(function (cell) {
            if (!cell.attributes.hasChildren)
                return cell;
        });

        if (searchString) {
            cells.forEach(function (cell) {
                var cellText = cell.attributes.name.textContent.toLowerCase();
                if (cellText.indexOf(searchString) > -1)
                    $(cell).attr('fill', '#34495e'); // exists
                else
                    $(cell).attr('fill', 'lightgrey');
                    //$(cell).attr('fill', cell.attributes.fillBackup.textContent); // does not exist
            });
        } else { // empty input string
            cells.forEach(function (cell) {
                $(cell).attr('fill', 'lightgrey');
                //$(cell).attr('fill', cell.attributes.fillBackup.textContent);
            });
        }

    });
});