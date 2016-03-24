var CsvFieldsInput = (function() {
    var attr = {
        csvPanel: '#csv-fields-panel',
        selectID: '#multiple-fields-csv',
        scaleSelectors: '.scaling',

        csvFieldsContainer: '#csv-fields-container',
        scaledFieldsContainer: '#scale-fields-container',

        scaleFieldsTemplate: '#fields-to-scale-template',
        csvFieldsTemplate: '#fields-to-select-template',

        fields: [],             // string array
        fieldsWithScaling: [],  // object array
        blockBy: ''
    };

    /**
     * Update the scaling and notify the Router.
     */
    function updateFieldsWithScaling() {
        var name = $(this).attr('name');
        var scale = $(this).val();

        var field = attr.fieldsWithScaling.filter(function(field) {
            if (field.name == name) return field
        })[0];

        field.scale = scale;
        Router.set('csvFields', attr.fieldsWithScaling);
    }

    /**
     * Gets the default values or the new values from the field selector,
     * and sets them on the appropriate variables OR the default ones.
     * @param fields
     */
    function saveValues(fields) {
        attr.fieldsWithScaling = fields.length
            ? fields.map(function(f) { return {name: f, scale: 1} })
            : attr.fields.map(function(f) { return {name: f, scale: 1} });

        // Everytime the values change, we want to change the block-by field
        var fieldsToSend = fields.length ? fields : attr.fields;
        $(document).trigger('csv-fields-change', {data: fieldsToSend});
    }

    /**
     * Render all the chosen fields, with their scaling.
     */
    function renderFieldsToScale() {
        Utils.compileTemplate(attr.scaleFieldsTemplate, attr.scaledFieldsContainer, { fields: attr.fieldsWithScaling }, true);
        $(attr.scaleSelectors).on('change', updateFieldsWithScaling);

        Router.set('csvFields', attr.fieldsWithScaling);
    }

    /**
     * Every time an item is added/removed, it re-renders the panels.
     */
    function renderFieldsToChoose() {
        Utils.compileTemplate(attr.csvFieldsTemplate, attr.csvFieldsContainer, { fields: attr.fields }, true);
        $(attr.selectID).dropdown({
            onChange: function(fields, item, selected) {
                saveValues(fields);
                renderFieldsToScale();
            }
        });
    }

    return {

        /**
         * Functionality:
         *      - Initializes the needed panels using the headers.
         *      - Re-renders the panels when a field is selected/disselected.
         *      - Notifies the Router.
         * @constructor
         * @param headers
         */
        init: function(headers) {
            attr.fields = headers;
            saveValues(headers);

            renderFieldsToChoose();
            renderFieldsToScale();

            $(attr.csvPanel).fadeIn();

            // Panel hide/show
            Utils.attachSliderToPanel('#csv-fields-hide', '#csv-fields-body', 150);
            console.log('Csv Fields Input init');
        },

        /**
         * Hide the csv fields panel.
         */
        hide: function() {
            $(attr.csvPanel).fadeOut();
            attr = {};
        }
    }
})();