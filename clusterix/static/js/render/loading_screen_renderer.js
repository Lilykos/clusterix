var LoadingScreenRenderer = (function () {
    var loadingScreenIntervalID;
    var loadingScreenID = '#loading-screen-dimmer';

    return {

        initLoadingScreen: function() {
            $(loadingScreenID)
                .on('click', function(){ return false; })
                .dimmer('show');
            LoadingScreenRenderer.render("#clusterix_loader");

            //var message = '';
            //loadingScreenIntervalID = setInterval(function() {
            //    $.ajax({
            //        type: 'GET',
            //        url: '/update',
            //        success: function(msg) {
            //            if (msg !== message) {
            //                message = msg;
            //
            //                $('#loading-screen-msg').text(msg);
            //                console.log('Update: ' + msg);
            //            }
            //        }
            //    });
            //}, 1000);
        },

        removeLoadingScreen: function() {
            clearInterval(loadingScreenIntervalID);
            $(loadingScreenID).dimmer('hide');
            //$('#loading-screen-msg').text('Loading...');
        },

        render: function (placement) {
            var svg = d3.select(placement + " svg");
            var width = svg.attr('width'),
                height = svg.attr('height');

            var data = [];

            svg.selectAll("circle").each(function (d, i) {
                var circle_data = {
                    'or': d3.select(this).attr('r'),
                    'ocx': d3.select(this).attr('cx'),
                    'ocy': d3.select(this).attr('cy'),
                    'fill': d3.select(this).style('fill')
                };
                d3.select(this).remove();
                data.push(circle_data);
            });

            var circles = svg.selectAll("circle")
                .data(data)
                .enter()
                .append("circle")
                    .style('fill', '#9eacad')
                    .attr('cx', function (d, i) {
                        // we start the X positions either at the beginning of the canvas, or end.
                        var start_position = Math.round(Math.random()) == 0 ? 0 : width;
                        return start_position == 0 ? start_position - (20) : start_position + 20;
                    })
                    .attr('cy', function (d, i) { return Math.random() * 3000 % height; })
                    .attr('r', 0);

            circles.transition()
                .ease('linear')
                .duration(function (d, i) { return (Math.random() * i) * 200; })
                .delay(function (d, i) { return i * (Math.random() * 50); })
                .attr('cx', function (d) { return d.ocx; })
                .attr('cy', function (d) { return d.ocy; })
                .attr('r', function (d) { return d.or; })

                .style('opacity', 1)
                .each("end", function (d, i) {
                    d3.select(this)
                        .transition('elastic')
                        .duration(500)
                        .delay(function (d, i) { return i * (Math.random() * 400); })
                        .style("fill", d.fill);
                });
        }
    }
})
();