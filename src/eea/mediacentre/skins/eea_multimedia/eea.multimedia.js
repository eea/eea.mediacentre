(function($) {

    jQuery.fn.delay = function(time,func){
        return this.each(function(){
            setTimeout(func,time);
        });
    };

    jQuery(document).ready(function($){
        var win_href = window.location.href,
            win_lastChar = win_href.charAt([win_href.length - 1]);
        if(win_lastChar === 'a' || win_href.indexOf('view') !== -1) {
            var $body = $('html, body');
            var multimedia_logo = $("#multimedia-logo");
            var multimedia_header = $("#parent-fieldname-title");
            var faceted_form = $("#faceted-form");
            faceted_form.hide();
            window.whatsnew.multimedia = { }; 
            var mult = window.whatsnew.multimedia;
                 mult.bg = $("#background1");
                 mult.bg2 = $("#background2");
            var ajax_loader_img = '<div style="text-align: center;"><img src="++resource++faceted_images/ajax-loader.gif" /></div>';
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
                $(bg).fullBg().fadeIn();
            }
            else {
                if(mult.bg.length) {
                    mult.bg.fullBg().fadeIn();
                }
            }

            var content_flow = $("#contentFlow"),
                media_player = $("#media-player"),
                media_flowplayer = $("#media-flowplayer"),
                multimedia_widgets = $("#multimedia-widgets"),
                bottom_widgets = $("#bottom-widgets");
            var player_title = document.getElementById("player-title");
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
                
                $("#faceted-tabs").tabs("#tag-cloud-content > div.faceted-widget", function(event, index) {
                    var cur_tab = this.getTabs()[index],
                        cur_tab_val = cur_tab.id.substr(8);
                    if (cur_tab_val === "tags") {
                        $("#c3").find('li').unbind();
                    }
                });

                var top_widgets  = $("#top-widgets");
                var top_widget_offset, top_widget_left, top_widget_top;
                function top_widget_offset_init() {
                    top_widget_offset =  top_widgets.offset();
                    top_widget_left = top_widget_offset.left;
                    top_widget_top = top_widget_offset.top;
                }
                window.setTimeout(top_widget_offset_init, 1050);

                var item_info = function(item, orig_href, clean_href) {
                            // get the description tab from video_popup_view which contains desc,
                            // video link, title, author and other key information
                            var $this = item;
                            var tab_desc = $this.find(".photoAlbumEntryDescription").text();                        
                            var featured_item = $("#featured-items");
                            $("#featured-films").fadeOut();
                            
                            var featured_description = featured_item.find(".featured-description");
                            featured_description.html(tab_desc).end().fadeIn();
                            
                            var title = $this.find(".photoAlbumEntryTitle").text();
                            var featured_item_title = featured_item.find("h3");
                            featured_item_title.text(title);
                            
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

                            $(".bookmark-link").attr("href", orig_href);
                };

                $("#greentips-highlights").delegate("a.animation-fancybox", "click", function(){
                    var $that = $(this);
                    if(!$that.data('greentips')) {
                        $that.click( function(){
                            // hide videoplayer if it's still open when we click on an
                            // animation
                            var $this = $(this);
                            var fancybox_wrap = $("#fancybox-wrap");
                            if (fancybox_wrap.is(":visible")) {
                                fancybox_wrap.fadeOut('fast',function(){$("#contentFlow").fadeIn('fast');});
                                $("#fancybox-frame").remove();
                            }

                            var orig_href = this.href;
                            var clean_href = this.href.replace(/(view|video_popup_view)/, "");
                            var swf_href = this.href.replace(/(view|video_popup_view)/, "getFile");
                            player_title.innerHTML = this.title;
                            media_flowplayer.flashembed({
                                    src: swf_href
                            });
                            content_flow.fadeOut('slow',function(){media_player.fadeIn('slow');});
                            var mult = content_flow.offset();
                            $body.animate({scrollTop: 0}, 600, 'linear');
                            item_info($this, orig_href, clean_href);
                            return false;
                        });
                        $that.data('greentips', true);
                        $that.click();
                        return false;
                    }
                    return false;
                });

                $("#imagegalleries-highlights").delegate(".gallery-ajax a", "click", function(){
                    var $this;
                    var href = this.href;
                    if (href.indexOf('fancybox') === -1) {
                        $this = $(this);
                        // close animations if they are still running when clicking
                        // on an image gallery
                        if (media_player.is(":visible")) {
                            media_player.fadeOut('fast',function(){$("#contentFlow").fadeIn('slow');});
                            $("#media-flowplayer").children().remove();
                        }
                        
                        // set link to gallery with different links depending
                        // whether we have normal galleries or atlas galleries
                        // which stores the photos in the photos directory
                        var res_href = href.indexOf('atlas') === -1 ? href + "/gallery_fancybox_view" : 
                                                            href + "/photos/gallery_fancybox_view";
                        $this.attr('href', res_href);

                        $this.fancybox({
                            type: 'iframe',
                            padding: 0,
                            margin: 0,
                            width: 640,
                            height: 501,
                            scrolling: 'no',
                            autoScale: false,
                            autoDimensions: false,
                            centerOnScroll: false,
                            overlayShow: false, 
                            titleShow: false,
                            onStart : function() {
                                // this function brings the fancybox to the top of
                                // the multimedia topright-widgets
                                $.fancybox.center = function() { return false;};
                                $('html, body').animate({scrollTop: 0}, 200);
                                $("#fancybox-wrap").hide().css({position : 'absolute'}).animate({
                                    left: top_widget_left - 14, // "260px"
                                    top: top_widget_top - 20 //,"100px" 
                                }, 200);
                            }
                        });

                        // send information to the item_info which is responsible
                        // for changing the about this item information 
                        $this.click(function() {
                            var orig_href = href.indexOf('atlas') === -1 ? href : href + "/photos";
                            item_info($this, orig_href, orig_href);
                        });
                        // redo the click event after clicking to start the
                        // gallery_view
                        $this.click();
                    }
                    return false;
                });
                // get all of the colophon images that are not selected
                var col_imgs = colophon_imgs.not('.selected');
                var hid_imgs = background_imgs.filter(':hidden');
                var vis_img  = background_imgs.filter(':visible');
                col_imgs.each(function(i){
                    var $back = $(hid_imgs[i]);
                    var col_img = this;
                    $back.attr('src', this.src.replace(/\/image_thumb/, ''));
                    $back.css({zIndex : -2, width: vis_img.css('width'), height: vis_img.css('height')});
                    $back.attr('alt', 'Switch background image');
                    $back.fullBg();
                    $back.hide();
                });
                // changes the results of the whatsnewgallery when clicking on
                // a theme
                var tags = $("#tag-cloud-content");
                var tags_li = tags.find('li').unbind();
                // remove items that have no results
                tags_li.filter(function(){
                    return this.value === 1 && this.title !== "All";
                }).remove();

                // remove default theme vocabulary item from tags
                $('#c1default').remove();
                $('#c1all').addClass('selected');
                $('#c3all').addClass('selected');

                tags.delegate('li', 'click', function(){
                    var tag_id = window.isNaN(this.id[3]) ? this.id.substr(2) : this.id.substr(3),
                        sel_value = tag_id === 'all' ? '' : tag_id,
                        sel_text = this.innerHTML,
                        index,
                        tag_title;

                    var tabs = $("#multimedia-tabs"),
                        cur_tab_val = tabs.find('a').filter('.current')[0].id.substr(4);
                    // only refresh highlights if we are on video or greentips tabs               
                    var c1 = $("#c1_widget");
                    // remove previously selected item before assigning selected to
                    // the currently clicked item
                    if (c1.is(":visible")) {
                        c1.find('li').filter('.selected').removeClass('selected');
                    }
                    else {
                        $("#c3").find('li').filter('.selected').removeClass('selected');
                    }
                    this.className = "selected";
                    
                    // don't send value if tag_title is All because we don't have
                    // a value to send
                    if ($(this).parent().prev().text().indexOf('tags') !== -1 ) { 
                        tag_title = this.title;
                        sel_value = tag_title === 'All' ? '' : tag_title;
                    }

                    var cur_tab_highlight = $("#whatsnew-gallery").find('.eea-tabs-panel').filter(':visible');
                    cur_tab_highlight.find(".gallery-ajax").html(ajax_loader_img);
                    window.whatsnew.whatsnew_func(cur_tab_val, sel_text, sel_value, index, tag_title);
                });
            // end delay 3500
            });

            var showMediaPlayer = function(item){
                var thumb_url =  item.src,
                    video_url = thumb_url.substring(0, thumb_url.length - 11);
                player_title.innerHTML = item.title;
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
                    var current = $(item);
                    media_flowplayer.flashembed({
                            src: current.attr('rel')
                    });
                }
                content_flow.fadeOut('slow',function(){media_player.fadeIn('slow');});
            };

            // displays media player, changes background image to the image of the
            // played file
            var coverflow_imgs = $("#coverflow").find('img');
            var featured_films = $("#featured-films");
            var featured_artic = featured_films.find("#artic");
            var featured_degree = featured_films.find("#degree");
            coverflow_imgs.click(function(e){
                var $this = $(this);
                if ( this.className === "content selected") {
                    showMediaPlayer(this);
                    var title = this.title;
                    $("#featured-items").fadeOut('slow');
                    featured_films.fadeIn('slow');
                    if (title.indexOf('arctic') !== -1) {
                        featured_degree.fadeOut('slow');
                        featured_artic.fadeIn('slow');
                    }
                    else if (title.indexOf('degree') !== -1) {
                        featured_degree.fadeIn('slow');
                        featured_artic.fadeOut('slow');
                    }
                    else {
                        featured_films.fadeOut();
                        var featured_item = $("#featured-items");
                        var featured_item_title = featured_item.find("h3");
                            featured_item_title.text(this.title);
                        $("#featured-location").find(".bookmark-link").attr("href", this.src.replace(/image_wide/, 'view'));
                        featured_description = featured_item.find(".featured-description");
                        featured_description.text('Concepts such as Green Economy, Resource efficiency and Sustainable Consumption and Production are currently discussed as pathways to reduce environmental pressures in Europe and beyond. The European Environment Agency has interviewed some selected key stakeholders  - from government, business, non-governmental organisations and academia -  and asked them which steps will bring us forward on the road to a Green economy.');
                        featured_item.fadeIn();
                    }
                    // TODO refactor this code when I have brains of the featured
                    // films and other videos that should be added as featured
                    // else {
                    // }

                }
                coverflow_imgs.removeClass('selected');
                this.className = "content selected";
            });
            // closes the fancybox window
            $("#fancybox-close").click(function(){
                media_player.fadeOut('fast',function(){content_flow.fadeIn('slow');});
                $("#media-flowplayer").children().remove();
            });
        
        }
    // end ready state
    });
}(jQuery));

