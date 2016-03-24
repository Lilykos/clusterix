var Router = (function() {
    var attr = {
        alertTemplate: '#alert-template',
        upload: '#upload',

        urlUploadFile: '/upload',
        urlUploadDataOnly: '/upload_data'
    };

    var dataModel = {
        blockBy: '',
        delimiter: ',',

        /* 3 vectorizer options:
           Count, Hashing, Tfidf
         */
        vectorizer: 'count',

        /* Number of Ks for K-Means Clustering
         */
        kNumber: 1,

        /* Block Clustering distance method
         */
        bclusterDistance: 'single',

        /* Affinity distance methods (pairwise)
         */
        affinity: 'euclidean',

        /* Algorithms Representation:
           algorithms: ['K-Means', ...]
         */
        algorithms: [],

        /* Csv Fields Representation:
           csvFields: [{name: 'PassengerID', scale: 1}, ...]
         */
        csvFields: []
    };

    var newFile;
    var dataFileInfo = {empty: true};

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

        data.append('algorithms', dataModel.algorithms);
        data.append('vectorizer', dataModel.vectorizer);
        data.append('k_num', dataModel.kNumber);
        data.append('bcluster_distance', dataModel.bclusterDistance);
        data.append('affinity', dataModel.affinity);

        data.append('csv_fields', JSON.stringify(dataModel.csvFields));
        data.append('block_by', dataModel.blockBy);
        data.append('delimiter', dataModel.delimiter);

        // If newFile == true, send the file
        // Else, do not send it and use the route that will
        // get the data without preprocessing
        var url;
        if (newFile) {
            data.append('file', dataFileInfo.file);
            data.append('type', dataFileInfo.file.type);
            data.append('timestamp', dataFileInfo.timestamp);

            url = attr.urlUploadFile;
            newFile = false;
        } else {
            url = attr.urlUploadDataOnly;
        }

        $.ajax({
            type: 'POST',
            url: url,
            data: data,
            cache: false,
            contentType: false,
            processData: false,
            success: function(data){
                Renderer.render(data);
                LoadingScreenRenderer.removeLoadingScreen();
            }
        });
        LoadingScreenRenderer.initLoadingScreen();
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

            // We set the newFile variable. If true, we upload the file,
            // else we upload just the data and use the previously created
            // json file to produce the results.
            newFile = true;
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