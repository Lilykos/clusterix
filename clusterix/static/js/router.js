var Router = (function() {
    var attr = {
        alertTemplate: '#alert-template',
        url: '/upload',
        upload: '#upload'
    };

    var dataFileInfo = {empty: true};

    var dataModel = {
        blockBy: '',
        delimiter: ',',
        /* Algorithms Representation:
           algorithms: ['K-Means', ...]
         */
        algorithms: [],
        /* Csv Fields Representation:
           csvFields: [{name: 'PassengerID', scale: 1}, ...]
         */
        csvFields: []
    };

    /**
     * Checks for validity, based on certain rules.
     * @returns {boolean}
     */
    function dataIsValid() {
        if (dataFileInfo.empty) {                           // Empty file
            console.log('Data file failed');
            return false;
        } else if (!dataModel.algorithms.length) {          // Empty algorithms array
            console.log('No algorithms found');
            return false;
        } else if (!dataModel.csvFields.length &&
                dataFileInfo.file.type === 'text/csv') {    // No csv fields sent
            console.log('Wrong csv fields.');
            return false;
        }

        return true;
    }

    /**
     * Uploads everything in FormData format.
     */
    function upload() {
        var data = new FormData();

        data.append('file', dataFileInfo.file);
        data.append('type', dataFileInfo.file.type);
        data.append('timestamp', dataFileInfo.timestamp);
        data.append('algorithms', dataModel.algorithms);
        data.append('csv_fields', JSON.stringify(dataModel.csvFields));
        data.append('block_by', dataModel.blockBy);
        data.append('delimiter', dataModel.delimiter);

        $.ajax({
            type: 'POST',
            url: attr.url,
            data: data,
            cache: false,
            contentType: false,
            processData: false,
            success: function(data){
                Renderer.render(data);
            }
        });
    }

    return {

        /**
         * Functionality:
         *      - Saves file/options.
         *      - Validates the data.
         *      - Uploads, and on success it renders the visualizations.
         * @constructor
         */
        init: function() {
            console.log('Router init');
            $(attr.upload).on('click', this.validateAndUpload);
        },

        /**
         * Saves the data file.
         * @param file
         */
        setFile: function(file) {
            dataFileInfo = {
                empty: false,
                file: file,
                fileName: file.name,
                timestamp: new Date().getTime()
            };
            console.log('-- Router received: file: ' + dataFileInfo.fileName);
        },

        /**
         * Sets specific options to the data model.
         * @param key
         * @param value
         */
        set: function(key, value) {
            dataModel[key] = value;
            console.log('-- Router received: ' + key + ': ' + dataModel[key]);
        },

        /**
         * Self explained. Also notifies Search in order to create index based on csv fields.
         */
        validateAndUpload: function() {
            if (dataIsValid()) upload();
            $(document).trigger('data-uploaded', {data: dataModel.csvFields}); // Search init basically
        },

        /**
         * Checks if the upload button exists, and makes it appear/disappear.
         */
        checkUploadButton: function() {
            if (!dataModel.algorithms.length) $(attr.upload).fadeOut(200);
            else $(attr.upload).fadeIn(200);
        },

        /**
         * Used for debug reasons, presents all the data that will be sent.
         * @returns {Object}
         */
        data: function() {
            return dataModel;
        }
    }
})();