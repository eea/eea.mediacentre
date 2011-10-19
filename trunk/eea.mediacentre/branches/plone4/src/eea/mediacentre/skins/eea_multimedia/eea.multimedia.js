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
        mult.bg = $("#background1"), 
        mult.bg2 = $("#background2"),
        content_flow = $("#contentFlow"),
        media_player = $("#media-player"),
        media_flowplayer = $("#media-flowplayer"),
        multimedia_widgets = $("#multimedia-widgets"),
        top_widgets  = $("#top-widgets"),
        bottom_widgets = $("#bottom-widgets");
        mult.bg2.fullBg();
        
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
            var tags = $("#c8").find('li');
            tags.unbind();
            // remove default theme vocabulary item from tags
            /* $('#c8default').remove(); */
            $('#c8all').text("All topics").addClass('selected');
            
            // changes the results of the whatsnewgallery when clicking on
            // a theme 
            tags.click(function(){
                var tag_title = this.title,
                    sel_value = tag_title === 'All' ? undefined : tag_title,
                    sel_text = this.innerHTML,
                    index;
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
            jQuery("#player-title").html(item.caption.innerHTML);
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
               scaleFactor : 2.0,
               reflectionHeight: 0
        });

}); 
})(jQuery);

