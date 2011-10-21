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
        window.whatsnew.multimedia = { };
        var mult = window.whatsnew.multimedia;
            mult.bg = $("#background1");
            mult.bg2 = $("#background2");
        var content_flow = $("#contentFlow"),
            media_player = $("#media-player"),
            media_flowplayer = $("#media-flowplayer"),
            multimedia_widgets = $("#multimedia-widgets"),
            top_widgets  = $("#top-widgets"),
            bottom_widgets = $("#bottom-widgets");
        mult.bg2.fullBg();
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

            // unbind any events from the tag cloud items
            var tags = $("#c10").find('li');
            tags.unbind();
            // remove default theme vocabulary item from tags
            $('#c10default').remove();
            $('#c10all').text("All topics").addClass('selected');

        $("#animations-highlights").delegate("a.animation-fancybox", "hover", function(){
            $(this).click( function(){
                var swf_href = this.href.replace(/(view|video_popup_view)/, "getFile");
                player_title.innerHTML = this.title;
                media_flowplayer.flashembed({
                        src: swf_href
                });
                media_player.fadeIn('slow');
                var mult = content_flow.offset();
                $('html, body').animate({scrollTop: 0}, 200);
                media_player.animate({
                    left: 0,
                    top: 0
                }, 2000);   
                content_flow.fadeOut('slow');
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
                    sel_value = tag_title === 'all' ? '' : tag_id,
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
                video_url = thumb_url.substring(0, thumb_url.length - 12);
            player_title.innerHTML = item.caption.innerHTML;
            media_flowplayer.flashembed(
                {
                    src:'%2B%2Bresource%2B%2Bflowplayer/flowplayer-3.2.2.swf'
                },
                {
                    config:{
                        clip: {
                            'url' : video_url,
                            'autoBuffering': true,
                            'autoPlay': false,
                            'loop': false
                        },
                        'useNativeFullScreen': true,
                        'initialScale': 'fit'
                    }
                });

             mult.bg2.attr('src', thumb_url.replace(/thumb/, "xlarge"));
             mult.bg2.fullBg();
             mult.bg2.fadeIn('slow',function(){mult.bg.fadeOut('slow',function(){});});
             content_flow.fadeOut('slow',function(){media_player.fadeIn('slow',function(){});});
        }

        // closes the fancybox window
        $("#fancybox-close").click(function(){
            media_player.fadeOut('fast',function(){content_flow.fadeIn('slow',function(){});});
            mult.bg.fadeIn('slow',function(){mult.bg2.fadeOut('slow');});
        });

        // contentFlow configurations
        var myNewFlow = new ContentFlow('contentFlow',{
               onclickActiveItem:function(item){showMediaPlayer(item);},
               reflectionHeight: 0
        });

});
})(jQuery);

