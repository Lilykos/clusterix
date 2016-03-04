var CsvFieldsInput = (function() {
    var attr = {
        csvPanel: '#csv-fields-panel',
        selectID: '#multiple-fields-csv',
        scaleSelectors: '.scaling',
        blockBySelector: '#block-by-field',

        csvFieldsContainer: '#csv-fields-container',
        scaledFieldsContainer: '#scale-fields-container',
        blockByContainer: '#block-by-container',

        scaleFieldsTemplate: '#fields-to-scale-template',
        csvFieldsTemplate: '#fields-to-select-template',
        blockByTemplate: '#block-by-template',

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
        attr.blockBy = fields.length ? fields[0] : attr.fields[0];
    }

    /**
     * Render all the chosen fields, with their scaling.
     */
    function renderFieldsToScale() {
        Utils.compileTemplate(attr.scaleFieldsTemplate, attr.scaledFieldsContainer, { fields: attr.fieldsWithScaling });
        $(attr.scaleSelectors).on('change', updateFieldsWithScaling);

        Router.set('csvFields', attr.fieldsWithScaling);
    }

    /**
     * Every time an item is added/removed, it re-renders the panels.
     */
    function renderFieldsToChoose() {
        Utils.compileTemplate(attr.csvFieldsTemplate, attr.csvFieldsContainer, { fields: attr.fields });
        $(attr.selectID).dropdown({
            onChange: function(fields, item, selected) {
                saveValues(fields);
                renderBlockByField();
                renderFieldsToScale();
            }
        });
    }

    /**
     * Renders the block by field according to the user-chosen fields,
     * and sets the variable to the Router.
     */
    function renderBlockByField() {
        var fields = attr.fieldsWithScaling.map(function(f) { return f.name; });

        Utils.compileTemplate(attr.blockByTemplate, attr.blockByContainer, { fields: fields });
        Router.set('blockBy', attr.blockBy);

        $(attr.blockBySelector).dropdown({
            onChange: function(val, text, selected) {
                attr.blockBy = text;
                Router.set('blockBy', attr.blockBy);
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
            renderBlockByField();

            $(attr.csvPanel).fadeIn();
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