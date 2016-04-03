var PreviewRenderer = (function() {
    var attr = {
        modalContent: '#data-modal-content',
        txtTemplate: '#txt-file-preview-template',
        csvTemplate: '#csv-file-preview-template'
    };

    return {

        /**
         * Parses the CSV file using Papaparse and renders the modal with the preview.
         */
        renderCsv: function (csvFile) {
            Papa.parse(csvFile, {
                dynamicTyping: true, preview: 100,
                complete: function (results) {
                    var headers = results.data.shift();
                    var delimiter = results.meta.delimiter;
                    var data = results.data;

                    Utils.compileTemplate(attr.csvTemplate, attr.modalContent, {headers: headers, data: data}, true);
                    Router.set('delimiter', delimiter);

                    // dimmer (modal) init
                    $('#data-preview').on('click', function() {
                        $('#preview-dimmer').modal('show');
                    });

                    /**
                     * Render the csv panel. We do this here because we need the headers (fields).
                     */
                    CsvFieldsInput.init(headers);
                }
            });
        },

        /**
        * Creates a new File Reader (for text files only), and parses the text.
        * Then renders the modal with the data preview.
        */
        renderTxt: function(txtFile) {
        var reader = new FileReader();
            reader.onload = function() {
                attr.fileTxt =  reader.result;
                Utils.compileTemplate(attr.txtTemplate, attr.modalContent, {data: attr.fileTxt}, true);
            };
            reader.readAsText(txtFile);

            // Hide the (possible) previous csv panel.
            CsvFieldsInput.hide();
        }
    }
})();