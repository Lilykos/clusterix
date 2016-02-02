var DataInput = (function() {
    var attr = {};
    var dataInput = '#data-input';

    var fileInputConfig = {
        maxFileCount:1,
        allowedFileExtensions: ['csv'],
        showPreview: false,
        showRemove: false,

        uploadClass: 'btn btn-default',
        uploadLabel: 'Preview',
        uploadIcon: '<span class="glyphicon glyphicon-eye-open"></span> ',
        layoutTemplates: {
            main1: "{preview}<div class='input-group {class}'>" +
            "<div class='input-group-btn'><span class='light-blue'>{browse}</span>" +
            "<span id='data-preview'>{upload}</span>" + // data-toggle='modal' data-target='#data-preview-modal'
            "{remove}</div>{caption}</div>"
        }
    };

    /**
     * Initializes the preview button and the contents of the preview modal.
     * Depending on the input type, there are different rendering methods.
     */
    function initModalPreview() {
        switch (attr.fileType) {
            case 'text/csv':
                PreviewRenderer.renderCsv(attr.file);
                break;
        }
    }

    return {

        /**
         * Functionality:
         *      - 1st step of the workflow. Creates the file input, checks for acceptable files.
         *      - Renders a preview of the file content, by calling the PreviewRenderer.
         *      - Sends file to the router for keeping.
         *      - Calls the next parts of the workflow CSV Field Options (if csv) and Algorithm Input.
         * @constructor
         */
        init: function() {
            $(dataInput)
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

            // Panel hide/show
            Utils.attachSliderToPanel('#data-input-hide', '#data-input-body', 150);
            console.log('Data Input init');
        }
    }
})();