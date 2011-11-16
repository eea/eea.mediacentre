(function($) {
$(document).ready(function() {

    function prepareVideoLinkURLs() {
        $("#content, #vids-slider").delegate(".video-fancybox", "hover", function(){
            var regex = /(\/$|\/view\/?$|\/video_popup_view\/?$)/;
            var orig_href = this.href;
            var clean_href = orig_href.replace(regex, ''); // remove any trailing '/view' or '/'
            this.href = clean_href + "/video_popup_view"; 
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
                    $parent = $(parent),
                    src = $parent.find('img');
                // if the parent can't find the img then we have listing view 
                var thumb_url = src.length !== 0 ? src[0].src : $parent.closest('div').prev().children()[0].src;

                options.width = 650;
                options.height = 387;
                options.overlayShow = false;
                options.onStart = function() {
                    $.fancybox.center = function() { return false;};
                    $('html, body').animate({scrollTop: 0}, 200);
                    $("#fancybox-wrap").css({position : 'absolute'}).animate({
                        left: mult.left - 18,
                        top: mult.top - 18
                    }, 200);   
                };
                options.onComplete = function() {
                    window.setTimeout(function() {
                        // get the description tab from video_popup_view which contains desc,
                        // video link, title, author and other key information
                        var iframe = $("#fancybox-frame").contents();
                        var tab_desc = iframe.find("#tab-desc");
                        var featured_item = $("#featured-items");
                        tab_desc.css({position : 'relative', display: 'block', height: '145px', top: '0px', minHeight: '145px', maxHeight:'200px'});
                        $("#featured-films").fadeOut();
                        featured_item.find(".featured-description").html(tab_desc).end().fadeIn();
                        var title = iframe.find("#video-title").text();
                        featured_item.find("h3").text(title);
                        $(".bookmark-link").attr("href", orig_href);
                        $(".vid-dl-link").attr("href", clean_href);
                    }, 2000);
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


