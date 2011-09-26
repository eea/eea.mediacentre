(function($) {
$(document).ready(function() {

    function prepareVideoLinkURLs() {
        $("#content, #vids-slider").delegate(".video-fancybox", "hover", function(){
            var regex = /(\/$|\/view\/?$|\/video_popup_view\/?$)/;
            var href = this.href;
            href = href.replace(regex, ''); // remove any trailing '/view' or '/'
            href = href + "/video_popup_view";
            this.href = href; 
            var isInsidePopUp = $('body').hasClass('video_popup_view');
            if (!isInsidePopUp) {
                    $(this).fancybox({
                        type: 'iframe',
                        padding: 0,
                        margin: 0,
                        width: 675,
                        height: 564,
                        scrolling: 'no',
                        autoScale: false,
                        autoDimensions: false,
                        titlePosition: 'wrap'
                    });
            }
        });
    }
    prepareVideoLinkURLs();

    if ($.fn.fancybox === undefined) {
        return;
    }


    if (window.Faceted) {
        jQuery(Faceted.Events).bind(Faceted.Events.AJAX_QUERY_SUCCESS, function(evt) {
            prepareVideoLinkURLs();

        });
    }

});

})(jQuery);

