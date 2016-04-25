function FlatTreemap() {
    var attr = {
        // Colors
        d3Color: d3.scale.category20(),
        defaultColor: '#95a5a6',
        stroke: '#fff',
        bgColor: '#ddd',

        // Treemap Data
        root: {},
        width: 0,
        height: 0
    };

    return {

        /**
         *Functionality
         *      - Initialize the mini-treemap, as well as render the actual representation.
         *      - Handle the mini-treemap click events (show the big treemap).
         * @constructor
         * @param {Object} root A d3-compatible json, that contains the nodes/structure to create a treemap.
         * @param width
         * @param height
         * @param selector
         * @param id
         */
        init: function(root, width, height, selector, id) {
            attr.width = width;
            attr.height = height;
            attr.data = root;
            attr.id = 'flat-treemap-' + id;
            attr.class = 'flat-treemap';
            attr.nodeSelector = selector;

            $(selector).empty();
            // TODO
        }
    };
}