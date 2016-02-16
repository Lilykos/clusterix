var TabScroller = (function() {

    var hidWidth;
    var scrollBarWidths = 40;

    function widthOfList() {
        var itemsWidth = 0;
        $('.list li').each(function() {
            itemsWidth += $(this).outerWidth();
        });
        return itemsWidth;
    }

    function widthOfHidden() {
        return (($('.wrapper').outerWidth()) - widthOfList() - getLeftPosi()) - scrollBarWidths;
    }

    function getLeftPosi() {
        return $('.list').position().left;
    }

    function reAdjust() {
        if (($('.wrapper').outerWidth()) < widthOfList()) {
          $('.scroller-right').show();
        } else {
          $('.scroller-right').hide();
        }

        if (getLeftPosi() < 0) {
          $('.scroller-left').show();
        } else {
          $('.item').animate({ left: "-=" + getLeftPosi() + "px" }, 'slow');
          $('.scroller-left').hide();
        }
    }

    return {
        init: function() {
            reAdjust();

            $(window).on('resize', function(e) {
                reAdjust();
            });

            $('.scroller-right').click(function() {
                $('.scroller-left').fadeIn('slow');
                $('.scroller-right').fadeOut('slow');
                $('.list').animate(
                    { left: "+=" + widthOfHidden() + "px" }, 'slow', function() {}
                );
            });

            $('.scroller-left').click(function() {
                $('.scroller-right').fadeIn('slow');
                $('.scroller-left').fadeOut('slow');

                $('.list').animate(
                    { left: "-=" + getLeftPosi() + "px" }, 'slow', function() {}
                );
            });

            console.log('Tab scroller init');
        }
    };
})();