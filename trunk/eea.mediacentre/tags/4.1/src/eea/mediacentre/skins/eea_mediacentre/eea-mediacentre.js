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
                    //close green tips media player if clicking on a video
                    var media_player = $("#media-player");
                    if (media_player.is(":visible")) {
                        media_player.fadeOut('fast',function(){$("#contentFlow").fadeIn('slow');});
                        $("#media-flowplayer").children().remove();
                    }

                    $.fancybox.center = function() { return false;};
                    $('html, body').animate({scrollTop: 0}, 200);
                    $("#fancybox-wrap").css({position : 'absolute'}).animate({
                        left: mult.left - 18,
                        top: mult.top - 18
                    }, 200);   
                };

                // function tthat fills the info area with content from
                // videopage on multimedia page
                var info_area = function(iframe) {
                    var frame = iframe.contents();
                    var tab_desc = frame.find("#tab-desc");
                    var featured_item = $("#featured-items");
                    var video_title = frame.find("#video-title").text();
                    var featured_item_title = featured_item.find("h3");
                    featured_item_title.text(video_title);
                    tab_desc.css({position : 'relative', display: 'block',  top: '0px', height: ''});
                    var featured_description = featured_item.find(".featured-description");
                    $("#featured-films").fadeOut();
                    featured_description.html(tab_desc).end().fadeIn();
                    var title_height = featured_item_title.height();
                    var desc_height;
                    if (title_height === 21) {
                        desc_height = "184px";
                    }
                    else if (title_height === 42) {
                        desc_height = "163px";
                    }
                    else {
                        desc_height = "142px";
                    }
                    featured_description.css({height: desc_height});
                    // convert the link back to view from video_popup_view
                    // for link button
                    orig_href = orig_href.replace(/video_popup_view/, 'view');
                    featured_item.find(".bookmark-link").attr("href", orig_href);
                };

                // fill info area of the multimedia page with content from the
                // fancybox irframe with video information
                options.onComplete = function() {
                    var iframe = $("#fancybox-frame");
                    iframe.one("load",function(){
                        info_area(iframe);
                    });
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


