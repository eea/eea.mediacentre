(function($) {

    jQuery.fn.delay = function(time,func){
        return this.each(function(){
            setTimeout(func,time);
        });
    };

    jQuery(document).ready(function($){
        var $body = $('html, body');
        var multimedia_logo = $("#multimedia-logo");
        var multimedia_header = $("#parent-fieldname-title");
        var faceted_form = $("#faceted-form");
        faceted_form.hide();
        window.whatsnew.multimedia = { }; 
        var mult = window.whatsnew.multimedia;
             mult.bg = $("#background1");
             mult.bg2 = $("#background2");

        // add background and colophon based on cookie if present else get the
        // first background and show it
        var background_imgs = $("#backgrounds").find('img');
        var colophon_imgs = $(".colophon-right").find('img');
        var colophon_img = SubCookieUtil.get('multimedia', 'colophon-image');
        if ( colophon_img ) {
            var index = parseInt(colophon_img, 10);
            var bg = background_imgs[index];
            var cl =  colophon_imgs[index];
            colophon_imgs.removeClass('selected');
            cl.className = 'selected';
            bg.src = cl.src.replace(/\/image_thumb/, '');
            $(bg).fullBg();
        }
        else {
            $("#background1").fullBg();
        }

        var content_flow = $("#contentFlow"),
            media_player = $("#media-player"),
            media_flowplayer = $("#media-flowplayer"),
            multimedia_widgets = $("#multimedia-widgets"),
            top_widgets  = $("#top-widgets"),
            bottom_widgets = $("#bottom-widgets");
        var player_title = document.getElementById("player-title");
        // move the footer and colophon out of visual-portal-wrapper
        var footer = $("#visual-portal-wrapper").find(".row").last();
        footer.detach().appendTo("body");
        var colophon = $("#portal-colophon");
        colophon.detach().appendTo("body");

        // background switching
        var cookie_expires = new Date();
            cookie_expires.setMonth(cookie_expires.getMonth() + 1); // one month
        var data_page = window.whatsnew.gallery_page;
        var colophon_links = $(".colophon-right").find('a');
        colophon_links.click(function(e){
            var $this = $(this);
            colophon_imgs.removeClass('selected');
            var img = $this.children();
            img.addClass("selected");
            var selected_index = $this.index();
            SubCookieUtil.set(data_page, "colophon-image", selected_index, expires = cookie_expires);
            var sel = background_imgs.filter(':visible');
            $(background_imgs[selected_index]).css({zIndex : -1 }).fadeIn('slow', function(){ sel.fadeOut('fast');});
            e.preventDefault(); 
        });

        // animate the positon of the title, and the top and bottom widgets
        $(this).delay(1000,function(){
            $("#title").fadeOut(2000);
        }).delay(3000,function(){
            multimedia_widgets.animate({height:"775px"},{queue:false, duration:500, easing:'easeOutCirc'});
        }).delay(3500,function(){
            $("#top-widgets, #bottom-widgets").animate({top:"0px"},{queue:false, duration:1000, easing:'easeInOutBack'});
            $("#cross-site-top, #portal-header, #footer-wrapper").slideUp('fast');
            multimedia_header.animate({left: 0}, 1000);
            multimedia_logo.animate({left: 0}, 1000);
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
                    $body.animate({scrollTop: 0}, 1200, 'linear');
                    return false;
                });
            });

            // get all of the colophon images that are not selected
            var col_imgs = colophon_imgs.not('.selected');
            var hid_imgs = background_imgs.filter(':hidden');
            var vis_img = background_imgs.filter(':visible');
            col_imgs.each( function(i){
                var $back = $(hid_imgs[i]);
                var col_img = this;
                $back.attr('src', this.src.replace(/\/image_thumb/, ''));
                $back.css({zIndex : -2, width: vis_img.css('width'), height: vis_img.css('height')}).hide();
            });
            // changes the results of the whatsnewgallery when clicking on
            // a theme
            tags.click(function(){
                // this code is for tags 
                // var tag_title = this.title,
                //     sel_value = tag_title === 'All' ? '' : tag_title,
                
                // scroll window to the bottom when clicking of tags to focus
                // on the whatsnewgallery
                var $window = $(window);
                var win_height = $window.height(); 
                var win_scroll = $window.scrollTop();
                var scrollBottom = win_scroll + win_height;
                if ( win_scroll !== scrollBottom ) {

                    $body.animate({scrollTop: scrollBottom}, 1200, 'linear');
                }

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
        // end delay 3500
        });

        function showMediaPlayer(item){
            var thumb_url = item.content ? item.content.src : item.src,
                video_url = thumb_url.substring(0, thumb_url.length - 11);
            var link = item.caption ? item.caption : 1;
            player_title.innerHTML = link !== 1 ? item.caption.innerHTML : item.title;
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
                var current = link !== 1 ? $(item.content) : $(item);
                media_flowplayer.flashembed({
                        src: current.attr('rel')
                });
            }
            content_flow.fadeOut('slow',function(){media_player.fadeIn('slow');});
        }

        // displays media player, changes background image to the image of the
        // played file
        var coverflow_imgs = $("#coverflow").find('img');
        coverflow_imgs.click(function(e){
            var $this = $(this);
            if ( this.className === "content selected") {
                showMediaPlayer(this);
            }
            coverflow_imgs.removeClass('selected');
            this.className = "content selected";
        });
        // closes the fancybox window
        $("#fancybox-close").click(function(){
            media_player.fadeOut('fast',function(){content_flow.fadeIn('slow');});
        });

        // contentFlow configurations
        if ( window.location.href.indexOf(2) === -1 ) {
            var myNewFlow = new ContentFlow('contentFlow',{
                   onclickActiveItem:function(item){showMediaPlayer(item);},
                   reflectionHeight: 0,
                   flowDragFriction: 1,
                   startOnLoad: true
            });
        }

    // end ready state
    });
})(jQuery);

