(function($) {

    jQuery.fn.delay = function(time,func){
        return this.each(function(){
            setTimeout(func,time);
        });
    };

    $(window).load(function() {
        $("#background1").fullBg();
    });

    jQuery(document).ready(function($){
        var faceted_form = $("#faceted-form");
        faceted_form.hide();
        window.whatsnew.multimedia = { };
        var mult = window.whatsnew.multimedia;
            mult.bg = $("#background1");
            /* mult.bg2 = $("#background2"); */
        var content_flow = $("#contentFlow"),
            media_player = $("#media-player"),
            media_flowplayer = $("#media-flowplayer"),
            multimedia_widgets = $("#multimedia-widgets"),
            top_widgets  = $("#top-widgets"),
            bottom_widgets = $("#bottom-widgets");
        /* mult.bg2.fullBg(); */
        var player_title = document.getElementById("player-title");
        // move the footer and colophon out of visual-portal-wrapper
        var footer = $("#visual-portal-wrapper").find(".row").last();
        footer.detach().appendTo("body");
        var colophon = $("#portal-colophon");
        colophon.detach().appendTo("body");

        // animate the positon of the title, and the top and bottom widgets
        $(this).delay(1000,function(){
            $("#title").fadeOut(2000);
        }).delay(3000,function(){
            multimedia_widgets.animate({height:"775px"},{queue:false, duration:500, easing:'easeOutCirc'});
        }).delay(3500,function(){
            $("#top-widgets, #bottom-widgets").animate({top:"0px"},{queue:false, duration:1000, easing:'easeInOutBack'});
            $("#cross-site-top, #portal-header, #footer-wrapper, #portal-colophon").slideUp('fast');
            // show faceted_form after the animation of the multimedia items to
            // avoid it appearing when the title is animating
            faceted_form.show();
            // unbind any events from the tag cloud items
            var tags = $("#c10").find('li');
            tags.unbind();
            // remove default theme vocabulary item from tags
            $('#c10default').remove();
            $('#c10all').text("All topics").addClass('selected');

        $("#animations-highlights").delegate("a.animation-fancybox", "hover", function(){
            var $this = $(this);
            $this.click( function(){
                var swf_href = this.href.replace(/(view|video_popup_view)/, "getFile");
                player_title.innerHTML = $this.attr('alt');
                media_flowplayer.flashembed({
                        src: swf_href
                });
                content_flow.fadeOut('slow',function(){media_player.fadeIn('slow');});
                var mult = content_flow.offset();
                $('html, body').animate({scrollTop: 0}, 200);
                return false;
            });
        });
            // changes the results of the whatsnewgallery when clicking on
            // a theme
            tags.click(function(){
                // this code is for tags 
                // var tag_title = this.title,
                //     sel_value = tag_title === 'All' ? '' : tag_title,
                var tag_id = this.id.substr(3),
                    sel_value = tag_id === 'all' ? '' : tag_id,
                    sel_text = this.innerHTML,
                    index,
                    tag_title;
                tags.filter('.selected').removeClass('selected');
                this.className = "selected";
                var tabs = $("#tabs"),
                    cur_tab_val = tabs.find('a').filter('.current')[0].id.substr(4);
                window.whatsnew.whatsnew_func(cur_tab_val, sel_text, sel_value, index, tag_title);
            });
        });

        // displays media player, changes background image to the image of the
        // played file
        function showMediaPlayer(item){
            var thumb_url = item.content.src,
                video_url = thumb_url.substring(0, thumb_url.length - 11);
            player_title.innerHTML = item.caption.innerHTML;
            if ( video_url.indexOf('films') === -1) {
                media_flowplayer.flashembed(
                    {
                        src:'%2B%2Bresource%2B%2Bflowplayer/flowplayer-3.2.2.swf'
                    },
                    {
                        config:{
                            clip: {
                                'url' : video_url,
                                'autoBuffering': true,
                                'autoPlay': true,
                                'loop': false
                            },
                            'useNativeFullScreen': true,
                            'initialScale': 'fit'
                        }
                    });

            }
            else {
                media_flowplayer.flashembed({
                        src:'http://vimeo.com/moogaloop.swf?clip_id=8119882&autoplay=true'
                });
            }
            content_flow.fadeOut('slow',function(){media_player.fadeIn('slow');});
        }

        // closes the fancybox window
        $("#fancybox-close").click(function(){
            media_player.fadeOut('fast',function(){content_flow.fadeIn('slow');});
        });

        // contentFlow configurations
        var myNewFlow = new ContentFlow('contentFlow',{
               onclickActiveItem:function(item){showMediaPlayer(item);},
               reflectionHeight: 0
        });

});
})(jQuery);

