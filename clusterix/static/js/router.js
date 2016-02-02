var Router = (function() {
    var attr = {
        alertTemplate: '#alert-template',
        url: '/upload',
        upload: '#upload'
    };

    var dataFileInfo = {empty: true};

    var dataModel = {
        blockBy: '',
        /* Algorithms Representation:
           algorithms: ['K-Means', ...]
         */
        algorithms: [],
        /* Csv Fields Representation:
           csvFields: [{name: 'PassengerID', scale: 1}, ...]
         */
        csvFields: []
    };

    function dataIsValid() {
        if (dataFileInfo.empty) {                           // Empty file
            console.log('Data file failed');
            return false;
        } else if (Utils.isEmpty(dataModel.algorithms)) {   // Empty algorithms array
            console.log('No algorithms found');
            return false;
        } else if (Utils.isEmpty(dataModel.csvFields) &&
                dataFileInfo.file.type === 'text/csv') {    // No csv fields sent
            console.log('Wrong csv fields.');
            return false;
        }

        return true;
    }

    function upload() {
        var data = new FormData();

        data.append('file', dataFileInfo.file);
        data.append('type', dataFileInfo.file.type);
        data.append('timestamp', dataFileInfo.timestamp);
        data.append('algorithms', dataModel.algorithms);
        data.append('csv_fields', JSON.stringify(dataModel.csvFields));
        data.append('block_by', dataModel.blockBy);

        $.ajax({
            type: 'POST',
            url: attr.url,
            data: data,
            cache: false,
            contentType: false,
            processData: false,
            success: function(data){
                new Treemap().init(data,
                {width: 900, height: 675}, // Treemap size
                {width: 260, height: 195}  // Mini map size
            );
            }
        });
    }

    return {

        data: function() {
            return dataModel;
        },

        init: function() {
            console.log('Router init');
            $(attr.upload).on('click', this.validateAndUpload);
        },

        setFile: function(file) {
            dataFileInfo = {
                empty: false,
                file: file,
                fileName: file.name,
                timestamp: new Date().getTime()
            };
            console.log('-- Router received: file: ' + dataFileInfo.fileName);
        },

        set: function(key, value) {
            dataModel[key] = value;
            console.log('-- Router received: ' + key + ': ' + dataModel[key]);
        },

        validateAndUpload: function() {
            if (dataIsValid()) upload();
        },

        checkUploadButton: function() {
            if (Utils.isEmpty(dataModel.algorithms)) $(attr.upload).fadeOut(200);
            else $(attr.upload).fadeIn(200);
        }
    }
})();