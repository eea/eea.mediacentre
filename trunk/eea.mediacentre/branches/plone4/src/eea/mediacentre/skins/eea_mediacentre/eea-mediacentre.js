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
            var video_page = window.location.href.indexOf('videopage') != '-1' ? true : undefined;
            var options = {
                    type: 'iframe',
                    padding: 0,
                    margin: 0,
                    width: 675,
                    height: 564,
                    scrolling: 'no',
                    autoScale: false,
                    autoDimensions: false,
                    centerOnScroll : false
            };
            if (video_page) {
                var mult = $("#multimedia-coverflow").offset();
                options.width = 650;
                options.onStart = function() {
                    $.fancybox.center = function() { return false;};
                    $('html, body').animate({scrollTop: 0}, 200);
                    $("#fancybox-wrap").css({position : 'absolute'}).animate({
                        left: mult.left - 18,
                        top: mult.top - 18
                    }, 200);   
                };            
            }
            if (!isInsidePopUp) {
                    $(this).fancybox( options );
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

