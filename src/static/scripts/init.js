$(function() {
    window.d3Color= d3.scale.category20();

    // Data input
    $('#data-input')
        .fileinput({
            maxFileCount:1, allowedFileExtensions: ['csv'], showPreview: false, showRemove: false,
            uploadClass: 'btn btn-default', uploadLabel: 'Preview',
            uploadIcon: '<span class="glyphicon glyphicon-eye-open"></span> ',
            layoutTemplates: {
                main1: "{preview}<div class='input-group {class}'>" +
                "<div class='input-group-btn'><span class='light-blue'>{browse}</span>" +
                "<span id='data-preview'>{upload}</span>{remove}</div>{caption}</div>"
            }
        })
        .on('change', function() {
            // Checking for stuff and create the data file
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
});


function initFields(data) {
    // FIELDS
    $('#fields-panel').html(data['fields']).fadeIn();
    $('#multiple-fields-csv').dropdown();
    $('#decomposition-selection').dropdown();
    $('#decomposition-metric-selection').dropdown();

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

    // UPLOAD BUTTON
    $('#get-results').fadeIn(200);
    $('#projection-results').fadeIn(200);
}