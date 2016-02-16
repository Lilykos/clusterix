$(function() {
    hljs.initHighlightingOnLoad();

    // Inputs
    DataInput.init();

    // Views
    SearchBox.init();
    Panels.init();

    // Router & Validation
    Router.init();
});