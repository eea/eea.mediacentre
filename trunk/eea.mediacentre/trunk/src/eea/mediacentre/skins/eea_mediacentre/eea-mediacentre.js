(function($) {
    $(document).ready(function() {
        
        // hide unsupported video type for cloudVideo contenttype 
        var $region_content = $("#region-content"),
            $objmeta = $region_content.find('#objmetadata_pbwidgets_wrapper');
        if ($objmeta.length) {
            $region_content.find("dd:contains('video')").closest('dl').hide();
        }

        function prepareVideoLinkURLs() {
            $("#content, #vids-slider, #portal-column-two").delegate(".video-fancybox", "click", function(){
                var $this = $(this);
                if (!$this.data('multimedia')) {
                    var coverflow = $("#multimedia-coverflow"),
                        video_page = coverflow.length > 0 ? 1 : 0;
                    var parent = this;
                    var href = this.href;
                    var isInsidePopUp = $('body').hasClass('video_popup_view');

                    // if we don't have multimedia coverflow then we are in another
                    // multimedia listing like the all faceted navigation folder
                    // therefore we show the full video_popup_view with articles and
                    // related items
                    if (video_page === 0) {
                        if (href.indexOf('video_popup_view') === -1) {
                            this.href = href.replace(/view/, 'video_popup_view'); 
                        }
                    }
                    
                    // general fancybox options, multimedia page will add or modify some
                    // ot these
                    var options = {
                            type: 'iframe',
                            padding: 0,
                            margin: 0,
                            width: 640,
                            height: 564,
                            scrolling: 'no',
                            autoScale: false,
                            autoDimensions: false,
                            centerOnScroll : false,
                            titlePosition: 'inside'
                    };
                    
                    // this code runs when we are inside the multimedia page
                    if (video_page) {
                        // check that the href is already containing
                        // multimedia_popup_view so that this action doesn't occur
                        // every time we hover the link
                        if (href.indexOf('multimedia_popup_view') === -1) {
                            var regex = /view|video_popup_view|multimedia_popup_view/;
                            var clean_href = href.replace(regex, ''); 
                            if (href.indexOf('youtube') === -1) {
                                this.href = clean_href + "multimedia_popup_view"; 
                                options.titleShow = false;
                                $("#fancybox-title").remove();
                            }
                        }

                        var mult = coverflow.offset(),
                            bg = window.whatsnew.multimedia.bg,
                            bg2 = window.whatsnew.multimedia.bg2,
                            $parent = $(parent),
                            src = $parent.find('img');
                        // if the parent can't find the img then we have listing view 
                        var thumb_url = src.length !== 0 ? src[0].src : $parent.closest('div').prev().children()[0].src;

                        options.height = 387;
                        /* options.height = 507; for 4:3 */

                        options.overlayShow = false;
                        options.onStart = function() {
                            //close green tips media player if clicking on a video
                            var media_player = $("#media-player");
                            if (media_player.is(":visible")) {
                                media_player.fadeOut('fast',function(){$("#contentFlow").fadeIn('slow');});
                                $("#media-flowplayer").children().remove();
                            }

                            $.fancybox.center = function() { return false;};
                            $('html, body').animate({scrollTop: 0}, 200, 'linear');
                            $("#fancybox-wrap").hide().css({position : 'absolute'}).animate({
                                left: mult.left - 20,
                                top: mult.top - 20
                            }, 200);   
                            window.setTimeout(function(){
                                if (href.indexOf('youtube') !== -1) {
                                    $("#fancybox-title").remove().prependTo('#fancybox-content');
                                }
                            }, 200);
                        };

                        // function that fills the info area with content from
                        // videopage on multimedia page
                        var info_area = function(iframe, iframe_src, $parent) {
                            var frame, tab_desc, video_title,
                                iframe_eea = iframe_src.indexOf('eea');
                            if (iframe_eea !== -1) {
                                frame = iframe.contents();
                                tab_desc = frame.find("#tab-desc");
                                video_title = frame.find("#video-title").text();
                            }

                            video_title = video_title || $("#fancybox-title").text();
                            var featured_item = $("#featured-items");
                            var featured_item_title = featured_item.find("h3");
                            featured_item_title.text(video_title);
                            var featured_description = featured_item.find(".featured-description");
                            $("#featured-films").fadeOut();
                            tab_desc = tab_desc || $('.photoAlbumEntryDescription', $parent).text();
                            featured_description.html(tab_desc).end().fadeIn();
                            var title_height = featured_item_title.height();
                            var desc_height;
                            // adjust the height of the description panel in accordance
                            // to the height of the title above it whether it spans
                            // over 1, 2 or 3 columns
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
                            // convert the link back to view from multimedia_popup_view
                            // for link button
                            var orig_href = iframe_eea !== -1 ? href.replace(/multimedia_popup_view/, 'view') : 
                                                                        href.replace('embed/', 'watch?v=');
                            featured_item.find(".bookmark-link").attr("href", orig_href);
                        };

                        // fill info area of the multimedia page with content from the
                        // fancybox iframe with video information
                        options.onComplete = function($parent) {
                            var iframe = $("#fancybox-frame"),
                                iframe_src = iframe.attr('src');

                            if (iframe_src.indexOf('youtube') !== -1) {
                                iframe.attr({width: 640, height: 360}).css('height', '360px');
                            }
                            iframe.one("load",function(){
                                info_area(iframe, iframe_src, $parent);
                            });
                        };
                        options.href = this.href;
                    }
                    if (!isInsidePopUp) {
                            $(this).fancybox( options );
                    }
                    $this.data('multimedia', true);
                    $this.click();
                    return false;
                }
                return false;
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

}(jQuery));
