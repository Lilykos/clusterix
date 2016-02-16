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
        fieldsToScale: [],      // string array
        fieldsWithScaling: [],  // object array
        blockBy: ''
    };

    function updateFieldsWithScaling() {
        var name = $(this).attr('name');
            var scale = $(this).val();

            var field = attr.fieldsWithScaling.filter(function(field) {
                if (field.name == name) return field
            })[0];
            field.scale = scale;
            Router.set('csvFields', attr.fieldsWithScaling);
    }


    function renderFieldsToScale(newItem) {
        // Every time this happens we have a new item.
        // We need to check if we add or remove it.
        if (Utils.inArray(newItem, attr.fieldsToScale)) {
            attr.fieldsWithScaling.push({
                name: newItem,
                scale: 1
            });
        } else {
            attr.fieldsWithScaling = attr.fieldsWithScaling
                .filter(function (item) {
                    if (item.name !== newItem) return item;
                });
        }

        Utils.compileTemplate(attr.scaleFieldsTemplate, attr.scaledFieldsContainer, { fields: attr.fieldsWithScaling });
        Router.set('csvFields', attr.fieldsWithScaling);

        $(attr.scaleSelectors).on('change', updateFieldsWithScaling);
    }

    function renderBlockByField() {
        Utils.compileTemplate(attr.blockByTemplate, attr.blockByContainer, { fields: attr.fieldsToScale });

        attr.blockBy = attr.fieldsToScale[0];
        Router.set('blockBy', attr.blockBy);

        $(attr.blockBySelector).dropdown({
            onChange: function(val, text, selected) {
                attr.blockBy = text;
                Router.set('blockBy', attr.blockBy);
            }
        });
    }

    function renderFieldsToChoose() {
        Utils.compileTemplate(attr.csvFieldsTemplate, attr.csvFieldsContainer, { fields: attr.fields });
        $(attr.selectID).dropdown({
            onChange: function(val, text, selected) {
                attr.fieldsToScale = val;

                if (val.length !== 0) {
                    renderBlockByField();
                    renderFieldsToScale(text)
                } else {
                    renderInitialFieldsToScale();
                    renderInitialBlockByField();
                }

            }
        });
    }




    // HELPER FUNCTIONS HERE
    function saveDefaultValues(fields) {
        attr.fields = fields;
        attr.fieldsToScale = fields;
        attr.blockBy = fields[0];
    }

    function getAllFieldsWithScale_1() {
        return attr.fields.map(function(i) {
            return { name: i, scale: 1 };
        });
    }

    function renderInitialBlockByField() {
        Utils.compileTemplate(attr.blockByTemplate, attr.blockByContainer, { fields: attr.fields });
        Router.set('blockBy', attr.blockBy);

        $(attr.blockBySelector).dropdown({
            onChange: function(val, text, selected) {
                attr.blockBy = text;
                Router.set('blockBy', attr.blockBy);
            }
        });
    }

    function renderInitialFieldsToScale() {
        var fields = getAllFieldsWithScale_1();

        Utils.compileTemplate(attr.scaleFieldsTemplate, attr.scaledFieldsContainer, { fields: fields });
        Router.set('csvFields', fields);
    }


    return {
        init: function(headers) {
            saveDefaultValues(headers);

            renderFieldsToChoose();
            renderInitialFieldsToScale();
            renderInitialBlockByField();

            $(attr.csvPanel).fadeIn();
            console.log('Csv Fields Input init');
        },

        hide: function() {
            $(attr.csvPanel).fadeOut();
            attr = {};
        }
    }
})();