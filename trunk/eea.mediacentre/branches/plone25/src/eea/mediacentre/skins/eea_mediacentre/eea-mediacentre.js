$(document).ready(function() {

    function prepareVideoLinkURLs() {
        $('.video-fancybox').each(function() {
            var regex = /(\/$|\/view\/?$|\/video_popup_view\/?$)/;
            var href = $(this).attr('href');
            href = href.replace(regex, ''); // remove any trailing '/view' or '/'
            href = href + "/video_popup_view";
            $(this).attr('href', href);
        });
    }
    prepareVideoLinkURLs();

    if ($.fn.fancybox === undefined) {
        return;
    }

    function prepareVideoLinks() {
        var isInsidePopUp = $('body').hasClass('video_popup_view');
        if (!isInsidePopUp) {
            $('.video-fancybox').each(function() {
                $(this).fancybox({
                    type: 'iframe',
                    padding: 0,
                    margin: 0,
                    width: 675,
                    height: 564,
                    scrolling: 'no',
                    autoScale: false,
                    autoDimensions: false
                });
            });
        }
    }
    prepareVideoLinks();

    if (window.Faceted) {
        jQuery(Faceted.Events).bind(Faceted.Events.AJAX_QUERY_SUCCESS, function(evt) {
            prepareVideoLinkURLs();
            prepareVideoLinks();
        });
    }

});
