jQuery.fn.delay = function(time,func){
    return this.each(function(){
        setTimeout(func,time);
    });
};

jQuery(document).ready(function($){
    var bg = $("#background1"); 
    bg.hide();
    bg.fullBg();
    bg.fadeIn();
    $("#background2").fullBg();

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
}); 

function showMediaPlayer(item){
    var thumb_url = item.content.getAttribute('src'),
        video_url = thumb_url.substring(0, thumb_url.length - 12);
    jQuery("#player-title").html(item.caption.innerHTML);
    console.log(video_url);
    jQuery("#media-flowplayer").flashembed({
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
     
     var bg = jQuery("#background2");
     bg.attr('src', thumb_url.replace(/thumb/, "xlarge"));
     bg.fullBg();
     bg.fadeIn('slow',function(){jQuery('#background1').fadeOut('slow',function(){});});
     jQuery('#contentFlow').fadeOut('slow',function(){jQuery('#media-player').fadeIn('slow',function(){});});
}

function hideMediaPlayer(){
    jQuery('#media-player').fadeOut('slow',function(){jQuery('#contentFlow').fadeIn('slow',function(){});});    
    jQuery('#background1').fadeIn('slow',function(){jQuery('#background2').fadeOut('slow',function(){
    var media_flowplayer = jQuery('#media-flowplayer');
	    media_flowplayer.html("Please enable javascript or upgrade to <a href='http://www.adobe.com/go/getflashplayer'/> to watch the video.");
	    media_flowplayer.find('a').html("Flash 9");
	});
    });
}

var myNewFlow = new ContentFlow('contentFlow',{onclickActiveItem:function(item){showMediaPlayer(item);}});
