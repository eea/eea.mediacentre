jQuery.fn.delay = function(time,func){
    return this.each(function(){
        setTimeout(func,time);
    });
};

$(document).ready(function(){
    $("#background1").fullBg();
    $("#background2").fullBg();
    $(this).delay(1000,function(){  
        $("#title").fadeOut(2000);
        $("#visual-portal-wrapper").animate({width:"100%"},{queue:false, duration:1000, easing:'easeOutCirc'});
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
    $("#player-title").html(item.caption.innerHTML);
    console.log(video_url);
    $("#media-flowplayer").flashembed({
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
     
     var bg = $("#background2");
     bg.attr('src', thumb_url.replace(/thumb/, "xlarge"));
     bg.fullBg();
     bg.fadeIn('slow',function(){$('#background1').fadeOut('slow',function(){});});
     $('#contentFlow').fadeOut('slow',function(){$('#media-player').fadeIn('slow',function(){});});
}

function hideMediaPlayer(){
    $('#media-player').fadeOut('slow',function(){$('#contentFlow').fadeIn('slow',function(){});});    
    $('#background1').fadeIn('slow',function(){$('#background2').fadeOut('slow',function(){
    var media_flowplayer = $('#media-flowplayer');
	    media_flowplayer.html("Please enable javascript or upgrade to <a href='http://www.adobe.com/go/getflashplayer'/> to watch the video.");
	    media_flowplayer.find('a').html("Flash 9");
	});
    });
}

var myNewFlow = new ContentFlow('contentFlow',{onclickActiveItem:function(item){showMediaPlayer(item);}});
