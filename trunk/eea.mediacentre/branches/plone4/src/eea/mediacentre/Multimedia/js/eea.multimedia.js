(function($) {
    jQuery.fn.delay = function(time,func){
        return this.each(function(){
            setTimeout(func,time);
        });
    };

    jQuery(document).ready(function($){

        var bg = $("#background1"), 
        bg2 = $("#background2"),
        content_flow = $("#contentFlow"),
        media_player = $("#media-player"),
        media_flowplayer = $("#media-flowplayer");
        bg.hide();
        bg.fullBg();
        bg.fadeIn();
        bg2.fullBg();

        var footer = $("#visual-portal-wrapper").find(".row").last();
        footer.detach().appendTo("body");
        var colophon = $("#portal-colophon");
        colophon.detach().appendTo("body");
        
        $(this).delay(1000,function(){  
            $("#title").fadeOut(2000);
            /* $("#visual-portal-wrapper").animate({width:"1024px"},{queue:false, duration:1000, easing:'easeOutCirc'}); */
        }).delay(3000,function(){  
            $("#multimedia-widgets").animate({height:"640px"},{queue:false, duration:500, easing:'easeOutCirc'});
        }).delay(3500,function(){  
            $("#top-widgets").animate({top:"0px"},{queue:false, duration:1000, easing:'easeInOutBack'});
            $("#bottom-widgets").animate({top:"430px"},{queue:false, duration:1000, easing:'easeInOutBack'});
        });

    function showMediaPlayer(item){
        var thumb_url = item.content.getAttribute('src'),
            video_url = thumb_url.substring(0, thumb_url.length - 12);
        jQuery("#player-title").html(item.caption.innerHTML);
        media_flowplayer.flashembed({
            src:'++resource++flowplayer/flowplayer-3.2.2.swf'
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
        } 
        );
         
         bg2.attr('src', thumb_url.replace(/thumb/, "xlarge"));
         bg2.fullBg();
         bg2.fadeIn('slow',function(){bg.fadeOut('slow',function(){});});
         content_flow.fadeOut('slow',function(){media_player.fadeIn('slow',function(){});});
    }

    $("#fancybox-close").click(function(){
        media_player.fadeOut('slow',function(){content_flow.fadeIn('slow',function(){});});    
        bg.fadeIn('slow',function(){bg2.fadeOut('slow',function(){
            media_flowplayer.html("Please enable javascript or upgrade to <a href='http://www.adobe.com/go/getflashplayer'/> to watch the video.");
            media_flowplayer.find('a').html("Flash 9");
        });
        });
    });

    var myNewFlow = new ContentFlow('contentFlow',{onclickActiveItem:function(item){showMediaPlayer(item);}});

}); 
})(jQuery);
