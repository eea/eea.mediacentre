var LARROW_ON = "++resource++video-slider-images/larrow_on.png";
var RARROW_ON = "++resource++video-slider-images/rarrow_on.png";
var LARROW_OFF = "++resource++video-slider-images/larrow_off.png";
var RARROW_OFF = "++resource++video-slider-images/rarrow_off.png";

var NUM_ITEMS = 25;
var PAGE_WIDTH = 600;
var ITEM_WIDTH = 120;

$(document).ready(function() {
    // Make ordinary, non video links, open in parent window.
    ignore = ".video-fancybox, #vid-desc-link, #vid-dl-link, .tabnav";
    $("a").not(ignore).attr("target", "_top");

    var caption = $("#vid-title").html();
    var captionMaxLength = 70;
    if(caption.length > captionMaxLength) {
        caption = caption.substring(0, captionMaxLength) + "...";
    }
    $("h1").text(caption);

    $("#tabs").tabs();
    $(".portlet img").reflect();

    $("#docs-slider").slidersetup();
    $("#vids-slider").slidersetup();

    $("#vids-slider a").click(function() {
        $('body').html('<img id="ajax-loader" src="/++resource++faceted_images/ajax-loader.gif" />');
    });
});

jQuery.fn.extend({
    slidersetup: function() {
        var portlet = $("#" + this.attr("id") + " .portlet");
        this.data("animating", false);

        //var start = portlet.sliderPos();
        var start = 20; // Seems like CSS hasn't kicked in yet.
        portlet.data("start_pos", start);

        var end = start - ((NUM_ITEMS * ITEM_WIDTH) - PAGE_WIDTH);
        portlet.data("end_pos", end);

        this.setArrows(start);

        var obj = this;
        $("#" + obj.attr("id") + " .larrow").click(function(event) {
            obj.slide(PAGE_WIDTH);
        });
        $("#" + obj.attr("id") + " .rarrow").click(function(event) {
            obj.slide(-PAGE_WIDTH);
        });
    },

    sliderPos: function() {
        var spos = this.css("left");
        if (spos === undefined) {
            return 0;
        }
        var pos = spos.substring(0, spos.length - 2);
        return parseInt(pos, 10);
    },

    slide: function(px) {
        if (this.data("animating")) {
            return;
        }
        this.data("animating", true);
        var portlet = $("#" + this.attr("id") + " .portlet");
        var pos = portlet.sliderPos();
        pos += px;
        if (pos <= portlet.data("start_pos") && pos >= portlet.data("end_pos")) {
            obj = this;
            portlet.animate({"left": pos}, 1000, function() {
                obj.data("animating", !obj.data("animating"));
            });
        } else {
            this.data("animating", false);
        }
        this.setArrows(pos);
    },

    setArrows: function(pos) {
       var portlet = $("#" + this.attr("id") + " .portlet");
       var larrow = $("#" + this.attr("id") + " .larrow").attr("src", LARROW_ON);
       var rarrow = $("#" + this.attr("id") + " .rarrow").attr("src", RARROW_ON);
       if (pos >= portlet.data("start_pos")) {
           larrow.attr("src", LARROW_OFF);
       } else if (pos <= portlet.data("end_pos")) {
           rarrow.attr("src", RARROW_OFF);
       }
    }
});

