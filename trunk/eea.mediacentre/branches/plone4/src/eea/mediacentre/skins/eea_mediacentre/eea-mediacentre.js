(function($) {
$(document).ready(function() {

    function prepareVideoLinkURLs() {
        $("#content, #vids-slider").delegate(".video-fancybox", "hover", function(){
            var regex = /(\/$|\/view\/?$|\/video_popup_view\/?$)/;
            var href = this.href;
            href = href.replace(regex, ''); // remove any trailing '/view' or '/'
            href = href + "/video_popup_view";
            this.href = href; 
            var parent = this;
            var isInsidePopUp = $('body').hasClass('video_popup_view');
            var coverflow = $("#multimedia-coverflow"),
                video_page = coverflow.length > 0 ? 1 : 0;
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
                var mult = coverflow.offset(),
                    bg = window.whatsnew.multimedia.bg,
                    bg2 = window.whatsnew.multimedia.bg2,
                    thumb_url = $(parent).find('img')[0].src;

                options.width = 650;
                options.onStart = function() {
                    $.fancybox.center = function() { return false;};
                    $('html, body').animate({scrollTop: 0}, 200);
                    $("#fancybox-wrap").css({position : 'absolute'}).animate({
                        left: mult.left - 18,
                        top: mult.top - 18
                    }, 200);   
                    
                        bg2.attr('src', thumb_url.replace(/thumb/, "xlarge"));
                        bg2.fullBg();
                        bg2.fadeIn('slow',function(){bg.fadeOut('slow',function(){});});
                };            
                options.onCleanup = function(){
                    bg.show();
                    bg2.hide();
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


