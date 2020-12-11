/* JavaScript that enables popovers for displaying artifact images and details
 * in Appendix A of the site.
 */

function setUpPopovers() {
    let figurePopovers = $(".figure-popover");
    let detailsPopovers = $(".details-popover");

    figurePopovers.popover({
        html: true,
        sanitize: false,
        title: '<span class="text-secondary">Details</span>'+
        '<button type="button" id="close" class="close" onclick="$(&quot;.figure-popover&quot;).popover(&quot;hide&quot;);">&times;</button>',
        content: function() {
            return `<img src="${this.getAttribute("data-figure-path")}"></img>
                    <br>
                    <br>
                    ${this.getAttribute("data-figure-caption")}`;
        },
        placement: "bottom",
        container: "body"
        // fallbackPlacement: "flip"
    });

    detailsPopovers.popover({
        html: true,
        sanitize: false,
        title: '<span class="text-secondary">Details</span>'+
        '<button type="button" id="close" class="close" onclick="$(&quot;.details-popover&quot;).popover(&quot;hide&quot;);">&times;</button>',
        content: function() {
            return this.getAttribute("data-details-html");
        },
        placement: "bottom",
        container: "body"
    });

};

setUpPopovers();
