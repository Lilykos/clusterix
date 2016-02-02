var PreviewRenderer = (function() {
    var attr = {
        modalContent: '#data-modal-content',
        txtTemplate: '#txt-file-preview-template',
        csvTemplate: '#csv-file-preview-template'
    };

    function initPreview() {
         $('#data-preview').on('click', function() {
            $('#preview-dimmer').modal('show');
        });
    }

    return {

        /**
         * Parses the CSV file using Papaparse and renders the modal with the preview.
         */
        renderCsv: function (csvFile) {
            Papa.parse(csvFile, {
                dynamicTyping: true, preview: 25,
                complete: function (results) {
                    var headers = results.data.shift();
                    var delimiter = results.meta.delimiter;
                    var data = results.data;

                    Utils.compileTemplate(attr.csvTemplate, attr.modalContent, {headers: headers, data: data}, true);
                    Router.data().csvType.delimiter = delimiter;
                    initPreview();

                    // Render the csv panel. We do this here because we need the headers (fields).
                    CsvFieldsInput.init(headers);
                }
            });
        }
    }
})();