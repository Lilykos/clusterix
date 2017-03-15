$(function() {
    window.d3Color= d3.scale.category20();

    // Data input
    $('#data-input')
        .fileinput(fileInputConfig())
        .on('change', function() {
            if (!this.files[0]) return;

            var formData = new FormData();
            formData.append('file', this.files[0]);

            // Load the file and render the input boxes.
            $.ajax({type: 'POST', url: '/load_file', data: formData,
                cache: false, contentType: false, processData: false,
                success: function(data){
                    initFields(data);
                    Router.init();
                }
            });
        });
    initSearch();
});


function initFields(data) {
    // Init all the needed elements for the processing space

    // FIELDS
    $('#fields-panel').html(data['fields']).fadeIn();
    $('#multiple-fields-csv').dropdown();
    $('#decomposition-selection').dropdown();
    $('#decomposition-metric-selection').dropdown();
    $('#scatterplot-matrix-fields').dropdown();

    // ALGORITHMS
    $('#algorithms-panel').html(data['algorithms']).fadeIn();
    $('#algorithms-selection').dropdown({
        onChange: function(val) {
            $.ajax({type: 'POST', url: '/algorithm_options', data: {'algorithm': val}, dataType:'text',
                success: function (data) { $('#algorithm-options').html(data); }
            });
        }
    });

    // TEXT
    if (data['hasText']) {
        $('#text-options-panel').html(data['textOptions']).fadeIn();
        $('#vectorizer-selection').dropdown();
        $('#norm-selection').dropdown();
        $('.checkbox').checkbox();
    }
}