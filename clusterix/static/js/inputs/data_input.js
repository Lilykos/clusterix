var DataInput = (function() {
    var attr = {
        // Selectors
        dataInput: '#data-input',
        dataPreview: '#data-preview',
        modalInit: 'data-preview-modal',
        modalContent: '#data-modal-content',

        // Template Selectors
        txtTemplate: '#txt-file-preview-template',
        csvTemplate: '#csv-file-preview-template'
    };

    var fileInputConfig = {
        maxFileCount:1,
        allowedFileExtensions: ['txt', 'csv'],
        showPreview: false,
        showRemove: false,

        uploadClass: 'btn btn-default',
        uploadLabel: 'Preview',
        uploadIcon: '<span class="glyphicon glyphicon-eye-open"></span> ',
        layoutTemplates: {
            main1: "{preview}\n<div class=\'input-group {class}\'>\n" +
            "<div class=\'input-group-btn\'>\n{browse}\n" +
            "<span id='data-preview' data-toggle='modal' data-target='#data-preview-modal'>{upload}</span>\n" +
            "{remove}\n</div>\n{caption}\n</div>"
        }
    };

    /**
     * Initializes the preview button and the contents of the preview modal.
     * Depending on the input type, there are different rendering methods.
     */
    function initModalPreview() {
        switch (attr.fileType) {
            case 'text/plain':
                render_txt();
                break;
            case 'text/csv':
                render_csv();
                break;
        }
    }

    /**
     * Creates a new File Reader (for text files only), and parses the text.
     * Then renders the modal with the data preview.
     */
    function render_txt() {
        var reader = new FileReader();
        reader.onload = function() {
            attr.fileTxt =  reader.result;
            Utils.compileTemplate(attr.txtTemplate, attr.modalContent, {data: attr.fileTxt});
        };
        reader.readAsText(attr.file);

        // Hide the (possible) previous csv panel.
        CsvFieldsInput.hide();
    }

    /**
     * Parses the CSV file using Papaparse and renders the modal with the preview.
     */
    function render_csv() {

        Papa.parse(attr.file, { dynamicTyping: true, preview: 100,
            complete: function(results) {
                var headers = results.data.shift();
                var data = results.data;

                Utils.compileTemplate(attr.csvTemplate, attr.modalContent, {headers:headers, data:data});
                // Render the csv panel. We do this here because we need the headers (fields).
                CsvFieldsInput.init(headers);
            }
        });
    }


    return {
        /**
         * Functionality:
         *      - 1st step of the workflow. Creates the file input, checks for acceptable files.
         *      - Renders a preview of the file content, using modals.
         *      - Sends file to the router for keeping.
         *      - Calls the next parts of the workflow CSV Field Options (if csv) and Algorithm Input.
         * @constructor
         */
        init: function() {
            $(attr.dataInput)
                .fileinput(fileInputConfig)
                .on('change', function() {
                    // Checking for stuff
                    if (!this.files[0]) return;

                    // Save important file attributes
                    attr.file = this.files[0];
                    attr.fileName = attr.file.name;
                    attr.fileType = attr.file.type;
                    initModalPreview();

                    // Save the file (to be sent).
                    Router.setFile(attr.file);
                    AlgorithmInput.init();
                });

            console.log('Data Input init');
        }
    }
})();