var Router = (function() {
    var attr = {
        alertTemplate: '#alert-template',
        upload: '#upload',

        url: '/upload_and_cluster'
    };

    var newFile;

    var dataFileInfo = {
        empty: true,
        file: null,
        timestamp: ''
    };

    var dataModel = {

        // CSV-specific info
        csvType: {
            delimiter: ',',
            fieldsWithScaling: []
        },

        // Each algorithm need certain parameters provided here.
        algorithms: {
            algorithmsToUse: [],

            kmeans: {
                kNumber: 1
            },

            bcluster: {
                blockBy: '',
                distance: 'single',
                affinity: 'euclidean'
            },

            hcluster: {
                distance: 'single',
                affinity: 'euclidean',
                kNumber: 1
            }
        },

        // 3 vectorizer options: Count, Hashing, Tfidf
        vectorizer: 'count'
    };


    /**
     * Uploads everything in FormData format.
     */
    function upload() {
        var data = new FormData();
        data.append('data', JSON.stringify(dataModel));

        // If newFile == true, send the file
        // Else, do not send it and use the route that will get the data without preprocessing
        if (newFile) {
            data.append('file', dataFileInfo.file);
            data.append('type', dataFileInfo.file.type);
            data.append('timestamp', dataFileInfo.timestamp);

            newFile = false;
        }

        $.ajax({
            type: 'POST',
            url: attr.url,
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
         */
        data: function() { return dataModel; },

        /**
         * Self explained. Also notifies Search in order to create index based on csv fields.
         */
        validateAndUpload: function() { upload(); },

        /**
         * Checks if the upload button exists, and makes it appear/disappear.
         */
        checkUploadButton: function() {
            if (!dataModel.algorithms.algorithmsToUse.length) $(attr.upload).fadeOut(200);
            else $(attr.upload).fadeIn(200);
        }
    }
})();