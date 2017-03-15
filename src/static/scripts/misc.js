/**
 * Router functions
 */
function ajaxConfig(route, data) {
    return { type: 'POST', url: route, data: data, cache: false, contentType: false, processData: false,
        success: function(data){
            $('#brush-results').addClass('no-display');
            $('#scatterplot-matrix').addClass('no-display');
            scatterplot(data['results']);
            removeLoadingScreen();
        }
    }
}

function ajaxConfigScatter(route, data) {
    return { type: 'POST', url: route, data: data, cache: false, contentType: false, processData: false,
        success: function(data){
            $('#scatterplot-matrix').removeClass('no-display');
            scatterplotMatrix(data['results']);
            removeLoadingScreen();
        }
    }
}


/**
 * Misc
 */
Array.prototype.contains = function(v) {
    for(var i = 0; i < this.length; i++) {
        if(this[i] === v) return true;
    }
    return false;
};

function cross(a, b) {
  var c = [],
      n = a.length,
      m = b.length,
      i, j;
  for (i = -1; ++i < n;)
      for (j = -1; ++j < m;)
          c.push({
              x: a[i],
              i: i,
              y: b[j],
              j: j}
          );
  return c;
}


 /**
 * Axis/scaling/translation/svg functions
 */
function getXScale(data, w, m) {
    return d3.scale.linear().domain(d3.extent(data, function (d) { return +d.x; }))
        .range([0, w - m.left - m.right]);
}

function getYScale(data, h, m) {
    return d3.scale.linear().domain(d3.extent(data, function (d) { return +d.y; }))
        .range([h - m.top - m.bottom, 0]);
}

function translate(a, b) { return "translate(" + a + "," + b + ")" }


/**
 * Various configurations
 */
function fileInputConfig() {
    return {
        maxFileCount:1, allowedFileExtensions: ['csv'], showPreview: false, showRemove: false,
        uploadClass: 'btn btn-default', uploadLabel: 'Preview',
        uploadIcon: '<span class="glyphicon glyphicon-eye-open"></span> ',
        layoutTemplates: {
            main1: "{preview}<div class='input-group {class}'>" +
            "<div class='input-group-btn'><span class='light-blue'>{browse}</span>" +
            "<span id='data-preview'>{upload}</span>{remove}</div>{caption}</div>"
        }
    }
}